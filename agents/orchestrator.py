import json
import ollama # Designed for 8GB RAM local inference
import logging

class UIOrchestrator:
    """
    COGNITIVE LAYER: The 'Brain' of Stitcher-Core.
    Uses local LLMs to reason through brand data and select 
    the optimal UI components and layout structure.
    """
    def __init__(self, model="llama3"):
        self.model = model
        self.system_prompt = (
            "You are a Senior Web Architect. Your task is to analyze business data "
            "and return a structured JSON plan for a website layout. "
            "Use only the provided component names: 'hero', 'pricing', 'features', 'footer'."
        )

    def generate_plan(self, brand_data):
        """
        Consults the Local LLM to decide which components 
        best represent the brand's services and 'vibe'.
        """
        logging.info(f"Orchestrator reasoning with {self.model}...")
        
        prompt = f"""
        Analyze this business data: {json.dumps(brand_data)}
        Return a JSON list of components in the order they should appear.
        Example: ["hero", "features", "pricing", "footer"]
        """

        try:
            # Running locally on 8GB RAM requires stream=False for stability
            response = ollama.generate(
                model=self.model,
                system=self.system_prompt,
                prompt=prompt,
                format="json" # Ensures we get a machine-readable plan
            )
            
            # Parsing the LLM decision
            plan = json.loads(response['response'])
            logging.info(f"Orchestrator Plan finalized: {plan}")
            return plan

        except Exception as e:
            logging.error(f"Orchestration Logic Failure: {e}")
            # Fallback Plan: Ensures system workability if LLM fails
            return ["hero", "pricing", "footer"]

if __name__ == "__main__":
    # Internal Test
    sample_data = {"brand": "Luxury Pet Spa", "vibe": "High-end"}
    brain = UIOrchestrator()
    print(brain.generate_plan(sample_data))
