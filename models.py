# models.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    session_id: str

class UploadResponse(BaseModel):
    message: str
    session_id: str
    initial_task: str
