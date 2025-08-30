from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory


from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

from models import llm_model
from output_parser import CustomOutputParser
from prompt import chat_prompt

class AgentHandler:
    def __init__(self, tools):
        self.llm = llm_model
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            prompt= chat_prompt,
            verbose=True,
            handle_parsing_errors= True,
            output_parser=CustomOutputParser()  
            
        )

    def run(self, query):
        return self.agent.invoke(query)

