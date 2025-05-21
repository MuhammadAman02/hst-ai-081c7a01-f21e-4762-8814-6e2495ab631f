from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Document(BaseModel):
    id: str
    type: str
    content: str
    metadata: dict

class ValidationResult(BaseModel):
    document_id: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class CustomerApplication(BaseModel):
    id: str
    customer_name: str
    date_of_birth: date
    pps_number: str
    documents: List[Document]
    validation_results: Optional[List[ValidationResult]]