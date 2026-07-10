from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_core.tools import tool

# Initialize local LLM
llm = Ollama(model="llama3", temperature=0)

# Define Custom Tools with Highly Explicit Docstrings
@tool
def refund_order(transaction_id: str) -> str:
    """
    USE THIS TOOL ONLY WHEN the user wants to get their money back for a past transaction, 
    reverses a previous charge, or explicitly mentions an issue with an existing transaction ID.
    DO NOT use this if the user wants to cancel or stop future billing.
    """
    return f"Success: Refund initiated for Transaction ID {transaction_id}."

@tool
def cancel_subscription(email: str) -> str:
    """
    USE THIS TOOL ONLY WHEN the user wants to stop future recurring charges, cancel their 
    active membership, close an account, or prevent a software platform from taking money again.
    DO NOT use this tool if the user is asking for money back for a past charge.
    """
    return f"Success: Subscription successfully canceled for account associated with {email}."

tools = [refund_order, cancel_subscription]

# Prompt engineering for strict ReAct enforcement
template = """You are a SaaS billing support routing agent. Route the user's request to the correct tool based strictly on their intent as described in the tool documentation.

You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: determine which tool perfectly matches the user intent based on the docstring parameters
Action: the action to take, must be one of [{tool_names}]
Action Input: the extracted parameter value (email address or transaction ID string)
Observation: the result of the action
Thought: I have successfully completed the routing action
Final Answer: The result returned by the chosen tool.

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- Verification Test Cases ---
print("--- TEST CASE 1: CANCEL INFERENCE ---")
agent_executor.invoke({"input": "I don't want to use your software anymore, stop charging john@email.com."})

print("\n--- TEST CASE 2: REFUND INFERENCE ---")
agent_executor.invoke({"input": "My last charge of $50 on ID #TXN991 was a mistake, give it back."})