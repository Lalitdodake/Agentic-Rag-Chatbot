import json
import requests

from langchain.agents import Tool
# from langchain.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities import GoogleSerperAPIWrapper

# ----------- WEATHER TOOL -----------
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['SERPER_API_KEY'] = os.environ.get('SERPER_API_KEY')

from vector_db_handler import VectorDBHandler
vectordb_handler = VectorDBHandler()

vector_retriever = vectordb_handler.get_retriever()

def get_tools():
    # Web Search Tool
    search = GoogleSerperAPIWrapper()

    def weather_tool(query):
        return search.run(f"Weather {query}")

    # Vector Db Search Tool
    
    def vectordb_search_tool(query):
        docs = vector_retriever.get_relevant_documents(query)
        return "\n".join([d.page_content for d in docs])

    tools = [
        Tool(
            name="Weather",
            func=weather_tool,
            description="Get the latest weather details for a location."
        ),
        Tool(
            name = 'VectorDbSearch',
            func=vectordb_search_tool,
            description="Search or fetch data from vector db which is ingested from pdf. "
        )
    ]
    return tools
