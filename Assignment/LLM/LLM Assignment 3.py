import json
import re
import logging
import requests
import urllib3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. MODULAR CONFIGURATION & API CLIENTS
LLAMA_BASE_URL = "https://aimodels.jadeglobal.com:8082/ollama/api"
LLAMA_VERIFY_SSL = False
JADE_API_KEY = "YOUR_INTERNAL_BEARER_TOKEN_HERE" 

class CompanyLLMClient:
    """Handles independent interactions with specific models on the company server."""
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        url = f"{LLAMA_BASE_URL}/chat"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {JADE_API_KEY}"
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }
        
        # Log the outgoing prompt payload
        logging.info(f"[{self.model_name}] Outgoing Prompt Content: {user_prompt[:100]}...")
        
        try:
            response = requests.post(
                url, headers=headers, data=json.dumps(payload), 
                verify=LLAMA_VERIFY_SSL, timeout=120
            )
            response.raise_for_status()
            result = response.json()
            raw_output = result["message"]["content"].strip()
            
            # Log the raw text output received
            logging.info(f"[{self.model_name}] Raw Output Received.")
            return raw_output
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API failure for model {self.model_name}: {str(e)}")



# 2. PROMPT CONSTRUCTION LOGIC
class PromptFactory:
    """Centralizes structural prompt engineering templates."""
    @staticmethod
    def get_system_prompt() -> str:
        return "You are a professional research AI. Keep your points precise, analytical, and highly articulate."

    @staticmethod
    def turn_1_model_a(topic: str) -> str:
        return f"State your core arguments, explanation, or position regarding the topic: '{topic}'."

    @staticmethod
    def turn_2_model_b(topic: str, model_a_response: str) -> str:
        return (
            f"Regarding the topic '{topic}', critique, question, or expand upon the "
            f"following position provided by Model A:\n\n\"{model_a_response}\""
        )

    @staticmethod
    def turn_3_model_a(topic: str, model_b_critique: str) -> str:
        return (
            f"Regarding the topic '{topic}', provide a definitive final reply or counter-argument "
            f"defending or adapting your initial position against this critique from Model B:\n\n\"{model_b_critique}\""
        )

    @staticmethod
    def final_synthesis(topic: str, a1: str, b2: str, a3: str) -> str:
        return (
            f"Review this entire discussion transcript concerning '{topic}':\n"
            f"Model A Initial: {a1}\nModel B Critique: {b2}\nModel A Reply: {a3}\n\n"
            f"Generate a short, completely neutral, and objective synthesized conclusion based on the debate."
        )


# 3. RESPONSE PARSING & TOPIC VALIDATION
class Guardrails:
    """Validates structural data safety and relevant topic mapping."""
    @staticmethod
    def validate_relevance(response: str, topic: str) -> bool:
        """Heuristic check ensuring key terminology overlapping to prevent hallucinations."""
        topic_words = set(re.findall(r'\w+', topic.lower()))
        response_words = set(re.findall(r'\w+', response.lower()))
        # Ensure at least one distinct context root keyword is matched
        meaningful_words = {w for w in topic_words if len(w) > 3}
        return bool(meaningful_words.intersection(response_words))


# 4. INTERACTION ORCHESTRATION ENGINE
class OrchestratorPipeline:
    """Manages the full multi-turn execution flow between Model A and Model B."""
    def __init__(self, token_ready: bool = True):
        self.client_a = CompanyLLMClient("llama3.1:8b")
        self.client_b = CompanyLLMClient("deepseek-coder:6.7b")

    def execute_discussion(self, topic: str) -> str:
        try:
            # --- TURN 1: Model A ---
            prompt_a1 = PromptFactory.turn_1_model_a(topic)
            response_a1 = self.client_a.generate_response(PromptFactory.get_system_prompt(), prompt_a1)
            if not Guardrails.validate_relevance(response_a1, topic):
                raise ValueError("Model A Turn 1 response failed topic relevance check.")

            # --- TURN 2: Model B ---
            prompt_b2 = PromptFactory.turn_2_model_b(topic, response_a1)
            response_b2 = self.client_b.generate_response(PromptFactory.get_system_prompt(), prompt_b2)
            if not Guardrails.validate_relevance(response_b2, topic):
                raise ValueError("Model B Turn 2 response failed topic relevance check.")

            # --- TURN 3: Model A ---
            prompt_a3 = PromptFactory.turn_3_model_a(topic, response_b2)
            response_a3 = self.client_a.generate_response(PromptFactory.get_system_prompt(), prompt_a3)
            if not Guardrails.validate_relevance(response_a3, topic):
                raise ValueError("Model A Turn 3 response failed topic relevance check.")

            # --- SYNTHESIS TURN: Executed on Model B for neutrality ---
            prompt_synth = PromptFactory.final_synthesis(topic, response_a1, response_b2, response_a3)
            synthesized_conclusion = self.client_b.generate_response(
                "You are an objective third-party summary system.", prompt_synth
            )

            # Assemble clean final structured map
            output_json = {
                "topic": topic,
                "model_a_initial_response": response_a1,
                "model_b_critique": response_b2,
                "model_a_final_reply": response_a3,
                "synthesized_conclusion": synthesized_conclusion
            }
            return json.dumps(output_json, indent=4)

        except Exception as err:
            # Gracefully wrap execution framework exceptions into strict JSON schemas
            error_json = {
                "error": "The pipeline encountered a system runtime failure.",
                "details": str(err)
            }
            return json.dumps(error_json, indent=4)


# 5. RUNTIME INTERACTIVE ENTRYPOINT
if __name__ == "__main__":
    user_topic = "The adoption of asynchronous core hours over traditional work days"
    
    print("Initiating Multi-Model Structured Discussion...")
    orchestrator = OrchestratorPipeline()
    
    final_output = orchestrator.execute_discussion(user_topic)
    
    print("\n================ SYSTEM RESULT (STRICT JSON) ================")
    print(final_output)
    print("=============================================================")