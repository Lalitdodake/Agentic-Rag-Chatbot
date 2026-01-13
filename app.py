import streamlit as st
import os
from tools_main import init_agent, insert_new_document
import uuid
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


print("Loading App File-------------------------")
config = {"configurable": {"thread_id": str(uuid.uuid4()).split('-')[1]}}


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Agentic RAG Chatbot",
    layout="wide"
)

st.title("🤖 Agentic Chatbot")


# ---------------- Initialize Agent ----------------
@st.cache_resource
def load_agent():
    return init_agent()

agent = load_agent()

# ---------------- Session State ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- Sidebar: Document Section ----------------
with st.sidebar:
    # ---------------- New Chat ----------------
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.chat_history = []
        config = {"configurable": {"thread_id": uuid.uuid4()}}
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
        for uploaded_file in uploaded_files:
            insert_new_document(uploaded_file)
        st.success(f"{len(uploaded_files)} file(s) indexed")
# ---------------- Chat Area ----------------
st.subheader("💬 Chat")

for user_msg, ai_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(ai_msg)

query = st.chat_input("Ask me anything...")

print("Config======", config)
if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = agent.run(query, config)
            ai_response = answer["messages"][-1].content
            final_answer = ai_response.split("Final Answer:")[-1].strip()
            st.markdown(final_answer)

    st.session_state.chat_history.append((query, final_answer))