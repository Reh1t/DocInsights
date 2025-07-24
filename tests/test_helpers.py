import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import io
from fastapi import UploadFile
from helpers import process_uploaded_files
from config import session_stores, chat_histories


def test_process_uploaded_txt_file():
    # Create a fake UploadFile object
    content = b"Test content from txt file."
    file = UploadFile(filename="test.txt", file=io.BytesIO(content))
    session_id = process_uploaded_files("Summarize this", [file])
    
    assert session_id in session_stores
    assert session_id in chat_histories
    assert session_stores[session_id]["task"] == "Summarize this"


def test_chunking_and_vectorstore():
    from config import embeddings
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document

    text = "Gemini is a powerful LLM by Google designed for complex tasks. " * 20
    doc = Document(page_content=text)
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    chunks = splitter.split_documents([doc])

    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever()
    results = retriever.invoke("What is Gemini?")
    assert results
