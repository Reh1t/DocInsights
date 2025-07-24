# helpers.py
import os
import tempfile
import shutil
import uuid
from typing import List
from fastapi import UploadFile
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.vectorstores import FAISS


from config import (
    llm, embeddings,
    contextualize_q_prompt, contextualize_q_system_prompt,
    qa_prompt, qa_system_prompt,
    session_stores, chat_histories, UPLOAD_DIR
)
from extractors import extract_text_from_file

def process_uploaded_files(task: str, files: List[UploadFile]) -> str:
    session_id = str(uuid.uuid4())
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp(dir=UPLOAD_DIR)
        all_extracted_text = ""

        valid_extensions = {'.pdf', '.txt', '.docx', '.html'}
        for file in files:
            if file.filename == '':
                continue
            _, ext = os.path.splitext(file.filename)
            if ext.lower() not in valid_extensions:
                raise ValueError(f"Invalid file type: {ext}")

            file_location = os.path.join(temp_dir, file.filename)
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object)

            extracted_text = extract_text_from_file(file_location)
            all_extracted_text += f"\n--- Content from {file.filename} ---\n{extracted_text}\n"
            
            if not all_extracted_text.strip():
                raise ValueError("No valid text could be extracted from the uploaded files.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = [Document(page_content=all_extracted_text)]
        splits = text_splitter.split_documents(docs)

        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

        session_stores[session_id] = {
            "task": task,
            "vectorstore": vectorstore
        }
        chat_histories[session_id] = [HumanMessage(content=task)]

        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

        return session_id

    except Exception as e:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise e

def chat_with_session(session_id: str, user_message: str):
    if session_id not in session_stores or session_id not in chat_histories:
        return "Error: Session not found. Please upload files first.", None

    try:
        initial_task = session_stores[session_id]["task"]
        vectorstore = session_stores[session_id]["vectorstore"]
        chat_history = chat_histories[session_id]

        chat_history.append(HumanMessage(content=user_message))
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

        try:
            contextualize_q_chain = contextualize_q_prompt | llm
            contextualized_input = {
                "input": user_message,
                "chat_history": chat_history[:-1]
            }
            contextualized_question_response = contextualize_q_chain.invoke(contextualized_input)
            contextualized_question = getattr(contextualized_question_response, 'content', str(contextualized_question_response)).strip()
        except Exception as ctx_e:
            print(f"Contextualization failed: {ctx_e}")
            formatted_history = "\n".join(
                f"{'user' if isinstance(msg, HumanMessage) else 'assistant'}: {msg.content}"
                for msg in chat_history[:-1]
            )
            contextualized_prompt = (
                f"{contextualize_q_system_prompt}\n\nChat History:\n{formatted_history}\nHuman: {user_message}\nStandalone Question:"
            )
            fallback_response = llm.invoke(contextualized_prompt)
            contextualized_question = getattr(fallback_response, 'content', str(fallback_response)).strip()

        docs = retriever.invoke(contextualized_question)
        context_text = "\n\n".join([doc.page_content for doc in docs])

        qa_chain_input = {
            "input": user_message,
            "chat_history": chat_history[:-1],
            "context": context_text,
            "initial_task": initial_task
        }

        try:
            qa_chain = qa_prompt | llm
            ai_msg = qa_chain.invoke(qa_chain_input)
            response_text = getattr(ai_msg, 'content', str(ai_msg)).strip()
        except Exception as qa_e:
            print(f"QA fallback: {qa_e}")
            formatted_history = "\n".join(
                f"{'user' if isinstance(msg, HumanMessage) else 'assistant'}: {msg.content}"
                for msg in chat_history[:-1]
            )
            full_prompt = (
                f"{qa_system_prompt.format(initial_task=initial_task, context=context_text)}\n\n"
                f"Chat History:\n{formatted_history}\nHuman: {user_message}\nAssistant:"
            )
            qa_response = llm.invoke(full_prompt)
            response_text = getattr(qa_response, 'content', str(qa_response)).strip()

        chat_history.append(AIMessage(content=response_text))
        return response_text, session_id

    except Exception as e:
        error_msg = f"Error during chat: {str(e)}"
        print(error_msg)
        return error_msg, session_id
