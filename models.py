from pydantic import BaseModel
import uuid

class DocumentInput(BaseModel):
    file_path: str

class ChatThread:
    def __init__(self, asset_id: str):
        self.thread_id = str(uuid.uuid4())
        self.asset_id = asset_id
        self.messages = []

class StartChatInput(BaseModel):
    asset_id: str

class PostMessageInput(BaseModel):
    chat_thread_id: str
    user_message: str