from fastapi import Depends, HTTPException, Request
from app.services.session_manager import UserSessionManager

def validate_session(request: Request):
    """
    Dependency to validate session token for specific routes.
    """
    try:
        # Get the session token from headers
        session_token = request.headers.get("Authorization")
        if not session_token:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        # split Token strign and actual token
        session_token = session_token.split()[1]

        # Initialize the UserSessionManager
        session_manager = UserSessionManager()

        # Validate the session token
        session_data = session_manager.get_session(session_token)

        if not session_data:
            raise HTTPException(status_code=401, detail="Invalid or expired session")

        # Attach session data to the request
        request.state.session_data = session_data
        return session_data
    except:
        raise HTTPException(status_code=500, detail='Internal Server Error')
