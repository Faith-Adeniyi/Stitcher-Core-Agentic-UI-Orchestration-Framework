import json
import os
import ollama
import logging
from datetime import datetime

class UIOrchestrator:
    """
    COGNITIVE ORCHESTRATION LAYER:
    Utilizes a dual-model inference strategy with persistent state management.
    """
    def __init__(self, config=None, manifest_path="project_manifest.json"):
        self.logger = logging.getLogger("StitcherCore.Orchestrator")
        self.manifest_path = manifest_path
        
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

        self.coder_model = self.config.get("model", "qwen2.5-coder:7b")
        self.writer_model = self.config.get("writing_model", "llama3.2:1b")
        self.available_components = self.config.get("available_components", ["hero", "footer"])
        self.role = self.config.get("role", "Web Architect")
        
        # PERSISTENCE: Initialize Build State
        self.state_file = "data/build_state.json"
        self._ensure_state_exists()

    def _ensure_state_exists(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.state_file):
            with open(self.state_file, 'w') as f:
                json.dump({"completed_steps": [], "cached_plan": []}, f)

    def log_cognitive_trace(self, thought, decision):
        """TELEMETRY: Logs the AI reasoning process."""
        trace = {
            "timestamp": datetime.now().isoformat(),
            "model": self.coder_model,
            "thought": thought,
            "decision": decision
        }
        with open("data/cognitive_trace.json", "a") as f:
            f.write(json.dumps(trace) + "\n")

    def generate_plan(self, brand_data, design_tokens):
        self.logger.info(f"ORCHESTRATOR: Initiating structural inference via {self.coder_model}")
        
        # Check if we can skip this based on State
        with open(self.state_file, 'r') as f:
            state = json.load(f)
            if "ORCHESTRATION" in state["completed_steps"]:
                self.logger.info("STATE: Plan found in cache. Resuming...")
                return state["cached_plan"]

        prompt = (
            f"Contextual Business Data: {json.dumps(brand_data)}\n"
            "Requirement: Return a JSON array of UI components in sequential order.\n"
            f"Format: ['component1', 'component2', ...]"
        )

        try:
            response = ollama.generate(
                model=self.coder_model,
                system=f"You are a {self.role}. Components: {self.available_components}",
                prompt=prompt,
                format="json"
            )
            
            plan = json.loads(response.get('response', '[]'))
            self.log_cognitive_trace("Analyzing brand data for optimal layout flow.", f"Blueprint: {plan}")
            
            # Save to State
            state["completed_steps"].append("ORCHESTRATION")
            state["cached_plan"] = plan
            with open(self.state_file, 'w') as f:
                json.dump(state, f)
                
            return plan
        except Exception as e:
            self.logger.error(f"ORCHESTRATOR: Failure: {e}")
            return [self.available_components[0], self.available_components[-1]]

    def refine_copy(self, raw_text):
        try:
            response = ollama.generate(
                model=self.writer_model,
                prompt=f"Rewrite for a senior AI Engineer portfolio: {raw_text}"
            )
            return response['response']
        except Exception as e:
            return raw_text