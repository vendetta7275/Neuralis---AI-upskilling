from typing import Dict, TypedDict, Literal
from langgraph.graph import StateGraph, END


# 1. Define the Workflow State

class ExpenseState(TypedDict):
    initial_amount_usd: float
    amount_with_tax_usd: float
    amount_inr: float
    route: str
    decision: str


# 2. Define the Nodes (Processing Steps)


def calculate_tax(state: ExpenseState) -> Dict:
    """Adds 10% tax to the initial USD amount."""
    usd_amount = state["initial_amount_usd"]
    amount_with_tax = usd_amount * 1.10
    print(f"[Node: Calculate Tax] Initial: ${usd_amount:.2f} -> With Tax: ${amount_with_tax:.2f}")
    return {"amount_with_tax_usd": amount_with_tax}

def convert_to_inr(state: ExpenseState) -> Dict:
    """Converts the USD amount (with tax) to INR. (Using a mock rate of 1 USD = 85 INR)"""
    usd_amount = state["amount_with_tax_usd"]
    exchange_rate = 85.0  
    inr_amount = usd_amount * exchange_rate
    print(f"[Node: Convert to INR] ${usd_amount:.2f} USD = ₹{inr_amount:.2f} INR")
    return {"amount_inr": inr_amount}

# Approval Team Nodes
def auto_approve(state: ExpenseState) -> Dict:
    return {"decision": f"Auto-Approved. Processed amount: ₹{state['amount_inr']:.2f} INR"}

def manager_approve(state: ExpenseState) -> Dict:
    return {"decision": f"Sent to Manager for Approval. Processed amount: ₹{state['amount_inr']:.2f} INR"}

def finance_approve(state: ExpenseState) -> Dict:
    return {"decision": f"Sent to Finance Department for Review. Processed amount: ₹{state['amount_inr']:.2f} INR"}


# 3. Define the Conditional Routing Logic

def route_expense(state: ExpenseState) -> Literal["auto", "manager", "finance"]:
    """Routes the workflow based on the INITIAL USD amount as requested."""
    amount = state["initial_amount_usd"]
    
    if amount <= 100:
        return "auto"
    elif 100 < amount <= 1000:
        return "manager"
    else:
        return "finance"


# 4. Build the LangGraph Workflow

workflow = StateGraph(ExpenseState)

# Add nodes to the graph
workflow.add_node("calculate_tax", calculate_tax)
workflow.add_node("convert_to_inr", convert_to_inr)
workflow.add_node("auto_approve", auto_approve)
workflow.add_node("manager_approve", manager_approve)
workflow.add_node("finance_approve", finance_approve)

# Define execution flow dependencies
workflow.set_entry_point("calculate_tax")
workflow.add_edge("calculate_tax", "convert_to_inr")

# Add conditional routing after currency conversion
workflow.add_conditional_edges(
    "convert_to_inr",
    route_expense,
    {
        "auto": "auto_approve",
        "manager": "manager_approve",
        "finance": "finance_approve"
    }
)

# Connect approval endpoints to the END of the workflow
workflow.add_edge("auto_approve", END)
workflow.add_edge("manager_approve", END)
workflow.add_edge("finance_approve", END)

# Compile the graph
app = workflow.compile()


# 5. Testing the Workflow

def process_expense(usd_amount: float):
    print(f"\n--- Processing Expense: ${usd_amount} USD ---")
    initial_state = {"initial_amount_usd": usd_amount}
    
    # Run the graph
    final_output = app.invoke(initial_state)
    
    # Print the final mandated requirements
    print("\n--- Final Summary ---")
    print(f"Final Decision: {final_output['decision']}")
    print(f"Converted Amount: ₹{final_output['amount_inr']:.2f} INR")
    print("-" * 40)

# Run test cases covering all 3 routing conditions
if __name__ == "__main__":
    process_expense(50)    # Should trigger Auto Approval
    process_expense(500)   # Should trigger Manager Approval
    process_expense(1500)  # Should trigger Finance Approval