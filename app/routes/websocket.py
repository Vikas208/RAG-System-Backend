from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.rag_session_manager import RagSessionManager

router = APIRouter(prefix="/ws")

@router.websocket("/chat/{session_id}")
async def chat(websocket: WebSocket, session_id: str):
    await websocket.accept()

    # Retrieve the RAG instance for this session
    rag = RagSessionManager.get_session(session_id)

    if not rag:
        await websocket.send_json({"event": "error", "code": 404, "message": "RAG instance not found"})
        await websocket.close()
        return

    await websocket.send_json({"event": "ready","code":200, "message": "Query processing started"})

    try:
        while True:
            # Receive a query from the client
            event = await websocket.receive_json()
            
            if event.type == 'question':
                user_query = event.data
                # Process the query with streaming
                response = rag.answer_question(user_query)

                # Send the response back to the client
                await websocket.send_json({"event": "response", "data": response['result'], "code":200})
            
            elif event.type == 'close':
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
