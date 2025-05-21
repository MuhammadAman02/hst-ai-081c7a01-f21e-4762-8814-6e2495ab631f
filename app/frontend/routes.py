from nicegui import ui
from fastapi import APIRouter, UploadFile, File
from app.models.document import CustomerApplication, Document
from app.api.routes import validate_application
import aiohttp
import json
from datetime import date

router = APIRouter()

@router.get("/")
async def index():
    async def handle_submit():
        documents = []
        for file in uploaded_files:
            async with aiohttp.ClientSession() as session:
                data = aiohttp.FormData()
                data.add_field('file', file.content, filename=file.name, content_type=file.type)
                async with session.post('http://localhost:8000/api/upload-document', data=data) as response:
                    document = await response.json()
                    documents.append(Document(**document))
        
        application = CustomerApplication(
            id=str(uuid.uuid4()),
            customer_name=name.value,
            date_of_birth=date.fromisoformat(dob.value),
            pps_number=pps.value,
            documents=documents
        )
        
        results = await validate_application(application)
        
        result_text = "Validation Results:\n"
        for result in results:
            result_text += f"Document {result.document_id}:\n"
            result_text += f"Valid: {result.is_valid}\n"
            if result.errors:
                result_text += "Errors:\n" + "\n".join(result.errors) + "\n"
            if result.warnings:
                result_text += "Warnings:\n" + "\n".join(result.warnings) + "\n"
            result_text += "\n"
        
        ui.notify(result_text)

    with ui.card():
        ui.label('Document Validation Application').classes('text-h4')
        name = ui.input('Customer Name')
        dob = ui.input('Date of Birth', input_type='date')
        pps = ui.input('PPS Number')
        uploaded_files = ui.upload(multiple=True, label='Upload Documents').props('accept=.pdf,.jpg,.png')
        ui.button('Submit', on_click=handle_submit)

    ui.run()

@router.get("/results")
async def results():
    with ui.card():
        ui.label('Validation Results').classes('text-h4')
        # This is a placeholder. In a real application, you would fetch and display actual results here.
        ui.label('No results to display.')

    ui.run()