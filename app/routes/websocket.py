from app.services.rag_session_manager import RagSessionManager

@app.websocket("/chat/{session_id}")
async def chat(websocket: WebSocket, session_id: str):
    await websocket.accept()

    # Retrieve the RAG instance for this session
    rag = RagSessionManager.get_session(session_id)

    if not rag:
        await websocket.json({"event": "error", "code": 404, "message": "RAG instance not found"})
        await websocket.close()
        return

    await websocket.json({"event": "ready","code":200, "message": "Query processing started"})

    try:
        while True:
            # Receive a query from the client
            user_query = await websocket.receive_text()

            # Process the query with streaming
            async for chunk in stream_rag_response(rag, user_query):
                await websocket.json({"event": "message", "data": chunk, "code": 200, message: "Query processed successfully"})  # Stream response to the client
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        print(f"Error in WebSocket session {session_id}: {e}")
    finally:
        # Clean up the session after disconnect
        RagSessionManager.remove_session(session_id)
