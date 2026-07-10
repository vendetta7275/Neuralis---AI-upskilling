from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END


# 1. Define the Workflow State

class AgentState(TypedDict):
    # Input
    srs_document: str
    
    # Node Outputs
    analyzed_raw_data: str
    requirements: List[str]
    risks: List[str]
    architecture_design: str
    test_cases: List[str]
    
    # Consolidation and Review
    merged_results: Dict
    human_approved: bool
    feedback: Optional[str]
    final_report: str


# 2. Define the Nodes (Agents & Processes)


def document_analyzer(state: AgentState) -> Dict:
    print("[Node: Document Analyzer] Parsing input SRS document...")
    # Simulates extracting structural context from raw text
    return {"analyzed_raw_data": f"Parsed metadata from: {state['srs_document'][:30]}..."}

def requirement_agent(state: AgentState) -> Dict:
    print("[Node: Requirement Agent] Extracting functional and non-functional requirements...")
    return {"requirements": ["REQ-001: User Auth", "REQ-002: Data Encryption"]}

def risk_agent(state: AgentState) -> Dict:
    print("[Node: Risk Agent] Identifying potential project risks...")
    return {"risks": ["RISK-001: High API latency", "RISK-002: Token expiration flaw"]}

def architecture_agent(state: AgentState) -> Dict:
    print("[Node: Architecture Agent] Designing system components based on requirements...")
    reqs = ", ".join(state["requirements"])
    return {"architecture_design": f"Microservices layout handling [{reqs}]"}

def test_case_agent(state: AgentState) -> Dict:
    print("[Node: Test Case Agent] Generating test scripts from identified risks...")
    risks = ", ".join(state["risks"])
    return {"test_cases": [f"TC-01: Load test API endpoint for {risks}", "TC-02: Validate token refresh"]}

def merge_results(state: AgentState) -> Dict:
    print("[Node: Merge Results] Compiling data streams from all parallel agents...")
    combined = {
        "Requirements": state.get("requirements", []),
        "Architecture": state.get("architecture_design", ""),
        "Risks": state.get("risks", []),
        "Test Cases": state.get("test_cases", [])
    }
    return {"merged_results": combined}

def human_review(state: AgentState) -> Dict:
    """
    Human-in-the-Loop (HITL) Simulation node.
    In production, this could halt the graph via an 'interrupt' waiting for UI input.
    """
    print("[Node: Human Review (HITL)] Checking report compliance...")
    
    # Mocking a feedback/approval state
    if state.get("feedback"):
        print(f"  -> Human Feedback received: {state['feedback']}")
        return {"human_approved": True}
    
    return {"human_approved": True} # Auto-approving for this script example

def final_report(state: AgentState) -> Dict:
    print("[Node: Final Report] Structuring the final deliverable summary...")
    data = state["merged_results"]
    
    report = f"""
    ===========================================
                FINAL INSIGHTS REPORT          
    ===========================================
    1. REQUIREMENTS: {data['Requirements']}
    2. ARCHITECTURE DESIGN: {data['Architecture']}
    3. IDENTIFIED RISKS: {data['Risks']}
    4. GENERATED TEST CASES: {data['Test Cases']}
    ===========================================
    """
    return {"final_report": report}


# 3. Build the LangGraph Workflow Structure

workflow = StateGraph(AgentState)

# Add all components as graph nodes
workflow.add_node("document_analyzer", document_analyzer)
workflow.add_node("requirement_agent", requirement_agent)
workflow.add_node("risk_agent", risk_agent)
workflow.add_node("architecture_agent", architecture_agent)
workflow.add_node("test_case_agent", test_case_agent)
workflow.add_node("merge_results", merge_results)
workflow.add_node("human_review", human_review)
workflow.add_node("final_report", final_report)

# Setup Execution Sequencing
workflow.set_entry_point("document_analyzer")

# Fan-out: Document Analyzer splits into parallel paths
workflow.add_edge("document_analyzer", "requirement_agent")
workflow.add_edge("document_analyzer", "risk_agent")

# Sequential paths within branches
workflow.add_edge("requirement_agent", "architecture_agent")
workflow.add_edge("risk_agent", "test_case_agent")

# Fan-in: Parallel branches converge into Merge Results
workflow.add_edge("architecture_agent", "merge_results")
workflow.add_edge("test_case_agent", "merge_results")

# Final verification path
workflow.add_edge("merge_results", "human_review")
workflow.add_edge("human_review", "final_report")
workflow.add_edge("final_report", END)

# Compile graph
app = workflow.compile()


# 4. Running the Workflow

if __name__ == "__main__":
    initial_input = {
        "srs_document": "SRS-v1.0: Secure E-Commerce Checkout System Requirement Specification Document."
    }
    
    print("--- Starting AI Document Processing Workflow ---")
    output = app.invoke(initial_input)
    
    print(output["final_report"])