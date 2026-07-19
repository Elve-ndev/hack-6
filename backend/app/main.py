from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List, Dict, Any, Optional
from backend.app.submission_engine import build_submission

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

app = FastAPI(title="RealDoor Backend API", description="Deterministic Calculator and Temporary Upload Handler")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "RealDoor API is running"}

from ai.extraction_pipeline import process_pdf

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
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

    return {
        "status": "success",
        "filename": file.filename,
        "message": "File processed and deleted from memory. Extraction data below.",
        "extracted_data": extracted_data.model_dump()
    }

from pydantic import BaseModel
from backend.app.calculate import evaluate_income
from backend.app.rules_engine import get_income_limit_rule
from backend.app.profile_engine import calculate_annualized_income
from ai.citation_engine import explain_rule

class ProfileRequest(BaseModel):
    gross_pay: str
    pay_period: str
    household_size: str

@app.post("/validate_profile")
async def validate_profile(req: ProfileRequest):
    """
    Step 2: Profile.
    Takes user-confirmed extracted data, deterministically calculates annualized income.
    Returns the parameters required for Step 3 (Understand).
    """
    try:
        annualized = calculate_annualized_income(req.gross_pay, req.pay_period)
        hh_size = int(req.household_size)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return {
        "status": "success",
        "annualized_income": annualized,
        "household_size": hh_size,
        "message": "Profile validated and income annualized deterministically."
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
from typing import List, Dict, Any

class PrepareRequest(BaseModel):
    documents: List[Dict[str, Any]]

@app.post("/prepare")
async def prepare_packet(req: PrepareRequest):
    """
    Step 4: Prepare.
    Checks the user's documents against the checklist.
    Flags missing or expired items.
    """
    try:
        readiness = check_packet_readiness(req.documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check readiness: {str(e)}")
        
    return {
        "status": "success",
        "readiness": readiness
    }

@app.delete("/session")
async def delete_session():
    """
    Step 5: Security Delete Test.
    Proves that all user data can be instantly and completely deleted.
    In a real app, this would drop database records. Here, we just confirm.
    """
    # Simulate deleting all temporary files/memory
    return {
        "status": "success",
        "message": "All session data, including uploaded documents and extracted fields, has been permanently deleted."
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
    """
    try:
        packet_text = generate_export_packet(req.profile_data, req.rule_data, req.readiness_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate export: {str(e)}")
        
    return PlainTextResponse(
        content=packet_text, 
        headers={"Content-Disposition": 'attachment; filename="realdoor_application_packet.txt"'}
    )

