# config.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load environment variables
load_dotenv()

# === File Upload Directory ===
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# === API Key Validation ===
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY or not GOOGLE_API_KEY.startswith("AIza"):
    raise ValueError("GOOGLE_API_KEY environment variable not set correctly or missing.")

# === Language Models ===
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
    google_api_key=GOOGLE_API_KEY,
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY,
)

# === Prompt Engineering ===

# 1. Contextualization Prompt (for question rewriting)
contextualize_q_system_prompt = (
    "You are a question reformulation assistant.\n"
    "Your job is to take the user’s latest question and, if necessary, rewrite it to be a standalone question "
    "that is fully understandable without the chat history. Never answer the question. If it's already standalone, return it unchanged."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 2. QA Prompt (for final document-based answer)
qa_system_prompt = (
    "You are a helpful assistant that answers questions strictly based on the provided context."
    "Refer only to the documents. If the answer is not present, say: 'I don’t know based on the provided documents.'\n\n"
    "Context:\n{context}"
)


qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        ("assistant", "Let me check the documents and get back to you."),
    ]
)

# === Session Stores ===
session_stores = {}
chat_histories = {}
