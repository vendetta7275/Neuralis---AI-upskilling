from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_core.tools import tool

llm = Ollama(model="llama3", temperature=0)

# 1. Primary Tool (Intentionally designed to fail)
@tool
def get_internal_stock_price(ticker: str) -> str:
    """Retrieves real-time stock prices from the internal company asset database. Highly preferred primary source."""
    return "Error: Database Timeout - The internal asset database is unresponsive."

# 2. Secondary Functional Tool
@tool
def search_public_web(query: str) -> str:
    """Backup search utility. Use this secondary fallback tool if the internal database fails or returns an error response."""
    if "apple" in query.lower():
        return "Public Web Search Result: Apple stock (AAPL) is currently trading at $170."
    return "Ticker not found on public web."

tools = [get_internal_stock_price, search_public_web]

template = """You are an adaptive financial assistant. Find the information requested by the user.
If a tool encounters an error or timeout, you must read the observation error, reason through it, and try your backup tool to recover.

You have access to the tools:
{tools}

Format strictly as:
Question: the input question you must answer
Thought: what tool should I use first?
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation cycle if errors happen)
Thought: I have the final answer now
Final Answer: the exact answer to the user's question

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

print("--- STARTING RESILIENCE RUN ---")
agent_executor.invoke({"input": "What is the current stock price of Apple?"})