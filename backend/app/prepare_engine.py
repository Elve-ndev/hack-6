from typing import List, Dict, Any
from datetime import datetime, timedelta

REQUIRED_DOCUMENTS = [
    "application_summary",
    "pay_stub",
    "employment_letter"
]

def check_packet_readiness(uploaded_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates the application packet against a checklist.
    Checks for missing documents and expired documents.
    """
    present_types = [doc.get("document_type") for doc in uploaded_docs]
    missing_docs = []
    
    for req in REQUIRED_DOCUMENTS:
        if req not in present_types:
            missing_docs.append(req)
            
    expired_docs = []
    warnings = []
    
    anchor_date = datetime(2026, 7, 18)
    
    for doc in uploaded_docs:
        doc_type = doc.get("document_type")
        date_issued_str = doc.get("date_issued")
        
        if date_issued_str:
            try:
                # Try parsing common formats
                date_issued = datetime.strptime(date_issued_str, "%Y-%m-%d")
                # Check if older than 60 days relative to event date (2026-07-18)
                # Also check if it is in the future relative to the event date
                if (anchor_date - date_issued).days > 60 or date_issued > anchor_date:
                    expired_docs.append(f"{doc_type} is expired (older than 60 days from 2026-07-18).")
            except ValueError:
                warnings.append(f"Could not verify date for {doc_type}: {date_issued_str}")
                
    status = "READY_TO_REVIEW" if not missing_docs and not expired_docs else "NEEDS_REVIEW"
    
    return {
        "status": status,
        "missing_documents": missing_docs,
        "expired_documents": expired_docs,
        "warnings": warnings,
        "message": "Your packet is ready to be downloaded!" if status == "READY_TO_REVIEW" else "There are issues with your application packet."
    }
