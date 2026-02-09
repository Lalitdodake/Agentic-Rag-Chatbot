# main.py
from fastapi import FastAPI, UploadFile, File, responses
from pydantic import BaseModel
import uuid
import os
from tools import init_agent, insert_new_document
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

app = FastAPI(title="Agentic RAG API")

# -------- Initialize Agent (ONCE) --------
print("Loading Agent")
agent = init_agent()
print("Agent Ready ")

# -------- Schemas --------
class ChatRequest(BaseModel):
    query: str
    thread_id: str | None = None


class ChatResponse(BaseModel):
    answer: str


# -------- API 1: Insert Document --------
@app.post("/insert-document")
def insert_document(file: UploadFile = File(...)):
    try:
        insert_new_document(file)
        print("File====", file)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        print("Error", e)
        return {"status": "error", "detail": str(e)}


# -------- API 2: Chat with Agent --------
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    thread_id = req.thread_id
    query = req.query

    result = agent.run(query, thread_id)

    ai_msg = result["messages"][-1].content
    final_answer = ai_msg.split("Final Answer:")[-1].strip()
    print("final_answer",final_answer)
    return {
        "answer": final_answer}