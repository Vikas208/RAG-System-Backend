from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.rag_session_manager import RagSessionManager
import json

router = APIRouter(prefix="/ws")

@router.websocket("/chat/{session_id}")
async def chat(websocket: WebSocket, session_id: str):
    await websocket.accept()
    # Check user is authenticated

    # Retrieve the RAG instance for this session
    rag = RagSessionManager.get_session(session_id)

    if not rag:
        await websocket.send_json({"event": "error", "code": 404, "message": "Session not found"})
        await websocket.close()
        return

    await websocket.send_json({"event": "ready","code":200, "message": "Welcome to the chat bot"})

    try:
        while True:
            # Receive a query from the client
            event = await websocket.receive_json()

            event_type = event.get('type')
            query = event.get('query')

            if event_type == 'error':
                await websocket.send_json({"event": "error", "code": event.code, "message": event.message})
                await websocket.close()
                break
                
            if event_type == 'question':
                # Process the query with streaming
                response = rag.answer_question(query)
                print(response)
                # Send the response back to the client
                await websocket.send_json({"event": "response", "message": response['result'], "code":200})

            elif event_type == 'close':
                await websocket.close()
                break
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        print(f"Error in WebSocket session {session_id}: {e}")
    finally:
        # Clean up the session after disconnect
        # RagSessionManager.remove_session(session_id)
        pass
