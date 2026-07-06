import json
import re
import requests
import urllib3

# 1. JADE GLOBAL INTERNAL LLM CONFIGURATION
LLAMA_BASE_URL = "https://aimodels.jadeglobal.com:8082/ollama/api"
LLAMA_MODEL = "llama3.1:8b" 
LLAMA_VERIFY_SSL = False     

JADE_API_KEY = "YOUR_INTERNAL_BEARER_TOKEN_HERE" 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 2. INTERNAL API CLIENT FUNCTION WITH AUTHENTICATION
def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Sends payload to the Jade Global internal Ollama chat endpoint
    using authenticated Bearer tokens.
    """
    url = f"{LLAMA_BASE_URL}/chat"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JADE_API_KEY}"
    }
    
    payload = {
        "model": LLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            verify=LLAMA_VERIFY_SSL,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        return result["message"]["content"]
        
    except requests.exceptions.RequestException as e:
        return f"Error calling LLM API: {str(e)}"


# 3. PROCESSING PIPELINE WITH STRUCTURAL VALIDATION
def analyze_article_pipeline(article_content: str) -> dict:
    """
    Manages the prompt injection, executes the API request, isolates the 
    JSON block from the response, and programmatically validates constraints.
    """
    
    system_prompt = """You are a strict JSON extraction assistant. You must output a raw JSON object and nothing else.
Do not include any conversational introduction, markdown formatting blocks (like ```json), or trailing notes.

Your output must exactly match this JSON keys framework:
{
    "summary": "string (strictly under 150 words)",
    "important_points": ["string", "string", ... (must be between 5 and 10 points)],
    "key_themes": ["string", "string", ... (must be 3 to 5 short phrases, not full sentences)],
    "target_audience": "string"
}"""

    user_prompt = f"Analyze the following article according to the system rules:\n\n{article_content}"
    
    raw_response = call_llm(system_prompt, user_prompt)
    
    if raw_response.startswith("Error calling LLM API:"):
        return {"error": raw_response}
        
    try:
        clean_json_match = re.search(r'(\{.*})', raw_response, re.DOTALL)
        if clean_json_match:
            json_string = clean_json_match.group(1)
        else:
            json_string = raw_response

        data = json.loads(json_string)
        
        summary_word_count = len(data.get("summary", "").split())
        points_count = len(data.get("important_points", []))
        themes_count = len(data.get("key_themes", []))
        
        errors = []
        if summary_word_count > 150:
            errors.append(f"Summary exceeds word count limit ({summary_word_count}/150 words).")
        if not (5 <= points_count <= 10):
            errors.append(f"Important points count out of boundary ({points_count} items generated, required: 5-10).")
        if not (3 <= themes_count <= 5):
            errors.append(f"Key themes count out of boundary ({themes_count} items generated, required: 3-5).")
            
        if errors:
            return {
                "status": "malformed_constraints",
                "validation_errors": errors,
                "raw_data_received": data
            }
            
        return {"status": "success", "data": data}
        
    except json.JSONDecodeError:
        return {
            "status": "failed_to_parse_json",
            "error": "The response could not be structuralized into a valid JSON object.",
            "raw_llm_output": raw_response
        }


# 4. EXECUTION RUNTIME WITH MOCK DATA
if __name__ == "__main__":
    sample_article = """
    Remote work frameworks are undergoing a massive structural shift as global tech companies begin 
    implementing 'Core Collaboration Hours' instead of traditional 9-to-5 schedules. A study of 
    over 500 enterprises indicates that productivity metrics rise by 22% when employees choose their own 
    deep-work schedules, provided they overlap online with teammates for at least 3 hours daily. However, 
    this framework presents distinct challenges for HR managers tracking asynchronous output and maintaining 
    organizational culture across time zones. Security infrastructure also demands updates, as VPN endpoints 
    face scattered access logs. Moving forward, decentralized organizations will likely invest heavily in 
    automated collaboration tracking tools to bridge these operational gaps.
    """
    
    print(f"Connecting to internal LLM base: {LLAMA_BASE_URL}")
    print(f"Targeting model: {LLAMA_MODEL}...\n")
    
    pipeline_result = analyze_article_pipeline(sample_article)
    
    print(json.dumps(pipeline_result, indent=4))