from fastapi import APIRouter, Request, HTTPException, Depends, File, UploadFile
from fastapi.security.api_key import APIKeyHeader
from app.dependencies.session_validator import validate_session
from app.services.rag import RAG
from app.services.file_upload import FileUpload
from app.services.rag_session_manager import RagSessionManager
from app.utils.response_handler import success_response, error_response

router = APIRouter(prefix="/upload")
api_key = APIKeyHeader(name="Authorization", auto_error=True)

@router.post("/upload", dependencies=[Depends(api_key), Depends(validate_session)]) 
async def upload(file: UploadFile = File(...), request: Request = None):
    try:
        # Get the uploaded file from the request
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Session data 
        session_data = request.state.session_data

        # store file
        file_upload = FileUpload()
        file_name = file_upload.upload_file(file, session_data)

        # Process the file
        rag = RAG()
        rag.process_file(file_name, session_data)
        
        RagSessionManager.add_session(session_data["session_id"], rag)
    
        return success_response(message="File uploaded successfully and processed",status_code=200)
    except ValueError as e:
        return error_response(message="Invalid file format", status_code=400,details=str(e))
    except Exception as e:
        return error_response(message="Failed to upload file", status_code=500, details=str(e))