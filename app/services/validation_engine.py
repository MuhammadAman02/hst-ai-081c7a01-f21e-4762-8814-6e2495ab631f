from app.models.document import Document, ValidationResult
from typing import List

class ValidationEngine:
    @staticmethod
    async def validate_document(document: Document, extracted_data: dict) -> ValidationResult:
        errors = []
        warnings = []

        # Implement validation rules here
        # This is a placeholder for demonstration purposes
        if len(extracted_data["extracted_text"]) < 50:
            warnings.append("Document content seems too short")

        if extracted_data["word_count"] < 10:
            errors.append("Document doesn't contain enough information")

        return ValidationResult(
            document_id=document.id,
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    @staticmethod
    async def cross_validate_documents(documents: List[Document], extracted_data_list: List[dict]) -> List[ValidationResult]:
        # Implement cross-document validation logic here
        # This is a placeholder for demonstration purposes
        results = []
        for doc, data in zip(documents, extracted_data_list):
            result = await ValidationEngine.validate_document(doc, data)
            results.append(result)
        return results