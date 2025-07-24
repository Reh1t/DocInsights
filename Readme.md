# 📚 Doc Insights

**Doc Insights** is an intelligent document-based chatbot that transforms your uploaded files into a conversation. Designed for students, researchers, and professionals, it enables interactive dialogue with your documents using modern LLMs and smart retrieval techniques.

---

## 🚀 Features

- ✅ Upload and process multiple document formats (`.pdf`, `.docx`, `.txt`, `.html`)
- ✅ Define a **custom task** (e.g., “Summarize these reports”, “Analyze this resume”)
- ✅ Smart chunking & embedding for deep understanding
- ✅ Interactive chatbot powered by **Gemini or OpenAI**
- ✅ Modern Gradio UI with **animated transitions** and toggles
- ✅ Reset chat to switch tasks dynamically without reloading

---

## 📂 Supported File Types

- `.pdf` – Reads and extracts readable page content
- `.txt` – Plain text file support
- `.docx` – Extracts both text and tables
- `.html` – Parses visible text; ignores scripts and styling

---

## 🧠 Tech Stack

| Layer         | Tools Used                          |
|--------------|-------------------------------------|
| **Frontend**  | Gradio (with custom layout & fade-in transitions) |
| **Backend**   | FastAPI + LangChain                 |
| **LLMs**      | Gemini (Google Generative AI) or OpenAI GPT-4o-mini |
| **Embeddings**| FAISS + GoogleGenerativeAIEmbeddings |
| **Parsing**   | PyMuPDF, python-docx, BeautifulSoup |

---

## 🧪 How It Works

1. **User uploads documents** and provides a task (e.g., summarize or analyze).
2. All files are **automatically parsed** and their content extracted.
3. Text is **split into chunks** and converted to **embeddings** using Gemini.
4. Questions are contextualized based on **chat history + task**.
5. Relevant chunks are retrieved and passed to the LLM.
6. You get a helpful, task-relevant response instantly.

---

## 🧪 Testing & Validation

- ✅ **API Testing**: Verified all endpoints (`/upload`, `/chat`) independently.
- ✅ **Document Testing**: Uploaded valid/invalid files to check error handling.
- ✅ **Gemini/OpenAI Testing**: Verified Gemini fallback logic and session behavior.
- ✅ **Chat State Testing**: Ensured history, reset, and session transitions work.
- ✅ **Frontend UX Testing**: Fade-in/out animations, reset buttons, and scrollable UI.

---

## 🎯 Use Cases

- 📊 Analyze financial or investment reports
- 🧑‍🏫 Summarize lecture slides or resumes
- 📚 Extract ideas from long academic texts
- 🤖 Build internal document assistants

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/Reh1t/DocInsights
cd doc-insights
python -m venv venv
venv\Scripts\activate   # or source venv/bin/activate

pip install -r requirements.txt
```

---

### 🔑 Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
# or if using OpenAI
# OPENAI_API_KEY=your_openai_api_key
```

---

## 🖥️ Run the App

```bash
# Start FastAPI backend
uvicorn main:app --reload

# In another terminal, launch the frontend
python ui.py
```

Go to [http://127.0.0.1:7860](http://127.0.0.1:7860) to try it out.

---

## ✅ What’s Done

- [x] Full chatbot backend (FastAPI + LangChain)
- [x] File parsing system (`extractors.py`)
- [x] Custom fallback for contextual question generation
- [x] Smart UI with fade transitions using Gradio
- [x] Reset button and full frontend-interaction logic
- [x] Modular codebase (`config.py`, `helpers.py`, etc.)
- [x] Language support beyond English (Handled by Gradio By Default)

---

## 💡 Extra Work & Improvements (Beyond Scope)

- 🌐 **Production-style UI** (fade-in/out UX, section toggles)
- 🧠 **Custom Contextualizer** with fallback for broken model responses
- 🔁 **Reset Button** restores task section without refreshing the app
- 🧪 **Tested for multiple document types & error handling**
- 🧼 **Session preservation across questions**
- 🛠️ **Code split into logical files** (clean and production-ready)

---

## 🛠️ Future Improvements

- [ ] Streaming support for premium APIs
- [ ] UI toggle to switch between Developer and User API
- [ ] Chat history download / export
- [ ] Model cost usage indicator

---

## 🤝 Contributing

Contributions are welcome. Feel free to fork and send a PR with enhancements!

---

## 🧠 Credits

Built with:

- [LangChain](https://www.langchain.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Gradio](https://www.gradio.app/)
- [FAISS](https://github.com/facebookresearch/faiss)

---

## 📜 License

Developed by Rehan Tariq

---
