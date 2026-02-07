import json
import os
import ollama
import logging

class UIOrchestrator:
    """
    COGNITIVE ORCHESTRATION LAYER:
    Utilizes a dual-model inference strategy to separate architectural reasoning 
    from narrative brand development.
    """
    def __init__(self, config=None, manifest_path="project_manifest.json"):
        """
        Initializes the Orchestrator utilizing configurations from the global manifest.
        """
        self.logger = logging.getLogger("StitcherCore.Orchestrator")
        
        # Load from manifest if no specific config is injected
        if config is None and os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    full_manifest = json.load(f)
                    self.config = full_manifest.get("orchestrator_settings", {})
            except Exception as e:
                self.logger.error(f"ORCHESTRATOR: Manifest load failure: {e}")
                self.config = {}
        else:
            self.config = config or {}

        # Dual-Model Mapping
        self.coder_model = self.config.get("model", "qwen2.5-coder:7b")
        self.writer_model = self.config.get("writing_model", "llama3.2:1b")
        
        self.available_components = self.config.get("available_components", ["hero", "footer"])
        self.role = self.config.get("role", "Web Architect")
        
        self.system_prompt = (
            f"You are a {self.role}. Return a structured JSON plan for a website layout. "
            f"Utilize only these components: {self.available_components}."
        )

    def generate_plan(self, brand_data, design_tokens):
        """
        Analyzes brand intelligence alongside design constraints 
        to architect a structural layout plan.
        """

        self.logger.info(f"ORCHESTRATOR: Initiating structural inference via {self.coder_model}")
        
        prompt = (
            f"Contextual Business Data: {json.dumps(brand_data)}\n"
            "Requirement: Return a JSON array representing the sequential order of UI components.\n"
            f"Format: ['component1', 'component2', ...]"
        )

        try:
            response = ollama.generate(
                model=self.coder_model,
                system=self.system_prompt,
                prompt=prompt,
                format="json"
            )
            
            plan = json.loads(response.get('response', '[]'))
            
            if not isinstance(plan, list):
                raise ValueError("Inference returned non-list structure.")
                
            self.logger.info(f"ORCHESTRATOR: Design blueprint finalized: {plan}")
            return plan

        except Exception as e:
            self.logger.error(f"ORCHESTRATOR: Structural inference failure: {e}")
            return [self.available_components[0], self.available_components[-1]]

    def refine_copy(self, raw_text):
        """
        Uses the specialized WRITER model to professionalize brand narratives.
        """
        self.logger.info(f"ORCHESTRATOR: Refining narrative via {self.writer_model}")
        try:
            response = ollama.generate(
                model=self.writer_model,
                prompt=f"Rewrite the following for a senior AI Engineer portfolio. Keep it concise: {raw_text}"
            )
            return response['response']
        except Exception as e:
            self.logger.error(f"ORCHESTRATOR: Narrative refinement failure: {e}")
            return raw_text

if __name__ == "__main__":
    """
    INTERNAL MODULE VALIDATION:
    Tests the dual-model routing logic using default manifest settings.
    """
    orchestrator = UIOrchestrator()
    sample_data = {"brand": "Stitcher-Core", "niche": "Agentic AI"}
    
    # Test Coder Model
    test_plan = orchestrator.generate_plan(sample_data)
    print(f"Coder Plan: {test_plan}")
    
    # Test Writer Model
    test_copy = orchestrator.refine_copy("I build cool AI things with python.")
    print(f"Writer Refinement: {test_copy}")