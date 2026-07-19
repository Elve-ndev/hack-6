from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from backend.app.submission_engine import build_submission

app = FastAPI(title="RealDoor Backend API", description="Deterministic Calculator and Temporary Upload Handler")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Host frontend static files directly from the backend to simplify deployment (Critique 3 / CORS workaround)
from fastapi.staticfiles import StaticFiles
current_dir = os.path.dirname(os.path.abspath(__file__))
public_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "Frontend_V2", "Frontend", "public"))
if not os.path.exists(public_dir):
    public_dir = os.path.abspath(os.path.join(current_dir, "..", "Frontend", "public"))

if os.path.exists(public_dir):
    app.mount("/static", StaticFiles(directory=public_dir), name="static")

# Stateful global session stores mapped by unique Session IDs (Critique 3 & ADV-002)
SESSION_STORES = {}

def get_session_store(request: Request) -> Dict[str, Any]:
    session_id = request.headers.get("X-Session-ID", "default_session")
    if session_id not in SESSION_STORES:
        SESSION_STORES[session_id] = {
            "uploaded_documents": [],
            "income_sources": {},
            "household_size": 1,
            "last_profile": None,
            "readiness": None
        }
    return SESSION_STORES[session_id]

class SubmissionRequest(BaseModel):
    household_id: str
    annualized_income: float
    household_size: int
    citations: List[Dict[str, Any]]
    packet_status: str
    review_reasons: Optional[List[str]] = None

@app.post("/submission")
async def get_submission(req: SubmissionRequest):
    return build_submission(
        req.household_id, req.annualized_income, req.household_size,
        req.citations, req.packet_status, req.review_reasons
    )

@app.get("/")
async def read_root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/safargate.html")

from ai.extraction_pipeline import process_pdf

@app.post("/upload")
async def upload_document(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()

    try:
        extracted_data = await process_pdf(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    # Fill in document_id ourselves — the model doesn't know the filename
    for field_name in ["applicant_name", "employer_name", "gross_pay", "pay_period", "date_issued", "household_size"]:
        field_value = getattr(extracted_data, field_name)
        if field_value is not None:
            field_value.document_id = file.filename

    # Save to stateful session store
    session = get_session_store(request)
    doc_type = extracted_data.document_type if getattr(extracted_data, "document_type", None) else "unknown"
    doc_data = {
        "filename": file.filename,
        "document_type": doc_type,
        "date_issued": extracted_data.date_issued.value if extracted_data.date_issued else None,
        "employer_name": extracted_data.employer_name.value if extracted_data.employer_name else None,
        "gross_pay": extracted_data.gross_pay.value if extracted_data.gross_pay else None,
        "pay_period": extracted_data.pay_period.value if extracted_data.pay_period else None,
        "household_size": extracted_data.household_size.value if extracted_data.household_size else None
    }
    session["uploaded_documents"].append(doc_data)

    return {
        "status": "success",
        "filename": file.filename,
        "message": "File processed and saved in session. Extraction data below.",
        "extracted_data": extracted_data.model_dump()
    }

from backend.app.calculate import evaluate_income
from backend.app.rules_engine import get_income_limit_rule
from backend.app.profile_engine import calculate_annualized_income
from ai.citation_engine import explain_rule

class ProfileRequest(BaseModel):
    gross_pay: str
    pay_period: str
    household_size: str
    employer_name: Optional[str] = None
    date_issued: Optional[str] = None

@app.post("/validate_profile")
async def validate_profile(request: Request, req: ProfileRequest):
    """
    Step 2: Profile.
    Takes user-confirmed extracted data, deterministically calculates annualized income.
    Supports summing multiple income sources (Critique 5).
    """
    session = get_session_store(request)
    try:
        annualized = calculate_annualized_income(req.gross_pay, req.pay_period)
        hh_size = int(req.household_size)
        session["household_size"] = hh_size
        
        # Track income source by unique document ID/date to prevent overwriting same-employer documents (Critique 5)
        doc_id = req.date_issued or f"source_{len(session['income_sources'])}"
        session["income_sources"][doc_id] = annualized
        
        total_income = sum(session["income_sources"].values())
        
        session["last_profile"] = {
            "annualized_income": total_income,
            "household_size": hh_size,
            "employer_name": req.employer_name or "default_source",
            "date_issued": req.date_issued
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return {
        "status": "success",
        "annualized_income": total_income,
        "household_size": hh_size,
        "message": "Profile validated and income annualized/summed deterministically."
    }

class UnderstandRequest(BaseModel):
    annualized_income: float
    household_size: int
    question: Optional[str] = None

@app.post("/understand")
async def understand_rules(req: UnderstandRequest):
    """
    Step 3: Understand.
    Runs the deterministic calculation, looks up the official rule, 
    and returns a plain-language explanation citing the source.
    """
    try:
        # 1. Math calculation (No AI)
        math_result = evaluate_income(req.annualized_income, req.household_size)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # 2. Rules Engine
    rule = get_income_limit_rule(req.household_size)
    
    # 3. Citation Engine (AI Explanation)
    try:
        explanation = await explain_rule(math_result, rule, req.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Explanation failed: {str(e)}")
        
    return {
        "status": "success",
        "math_result": math_result,
        "rule_cited": rule,
        "explanation": explanation
    }

from backend.app.prepare_engine import check_packet_readiness

class PrepareRequest(BaseModel):
    documents: Optional[List[Dict[str, Any]]] = None

@app.post("/prepare")
async def prepare_packet(request: Request, req: PrepareRequest):
    """
    Step 4: Prepare.
    Checks the user's documents against the checklist.
    """
    session = get_session_store(request)
    try:
        docs = req.documents if req.documents is not None else session["uploaded_documents"]
        readiness = check_packet_readiness(docs)
        session["readiness"] = readiness
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check readiness: {str(e)}")
        
    return {
        "status": "success",
        "readiness": readiness
    }

@app.get("/session")
async def get_session(request: Request):
    """
    Verification route (Critique 3).
    Allows checking that the session was deleted or viewing current values.
    """
    session = get_session_store(request)
    return {
        "status": "success",
        "session_data": session
    }

@app.delete("/session")
async def delete_session(request: Request):
    """
    Step 5: Security Delete Test.
    Wipes all temporary files, session states, and in-memory lists (Critique 3).
    """
    session = get_session_store(request)
    session["uploaded_documents"] = []
    session["income_sources"] = {}
    session["household_size"] = 1
    session["last_profile"] = None
    session["readiness"] = None
    return {
        "status": "success",
        "message": "All session data, including uploaded documents and extracted fields, has been permanently deleted from memory."
    }

from fastapi.responses import PlainTextResponse
from backend.app.packet.export_engine import generate_export_packet

class ExportRequest(BaseModel):
    profile_data: Dict[str, Any]
    rule_data: Dict[str, Any]
    readiness_data: Dict[str, Any]

@app.post("/export")
async def export_packet(req: ExportRequest):
    """
    Step 4: Export.
    Generates the final downloadable text file.
    Includes verification of frontend data on the backend (Critique 4).
    """
    # 1. Verification of math calculations on the backend (Defense in Depth)
    income = req.profile_data.get("annualized_income", 0.0)
    size = req.profile_data.get("household_size", 1)
    
    math_result = evaluate_income(income, size)
    rule = get_income_limit_rule(size)
    
    # Recalculate/override client data to match backend calculations
    req.rule_data["threshold"] = math_result["threshold"]
    req.rule_data["comparison"] = math_result["comparison"]
    req.rule_data["rule_cited"] = rule
    
    # Ensure correct status matching the schema
    status = "READY_TO_REVIEW" if not req.readiness_data.get("missing_documents") and not req.readiness_data.get("expired_documents") else "NEEDS_REVIEW"
    req.readiness_data["status"] = status
    
    try:
        packet_text = generate_export_packet(req.profile_data, req.rule_data, req.readiness_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate export: {str(e)}")
        
    return PlainTextResponse(
        content=packet_text, 
        headers={"Content-Disposition": 'attachment; filename="realdoor_application_packet.txt"'}
    )
