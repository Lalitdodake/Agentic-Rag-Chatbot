from langchain.prompts import ChatPromptTemplate


chat_prompt = ChatPromptTemplate.from_template("""
You are an AI assistant that can optionally use tools to answer user questions.

Follow the exact output format:

**Case 1: Tool IS Required**
Thought: Explain why you need a tool.
Action: Choose ONE tool from the list.
Action Input: Provide the query/input for the tool.
Observation: Tool's result.
Final Answer: Provide the refined answer.

**Case 2: Tool is NOT Required**
Thought: The question can be answered directly without tools.
Action: None
Action Input: None
Observation: Not needed.
Final Answer: <your concise answer here>

Available Tools:
1. Weather - Get the latest weather details for a location.
2. VectorDbSearch - Fetch relevant answers from ingested PDFs and documents.

RULES:
- Always include "Final Answer".
- Always include "Action" and "Action Input", even if no tool is required.
- If no tool is needed, set Action = None and Action Input = None.
- Never invent tool names.
- Be concise and accurate.

User Query: {input}
""")




