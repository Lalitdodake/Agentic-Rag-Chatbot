from langchain.agents import create_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.messages import  HumanMessage
from langgraph.checkpoint.memory import InMemorySaver


from models import llm_model
# from output_parser import CustomOutputParser
from prompt import chat_prompt


_store = {}

def get_session_history(session_id: str):
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


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



    def run(self, query, config):
        print("USER QUERY====", query)
        return self.agent.invoke(
            {"messages": [HumanMessage(f"{query}")]},
            {"configurable": {"thread_id": "1"}}
        )

