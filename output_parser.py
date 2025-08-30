import re
from langchain.schema import AgentFinish, AgentAction
from langchain.agents import AgentOutputParser

class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str):
        llm_output = llm_output.strip()
        print("LLM OUTPUT>>>>>>>>..", llm_output)
        
        final_match = re.search(r"Final Answer\s*:\s*(.*)", llm_output, re.DOTALL | re.IGNORECASE)
        if final_match:
            return AgentFinish(
                return_values={"output": final_match.group(1).strip()},
                log=llm_output
            )

        
        obs_match = re.search(r"Observation\s*:\s*(.*)", llm_output, re.DOTALL | re.IGNORECASE)
        if obs_match:
            return AgentFinish(
                return_values={"output": obs_match.group(1).strip()},
                log=llm_output
            )

        
        return AgentFinish(
            return_values={"output": llm_output},
            log=llm_output
        )
