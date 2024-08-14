from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import models 
from document_processor import process_document_service
from chat_service import start_chat_service, post_message_service, get_chat_history_service

app = FastAPI()

@app.post("/api/documents/process")
async def process_document(input: models.DocumentInput):
    file_path = input.file_path
    try:
        asset_id = await process_document_service(file_path)
        return {"asset_id": asset_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/chat/start")
async def start_chat(input: models.StartChatInput):
    try:
        chat_thread_id = await start_chat_service(input.asset_id)
        return {"chat_thread_id": chat_thread_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/message")
async def post_message(input: models.PostMessageInput):
    try:
        agent_response = await post_message_service(input.chat_thread_id, input.user_message)
        return {"agent_response": agent_response}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/history")
async def get_history(chat_thread_id: str):
    try:
        messages = await get_chat_history_service(chat_thread_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/chat/{chat_thread_id}")
async def websocket_endpoint(websocket: WebSocket, chat_thread_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            user_message = data
            
            try:
                agent_response = await post_message_service(chat_thread_id, user_message)
                await websocket.send_text(agent_response)
            except ValueError as e:
                await websocket.send_text("Error: " + str(e))
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for chat thread {chat_thread_id}")