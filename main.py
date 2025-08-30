import os
from vector_db_handler import VectorDBHandler
from tools import get_tools
from agents import AgentHandler

from warnings import filterwarnings
filterwarnings('ignore')

vectordb_handler = VectorDBHandler

def init_agent():
    #  Load vector db and ingest doc if needed


    tools = get_tools()

    agent = AgentHandler(tools)
    return agent

def insert_new_document(uploaded_file):
    file_path = os.path.join("./docs", uploaded_file.name)
    with open(file_path, "wb") as f:        
        f.write(uploaded_file.read())
    
    vectordb_handler.ingest_uploaded_file(file_path)
    


# if __name__ == "__main__":
#     agent = init_agent()
#     print(agent.run("What's the average temperature in Paris over the last 3 days in Fahrenheit?"))


























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
