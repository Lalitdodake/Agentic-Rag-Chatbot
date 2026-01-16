import streamlit as st
import uuid
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import requests
import codecs

decoder = codecs.getincrementaldecoder("utf-8")()
print("Loading App File-------------------------")

API_URL = "http://localhost:8211"

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Agentic RAG Chatbot",
    layout="wide"
)

st.title("🤖 Agentic Chatbot")


# ---------------- Session State ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4()).split('-')[1]

print("Thread Id========", st.session_state.thread_id)
# ---------------- Sidebar: Document Section ----------------
with st.sidebar:
    # ---------------- New Chat ----------------
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.thread_id = str(uuid.uuid4()).split('-')[1]
        st.rerun()

    st.divider()

    # ---------------- Documents ----------------
    st.header("📄 Documents")

    document_store_path = "./docs"
    os.makedirs(document_store_path, exist_ok=True)

    st.subheader("Uploaded Files")
    docs = os.listdir(document_store_path)
    if docs:
        for doc in docs:
            st.write(f"• {doc}")
    else:
        st.info("No documents uploaded")

    st.divider()

    st.subheader("Upload PDFs")
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            files = {"file": (file.name, file, "application/pdf")}
            requests.post(f"{API_URL}/insert-document", files=files)

        st.success(f"{len(uploaded_files)} file(s) indexed")


# ---------------- Chat Area ----------------
st.subheader("💬 Chat")

for user_msg, ai_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(ai_msg)

# Generator Method for token Streaming

def response_generator(payload_):
    response_from_model= requests.post( f"{API_URL}/chat", json=payload_,stream=True).json()['answer']
    for token in response_from_model:
        yield token

query = st.chat_input("Ask me anything...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    payload = {
        "query": query,
        "thread_id": st.session_state.thread_id
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.write_stream(response_generator(payload))

    st.session_state.chat_history.append((query, response))