from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class ExtractedField(BaseModel):
    document_id: Optional[str] = Field(default=None, description="Identifier of the source document — filled in by the backend after extraction, not by the model")
    field: str = Field(..., description="The name of the extracted field, e.g., 'gross_pay', 'applicant_name', 'employer_name'")
    value: str = Field(..., description="The exact value found in the document")
    confidence_score: float = Field(..., description="Confidence score from 0.0 to 1.0", ge=0.0, le=1.0)
    page: int = Field(..., description="The page number where the field was found (1-indexed)")
    bbox: List[float] = Field(default_factory=list, description="Bounding box [x0, y0, x1, y1] if applicable. Leave empty if text-only extraction.")

class DocumentExtractionResult(BaseModel):
    document_type: Literal["pay_stub", "employment_letter", "benefit_letter", "application_summary", "unknown"]
    applicant_name: Optional[ExtractedField] = None
    employer_name: Optional[ExtractedField] = None
    gross_pay: Optional[ExtractedField] = None
    pay_period: Optional[ExtractedField] = None
    date_issued: Optional[ExtractedField] = None
    household_size: Optional[ExtractedField] = None
    
    # We will strictly ignore any other fields to comply with the rules.
