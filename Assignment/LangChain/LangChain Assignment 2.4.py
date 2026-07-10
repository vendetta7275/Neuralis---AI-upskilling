from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# 1. Initialize Local Components & Cache
llm = Ollama(model="llama3", temperature=0)
query_cache = {}

# Strict grounding system prompt setup
grounding_prompt = PromptTemplate.from_template(
    "System: You are an AI assistant that answers questions based solely on the Context provided. "
    "If the answer cannot be confidently found within the context, you MUST reply with exactly "
    "\"I do not have enough information\". Do not extrapolate or use external facts.\n"
    "Context: {context}\n"
    "Question: {question}\n"
    "Answer:"
)

# 2. Optimized Execution Layer with Caching
def process_request(question: str, context: str) -> str:
    # 1. Latency Component: Check if it exists in cache
    if question in query_cache:
        return f"Returned from Cache: {query_cache[question]}"
    
    # 2. Generate and store if it does not exist
    chain = grounding_prompt | llm
    response = chain.invoke({"context": context, "question": question}).strip()
    
    # Cache the result
    query_cache[question] = response
    return response

# Test parameters
shared_context = "The corporate office headquarters are located in New York City. Operating hours are from 9 AM to 5 PM EST."

print("--- Fast & Grounded System Output Scenarios ---")

# Scenario 1 (First Ask)
print("\n● Scenario 1 (First Ask):")
ans1 = process_request("Where are the corporate headquarters located?", shared_context)
print(f"LLM Response: {ans1}")

# Scenario 2 (Cache Hit)
print("\n● Scenario 2 (Cache Hit):")
ans2 = process_request("Where are the corporate headquarters located?", shared_context)
print(f"{ans2}")

# Scenario 3 (Grounding Test)
print("\n● Scenario 3 (Grounding Test):")
ans3 = process_request("What is the recipe for a chocolate cake?", shared_context)
print(f"LLM Response: {ans3}")