from fastapi import APIRouter, Request, HTTPException
from app.services.session_manager import UserSessionManager
from app.utils.response_handler import success_response, error_response  # Import utilities

router = APIRouter(prefix="/auth")


@router.get("/create_session")
async def create_session():
    try:
        session_manager = UserSessionManager()
        session_token = session_manager.create_session()
        return success_response(
            data={"session_token": session_token},
            message="Session created successfully"
        )
    except Exception as e:
        return error_response(
            message="Failed to create session",
            status_code=500,
            details=str(e)
        )


@router.get("/invalidate_session")
async def invalidate_session(request: Request):
    try:
        session_token = request.headers.get("Authorization")
        if not session_token:
            return error_response(message="Session token not found", status_code=400)

        session_manager = UserSessionManager()
        if session_manager.invalidate_session(session_token):
            return success_response(message="Session invalidated successfully")
        else:
            return error_response(message="Session not found or already invalidated", status_code=404)
    except Exception as e:
        return error_response(
            message="Failed to invalidate session",
            status_code=500,
            details=str(e)
        )


@router.get("/extend_session")
async def extend_session(request: Request):
    try:
        session_token = request.headers.get("Authorization")
        if not session_token:
            return error_response(message="Session token not found", status_code=400)

        session_manager = UserSessionManager()
        new_session_token = session_manager.extend_session(session_token)
        return success_response(
            data={"session_token": new_session_token},
            message="Session extended successfully"
        )
    except Exception as e:
        return error_response(
            message="Failed to extend session",
            status_code=500,
            details=str(e)
        )
