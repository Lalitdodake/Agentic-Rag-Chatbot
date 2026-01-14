from langchain.agents import create_agent
from langchain.messages import  HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from PyMongo import insert_into_db

from models import llm_model
from prompt import chat_prompt

messages = []

_store = {}



class AgentHandler:
    def __init__(self, tools, middleware):
        self.llm = llm_model

        self.llm_with_tools = self.llm.bind_tools(tools)
        self.agent = create_agent(
            model=self.llm_with_tools,
            tools=tools,
            checkpointer= InMemorySaver(),
            system_prompt  = chat_prompt,
            middleware = middleware
        )



    def run(self, query, thread_id):
        print("USER QUERY====", query)

        response = self.agent.invoke(
            {"messages": [HumanMessage(f"{query}")]},
            {"configurable": {"thread_id": thread_id}}
        )

        return response

