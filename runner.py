import time
import traceback
from vector_db_handler import VectorDBHandler

class AgentRunner:
    def __init__(self, agent, ltmem=None):
        self.agent = agent
        self.ltmem = ltmem or VectorDBHandler()

    def ask(self, query: str, max_retries: int = 2):
        history_notes = []
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    self.agent.memory.chat_memory.add_ai_message(
                        f"Previous attempt failed. Retry #{attempt + 1}."
                    )
                out = self.agent.invoke({"input": query})
                text = out.get("output") if isinstance(out, dict) else str(out)
                self.ltmem.add_note(f"Q: {query}\\nA: {text}", kind="qa")
                return text
            except Exception as e:
                err = f"Agent error on attempt {attempt+1}: {e}\\n{traceback.format_exc()}"
                history_notes.append(err)
                time.sleep(0.3)

        self.ltmem.add_note("\\n\\n".join(history_notes), kind="error")
        return "Sorry, I couldn't complete the task after multiple attempts."
    