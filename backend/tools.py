# LANGCHAIN MODULE IMPORTS
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools import tool
from fastapi import UploadFile, File
import shutil

# INTERNAL FILES IMPORT
from vector_db_handler import VectorDBHandler
from agents import AgentHandler

from warnings import filterwarnings
filterwarnings('ignore')


import os
from dotenv import load_dotenv
load_dotenv()
os.environ['SERPER_API_KEY'] = os.environ.get('SERPER_API_KEY')

vectordb_handler = VectorDBHandler()
retriever = vectordb_handler.get_retriever()
search = GoogleSerperAPIWrapper()


# ----------- WEB SEARCH TOOL -----------@tool
def google_search(query):
    """ This tool is used to search any information from Google, useful for when you need to ask with search"""
    return search.results(query)



# ----------- VECTOR DB SEARCH TOOL -----------
@tool
def vectordb_search_tool(query):
    """Search or fetch data from vector db which is ingested from pdf.
       Use this tool ONLY when the user asks questions
       about uploaded documents, PDFs, internal files,
       Aadhaar cards, contracts, or previously stored content.
    """
    print('\n\n VectorDB tool is called===================')
    docs = retriever.invoke(query)
    print("Vector db Retrieved document", docs)
    return "\n".join([d.page_content for d in docs])

# ------------------- Priority tool--------------
@tool
def priority_scoring_tool(urgency, impact, effort) -> str:
    """
    Calculates a priority score (0-10) for a task.
    Inputs:
    - urgency: 1-10 (10 being most urgent)
    - impact: 1-10 (10 being highest stakeholder impact)
    - effort: 1-5 (5 being highest effort/time)
    """
    # Logic: High Urgency and Impact increase score; High Effort slightly decreases it to prioritize 'quick wins'.
    score = (int(urgency) * 0.5) + (int(impact) * 0.3) + ((6 - int(effort)) * 0.4)
    final_score = min(round(score, 2), 10.0)

    status = "P1 (Critical)" if final_score > 8 else "P2 (Medium)" if final_score > 5 else "P3 (Low)"
    return f"Priority Score: {final_score}/10. Classification: {status}"


# --- 2. NOTIFICATION / NUDGE TOOL ---
@tool
def send_notification_tool(recipient: str, message: str):
    """Proactively notifies a team member. Use for urgent updates or status alerts."""
    # Send notification to ui, for production we can integrate this with SMTP server to send mail.
    notification_payload = f"🔔 NOTIFICATION SENT TO {recipient}: {message}"

    return notification_payload


# --- 3. KNOWLEDGE SUMMARIZER (Internal helper) ---
@tool
def multi_doc_summarizer(query: str):
    """Retrieves multiple documents and provides a high-level executive summary."""
    # This leverages your existing retriever but adds a 'summarization' intent
    docs = retriever.invoke(query)
    context = "\n".join([d.page_content for d in docs])
    return f"EXECUTIVE SUMMARY BASED ON DOCS:\n{context[:1500]}..." # Simple truncation for reasoning


@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )


tools = [
         vectordb_search_tool,google_search, priority_scoring_tool, send_notification_tool, multi_doc_summarizer
    ]

middleware = [handle_tool_errors]

def init_agent():

    agent = AgentHandler(tools, middleware)
    return agent



def insert_new_document(uploaded_file: UploadFile):
    os.makedirs("../docs", exist_ok=True)

    file_path = os.path.join("../docs", uploaded_file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(uploaded_file.file, f)

    vectordb_handler.ingest_uploaded_file(file_path)





















# from agents import build_agent
# from runner import AgentRunner

# def demo():
#     agent = build_agent()
#     runner = AgentRunner(agent)
#     query = "What’s the average temperature in Paris over the last 3 days, and convert it to Fahrenheit?"
#     result = runner.ask(query)
#     print("\\n=== RESULT ===\\n", result)

# if __name__ == "__main__":
#     demo()
