from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool
from vector_db_handler import VectorDBHandler
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage


# ----------- WEATHER TOOL -----------
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['SERPER_API_KEY'] = os.environ.get('SERPER_API_KEY')

vectordb_handler = VectorDBHandler()
retriever = vectordb_handler.get_retriever()

search = GoogleSerperAPIWrapper()


# Web Search Tool
@tool
def google_search(query):
    """ This tool is used to search any information from Google, useful for when you need to ask with search"""
    return search.results(query)

@tool
def weather_tool(query):
    """Get the latest weather details for a location."""
    print('\n\n Weather tool is called===================')
    return search.run(f"Weather {query}")


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

def get_tools():
    """ Return the available tools in a list"""
    tools = [
        weather_tool, vectordb_search_tool,google_search
    ]
    middleware = [handle_tool_errors]
    return tools, middleware
