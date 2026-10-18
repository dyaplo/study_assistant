import streamlit as st
import uuid
import os
from utils.pdf_reader import extract_text_from_pdf
from utils.text_splitter import split_text
from utils.rag import add_documents_to_db, ask_question
from utils.chat_history import save_chat, load_chat

st.set_page_config(page_title="Study Assistant", page_icon="📚", layout="wide")
os.makedirs("data/uploads", exist_ok=True)
st.title("📚 Study Assistant")
st.write("Upload a PDF file, and ask questions about its content.")

with st.sidebar:
    st.header("upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    process_button = st.button("Process PDF")

if process_button and uploaded_file is not None:
    file_path = os.path.join("data/uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    text = extract_text_from_pdf(file_path)
    if text.strip():
        chunks = split_text(text)
        add_documents_to_db(chunks)
        st.success("PDF processed you can now ask questions about its content.")
    else:
        st.error("The uploaded PDF is empty or could not be read.")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
prompt = st.chat_input("Ask a question about the PDF content:")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    answer = ask_question(prompt)
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})


