import streamlit as st
import os
from main import init_agent, insert_new_document
# from vector_db_handler import VectorDBHandler

st.set_page_config(page_title="AI Agent", layout="wide")
st.title("Agentic Chatbot with RAG + Tools + PDF Upload")

# Initialize Agent
agent = init_agent()


# uploaded documents list
st.subheader('Already Uploaded Documents')
already_uploaded_file= []

document_store_path = './docs'

if not os.path.exists(document_store_path):
    os.makedirs(document_store_path)

for files in os.listdir(document_store_path):
    already_uploaded_file.append(files)

# print(already_uploaded_file)
st.write(already_uploaded_file)


# Upload PDFs
st.subheader(" Upload Documents")
uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)


if uploaded_files:

    os.makedirs("./docs", exist_ok=True)
    for uploaded_file in uploaded_files:
        insert_new_document(uploaded_file)
        print("\nFile uploaded=================", uploaded_file)
    st.success(f"{len(uploaded_files)} PDF(s) uploaded and indexed successfully!")


st.divider()

st.subheader("Chat with AI Agent")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

query = st.text_input("Ask me anything:")

if st.button("Submit") and query:
    with st.spinner("Thinking..."):
        answer = agent.run(query)
        print("Answer", answer)
        ai_response = answer['messages'][-1].content
        final_answer = ai_response.split("Final Answer:")[-1].strip()
        st.session_state["chat_history"].append((query, final_answer))
        st.success(final_answer)

# Display Chat History
st.subheader(" Chat History")
for q, a in st.session_state["chat_history"]:
    st.write(f"**You:** {q}")
    st.write(f"**Agent:** {a}")
