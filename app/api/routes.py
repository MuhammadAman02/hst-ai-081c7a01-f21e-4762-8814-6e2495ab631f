from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.document import Document, CustomerApplication, ValidationResult
from app.services.document_processor import DocumentProcessor
from app.services.validation_engine import ValidationEngine
from typing import List
import uuid

router = APIRouter()

@router.post("/upload-document", response_model=Document)
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    document = Document(
        id=str(uuid.uuid4()),
        type=file.content_type,
        content=content.decode(),
        metadata={"filename": file.filename}
    )
    return document

@router.post("/validate-application", response_model=List[ValidationResult])
async def validate_application(application: CustomerApplication):
    results = []
    for document in application.documents:
        processed_text = await DocumentProcessor.process_document(document)
        extracted_data = await DocumentProcessor.extract_data(processed_text)
        validation_result = await ValidationEngine.validate_document(document, extracted_data)
        results.append(validation_result)
    
    cross_validation_results = await ValidationEngine.cross_validate_documents(application.documents, [await DocumentProcessor.extract_data(await DocumentProcessor.process_document(doc)) for doc in application.documents])
    results.extend(cross_validation_results)
    
    return results

@router.get("/ping")
async def ping_pong():
    return {"message": "pong!"}