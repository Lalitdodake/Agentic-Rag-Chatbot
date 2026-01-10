# LANGCHAIN MODULE IMPORTS
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools import tool

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


# ----------- WEATHER TOOL -----------
@tool
def weather_tool(query):
    """Get the latest weather details for a location."""
    print('\n\n Weather tool is called===================')
    return search.run(f"Weather {query}")


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
    print("Vector db Retrieved document")
    return "\n".join([d.page_content for d in docs])


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
        weather_tool, vectordb_search_tool,google_search
    ]

middleware = [handle_tool_errors]

def init_agent():

    agent = AgentHandler(tools, middleware)
    return agent


def insert_new_document(uploaded_file):
    file_path = os.path.join("./docs", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

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
