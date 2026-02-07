import json
import os
import logging
import ollama

class UIDesigner:
    """
    COGNITIVE DESIGN LAYER:
    Responsible for brand-to-visual translation. Generates multiple design 
    variations, performs competitive niche research, and manages human 
    designer overrides (e.g., Figma references).
    """
    def __init__(self, manifest_path="project_manifest.json"):
        """
        Initializes the designer with manifest configurations and local cache paths.
        """
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
        except FileNotFoundError:
            logging.error(f"UI_UX_AGENT: {manifest_path} missing. Initializing with defaults.")
            self.manifest = {"vibe": "Cyber-Industrial"}
        
        self.model = self.manifest.get("writing_model", "llama3.2:1b")
        self.design_memory_path = "data/current_design_tokens.json"

    def perform_competitive_research(self, niche_context):
        """
        Agentic Self-Improvement: Scours niche-specific trends to ensure 
        generated designs are competitive and industry-aligned.
        """
        logging.info(f"UI_UX_AGENT: Researching competitive design patterns for: {niche_context}")
        
        research_prompt = f"""
        ACT AS: UI/UX Market Researcher.
        NICHE: {niche_context}
        TASK: Identify current (2026) high-converting design trends for this specific industry.
        Focus on: Color psychology, layout density, and modern typography choices.
        Return a concise summary for the design generator.
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=research_prompt)
            return response['response']
        except Exception as e:
            logging.error(f"UI_UX_AGENT: Competitive research failed: {e}")
            return "Standard modern professional layouts with high accessibility."

    def generate_variants(self, research_insights=None):
        """
        Executes a design reasoning cycle to produce 5 distinct visual 
        directions, incorporating competitive research if available.
        """
        logging.info(f"UI_UX_AGENT: Synthesizing 5 variants using {self.model}...")
        
        research_context = f"RESEARCH_INSIGHTS: {research_insights}" if research_insights else ""
        
        prompt = f"""
        ACT AS: Senior UI/UX Consultant.
        BRAND_VIBE: {self.manifest.get('vibe', 'Cyber-Industrial')}
        {research_context}
        
        TASK: Generate 5 distinct UI design variations.
        REQUIREMENTS:
        - Return a JSON list containing 5 objects.
        - Each object must include: 'variant_name', 'colors' (primary, secondary, bg), 
          'typography' (heading, body), and 'border_radius'.
        
        NOTE: Return ONLY valid JSON.
        """
        
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            variants = json.loads(response['response'])
            
            if isinstance(variants, list) and len(variants) >= 5:
                return variants[:5]
            else:
                raise ValueError("LLM returned malformed variant array.")
                
        except Exception as e:
            logging.error(f"UI_UX_AGENT: Multi-variant synthesis failure: {e}")
            return self._get_fallback_variants()

    def ingest_external_reference(self, reference_url):
        """
        Handles Human-in-the-loop overrides by creating design tokens 
        based on external references (Figma/Portfolio links).
        """
        logging.info(f"UI_UX_AGENT: Processing human designer reference: {reference_url}")
        
        # We create a specific token set that flags the engine to follow the URL vibe
        return {
            "variant_name": "Human_Selection_Override",
            "colors": {"primary": "FOLLOW_LINK", "secondary": "FOLLOW_LINK", "bg": "FOLLOW_LINK"},
            "typography": {"heading": "REPLICATE_REFERENCE", "body": "REPLICATE_REFERENCE"},
            "border_radius": "MATCH_REFERENCE",
            "external_link": reference_url
        }

    def save_selected_design(self, design_tokens):
        """
        Persists approved design tokens to local memory for resource management.
        """
        os.makedirs("data", exist_ok=True)
        try:
            with open(self.design_memory_path, 'w', encoding='utf-8') as f:
                json.dump(design_tokens, f, indent=4)
            logging.info("UI_UX_AGENT: Design tokens persisted for future iterations.")
        except Exception as e:
            logging.error(f"UI_UX_AGENT: Persistence failure: {e}")

    def load_cached_design(self):
        """
        Retrieves cached design tokens to bypass redundant compute cycles.
        """
        if os.path.exists(self.design_memory_path):
            logging.info("UI_UX_AGENT: Loading cached tokens from disk.")
            with open(self.design_memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return self._get_fallback_variants()[0]

    def _get_fallback_variants(self):
        """Standard fallback to ensure pipeline continuity."""
        return [{
            "variant_name": f"Stable_Default_{i}",
            "colors": {"primary": "#00FF41", "secondary": "#1A1A1A", "bg": "#0D0D0D"},
            "typography": {"heading": "JetBrains Mono", "body": "Inter"},
            "border_radius": "4px"
        } for i in range(5)]

if __name__ == "__main__":
    designer = UIDesigner()
    # Test the self-improvement research loop
    insights = designer.perform_competitive_research("Modern Fitness Gym")
    print(f"RESEARCH DEBUG: {insights[:100]}...")