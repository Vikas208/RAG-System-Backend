import redis
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json

load_dotenv()

class UserSessionManager:
    """
    A class to manage user sessions using only session tokens for tracking.
    """

    def __init__(self, redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379"), session_expiry_minutes: int = int(os.getenv("REDIS_EXPIRY_MINUTES", 30))):
        """
        Initialize the UserSessionManager with a Redis connection.

        Args:
            redis_url (str): URL of the Redis instance.
            session_expiry_minutes (int): Time in minutes for session expiration.
        """
        self.redis = redis.StrictRedis.from_url(redis_url, decode_responses=True)
        self.session_expiry = timedelta(minutes=session_expiry_minutes)

    def create_session(self) -> str:
        """
        Create a new session and store session metadata.

        Returns:
            str: The generated session token.
        """
        session_token = str(uuid.uuid4())
        session_data = {
            "session_id": session_token,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.redis.setex(
            session_token,
            int(self.session_expiry.total_seconds()),
            value=json.dumps(session_data),  # Serialize the dictionary to a JSON string
        )
        return session_token

    def get_session(self, session_token: str) -> dict | None:
        """
        Retrieve session metadata by token.

        Args:
            session_token (str): The session token.

        Returns:
            dict: Session metadata if valid, otherwise None.
        """
        session_data = self.redis.get(session_token)
        if session_data:
            return eval(session_data)  # Convert string representation back to dict
        return None

    def invalidate_session(self, session_token: str) -> bool:
        """
        Invalidate a session.

        Args:
            session_token (str): The session token.

        Returns:
            bool: True if session invalidated, False otherwise.
        """
        return bool(self.redis.delete(session_token))

    def extend_session(self, session_token: str) -> bool:
        """
        Extend the session expiration time.

        Args:
            session_token (str): The session token.

        Returns:
            bool: True if session extended, False otherwise.
        """
        return self.redis.expire(session_token, int(self.session_expiry.total_seconds()))

    def list_active_sessions(self) -> list:
        """
        List all active session tokens. (Optional method for debugging or analytics)

        Returns:
            list: A list of all active session tokens.
        """
        return [key.decode() for key in self.redis.keys()]

