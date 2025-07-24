# ui.py
import gradio as gr
import requests
import os

# Global session ID
session_id = None

# Upload files and start session
def upload_and_start_chat(task, files):
    global session_id
    if not task or not files:
        return "Please enter a task and upload at least one file.", gr.update(visible=True), gr.update(visible=False)

    try:
        file_data = [
            ("files", (os.path.basename(file.name), open(file.name, "rb").read(), "application/octet-stream"))
            for file in files
        ]

        response = requests.post(
            "http://127.0.0.1:8000/upload/",
            data={"task": task},
            files=file_data
        )
        response.raise_for_status()
        data = response.json()
        session_id = data["session_id"]

        return f"Session started for: {task}", gr.update(visible=False), gr.update(visible=True)

    except Exception as e:
        return f"Upload failed: {str(e)}", gr.update(visible=True), gr.update(visible=False)

# Chat interaction
def chat_with_bot(message, history):
    global session_id
    if not session_id:
        return "Please upload files first."

    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat/",
            json={"session_id": session_id, "message": message}
        )
        response.raise_for_status()
        reply = response.json().get("response", "No response from server.")
        return reply
    except Exception as e:
        return f"Error: {str(e)}"

# Reset session
def reset_chat():
    global session_id
    session_id = None
    return "", [], None, gr.update(visible=True), gr.update(visible=False)

# UI layout
with gr.Blocks(title="Doc Insights", css="""
    .fade-in {
        animation: fadeIn 0.8s ease-in-out forwards;
    }
    .fade-out {
        animation: fadeOut 0.5s ease-in-out forwards;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(20px); display: none; }
    }
    .gr-chatbot {
        max-height: none !important;  /* Allow chatbot to grow */
        overflow: visible !important;
    }
    .gr-box {
        padding: 20px;
        max-width: 900px;
        margin: auto;
    }
""") as demo:
    # Title
    gr.Markdown(
        "<h1 style='text-align:center; font-size: 32px; margin-bottom: 0.5em;'>Doc Insights</h1>"
        "<p style='text-align:center; font-size: 16px;'>Smart conversations with your documents</p>"
    )

    # === Group 1: Inputs ===
    with gr.Column(visible=True, elem_id="group-1", elem_classes=["fade-in"]) as group_1:
        
        with gr.Row():
            with gr.Column():
                task_input = gr.Textbox(label="Task Description", placeholder="e.g. Analyze the uploaded reports", lines=9)
            with gr.Column():
                file_input = gr.File(label="Upload Document(s)", file_types=[".pdf", ".txt", ".docx", ".html"], file_count="multiple")
        submit_button = gr.Button("Submit", variant="primary", size="lg")
        status_output = gr.Textbox(label="Status", interactive=False)

    # === Group 2: Chat ===
    with gr.Column(visible=False, elem_id="group-2", elem_classes=["fade-in"]) as group_2:
        chatbot_ui = gr.ChatInterface(
            fn=chat_with_bot,
            chatbot=gr.Chatbot(type="messages"),  # Remove fixed height
            textbox=gr.Textbox(placeholder="Ask a question about the document...", label="Your Question"),
        )
        reset_btn = gr.Button("Reset Chat", variant="stop")

    # === Actions ===
    submit_button.click(
        upload_and_start_chat,
        inputs=[task_input, file_input],
        outputs=[status_output, group_1, group_2],
        show_progress="full"
    )

    reset_btn.click(
        reset_chat,
        outputs=[status_output, chatbot_ui.chatbot, file_input, group_1, group_2]
    )

if __name__ == "__main__":
    demo.launch()
