class RagSessionManager:
    """
    Static class to manage active RAG sessions.
    """
    active_sessions = {}

    @staticmethod
    def add_session(session_id, rag_instance):
        RagSessionManager.active_sessions[session_id] = rag_instance

    @staticmethod
    def get_session(session_id):
        return RagSessionManager.active_sessions.get(session_id, None)

    @staticmethod
    def remove_session(session_id):
        if session_id in RagSessionManager.active_sessions:
            del RagSessionManager.active_sessions[session_id]

    @staticmethod
    def session_exists(session_id):
        return session_id in RagSessionManager.active_sessions
