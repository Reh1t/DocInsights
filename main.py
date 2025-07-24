# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from typing import List

from models import ChatRequest, ChatResponse, UploadResponse
from helpers import process_uploaded_files, chat_with_session
from config import chat_histories  # for trimming chat history

app = FastAPI(title="Document Chatbot API")


@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>✅ Chatbot API is running.</h1>"


@app.post("/upload/", response_model=UploadResponse)
async def upload(
    task: str = Form(...), 
    llm_choice: str = Form(...),
    files: List[UploadFile] = File(...)
):
    try:
        session_id = process_uploaded_files(task, files, llm_choice)
        return UploadResponse(
            message="Files uploaded successfully.",
            session_id=session_id,
            initial_task=task
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # ✅ Trim history to last 6 exchanges for efficiency
        if request.session_id in chat_histories:
            chat_histories[request.session_id] = chat_histories[request.session_id][-6:]

        response, _ = chat_with_session(request.session_id, request.message)
        return ChatResponse(response=response, session_id=request.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
