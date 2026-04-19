import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Agentic RAG", page_icon="🤖", layout="wide")

st.title("📚 Agentic RAG Chatbot")

# --- Sidebar for PDF Upload ---
st.sidebar.header("Upload PDF")

if "pdf_uploaded" not in st.session_state:
    st.session_state["pdf_uploaded"] = False

uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None and not st.session_state["pdf_uploaded"]:
    with st.spinner("Uploading PDF..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{BACKEND_URL}/upload_pdf", files=files)

        if response.status_code == 200:
            st.sidebar.success(response.json()["message"])
            st.session_state["pdf_uploaded"] = True  # ✅ Prevent re-upload
        else:
            st.sidebar.error(response.json().get("error", "Upload failed"))

# --- Chat Interface ---
st.subheader("💬 Chat with your documents")

# Maintain chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Query backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(f"{BACKEND_URL}/chat", params={"query": prompt})
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.markdown(answer)
                st.session_state["messages"].append({"role": "assistant", "content": answer})
            else:
                st.error("Error: Could not get response from backend.")
