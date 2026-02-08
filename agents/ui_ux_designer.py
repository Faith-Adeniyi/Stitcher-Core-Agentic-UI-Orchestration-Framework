import json
import os
import logging
import asyncio
import datetime
from ollama import AsyncClient

class UIDesigner:
    """
    COGNITIVE DESIGN LAYER:
    Handles brand-to-visual translation with Asynchronous Parallelism, 
    Agentic Self-Healing, and Cognitive Trace Logging for auditability.
    """
    def __init__(self, manifest_path="project_manifest.json"):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
        except FileNotFoundError:
            logging.error(f"UI_UX_AGENT: {manifest_path} missing. Using defaults.")
            self.manifest = {"vibe": "Cyber-Industrial"}
        
        self.model = self.manifest.get("writing_model", "llama3.2:1b")
        self.design_memory_path = "data/current_design_tokens.json"
        self.trace_path = "data/cognitive_trace.json"

    def _log_cognitive_trace(self, event_type, details):
        """
        Observability Layer: Logs the AI's internal reasoning and decision-making process.
        """
        os.makedirs("data", exist_ok=True)
        trace_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "agent": "UI_UX_DESIGNER",
            "event": event_type,
            "details": details
        }
        
        try:
            trace_data = []
            if os.path.exists(self.trace_path):
                with open(self.trace_path, 'r', encoding='utf-8') as f:
                    trace_data = json.load(f)
            
            trace_data.append(trace_entry)
            with open(self.trace_path, 'w', encoding='utf-8') as f:
                json.dump(trace_data, f, indent=4)
        except Exception as e:
            logging.error(f"UI_UX_AGENT: Trace logging failed: {e}")

    def perform_competitive_research(self, niche_context):
        """
        Agentic Self-Improvement: Scours niche trends to guide the design.
        """
        logging.info(f"UI_UX_AGENT: Researching design patterns for: {niche_context}")
        
        research_prompt = f"""
        ACT AS: UI/UX Market Researcher.
        NICHE: {niche_context}
        TASK: Identify 2026 high-converting design trends.
        Return a concise summary and reasoning.
        """
        
        import ollama
        try:
            response = ollama.generate(model=self.model, prompt=research_prompt)
            insight = response['response']
            self._log_cognitive_trace("MARKET_RESEARCH", {"niche": niche_context, "insight": insight})
            return insight
        except Exception as e:
            logging.error(f"UI_UX_AGENT: Research failed: {e}")
            return "Standard modern professional layouts."

    async def _generate_single_variant_task(self, variant_id, research_context, retry_count=0):
        """
        INTERNAL ASYNC TASK: Generates one direction with a Self-Healing loop.
        """
        vibe = self.manifest.get('vibe', 'Cyber-Industrial')
        
        prompt = f"""
        ACT AS: Senior UI/UX Consultant.
        VARIANT_NUMBER: {variant_id}
        BRAND_VIBE: {vibe}
        {research_context}
        
        TASK: Generate ONE unique UI design variation.
        REQUIREMENTS:
        - Return ONLY a valid JSON object.
        - Structure: {{"variant_name": "STR", "colors": {{"primary": "HEX", "secondary": "HEX", "bg": "HEX"}}, "typography": {{"heading": "STR", "body": "STR"}}, "border_radius": "STR"}}
        """
        
        try:
            response = await AsyncClient().generate(model=self.model, prompt=prompt)
            raw_content = response['response'].strip()
            
            try:
                data = json.loads(raw_content)
                self._log_cognitive_trace("VARIANT_SYNTHESIS", {"id": variant_id, "status": "SUCCESS", "variant": data.get("variant_name")})
                return data
            except json.JSONDecodeError as e:
                if retry_count < 2:
                    logging.warning(f"UI_UX_AGENT: Variant {variant_id} JSON corrupt. Healing attempt {retry_count + 1}...")
                    self._log_cognitive_trace("SELF_HEALING_TRIGGER", {"id": variant_id, "error": str(e)})
                    return await self._fix_json_output(raw_content, str(e), variant_id, research_context, retry_count + 1)
                raise e

        except Exception as e:
            logging.error(f"UI_UX_AGENT: Async variant {variant_id} failed: {e}")
            return self._get_fallback_variants()[variant_id % 5]

    async def _fix_json_output(self, bad_json, error_msg, variant_id, context, retry_count):
        """
        AGENTIC TUTOR LOGIC: Feeds the error back to the model for correction.
        """
        repair_prompt = (
            f"Your previous JSON for variant {variant_id} failed parsing.\n"
            f"ERROR: {error_msg}\n"
            f"BAD_OUTPUT: {bad_json}\n"
            "FIX: Return ONLY the corrected JSON object."
        )
        try:
            response = await AsyncClient().generate(model=self.model, prompt=repair_prompt)
            fixed_data = json.loads(response['response'].strip())
            self._log_cognitive_trace("SELF_HEALING_SUCCESS", {"id": variant_id, "attempt": retry_count})
            return fixed_data
        except:
            return self._get_fallback_variants()[variant_id % 5]

    async def generate_variants_async(self, count=5, research_insights=None):
        """
        HIGH-CONCURRENCY GENERATION: Runs multiple AI thoughts in parallel.
        """
        logging.info(f"UI_UX_AGENT: Initiating parallel synthesis of {count} variants...")
        research_context = f"RESEARCH_INSIGHTS: {research_insights}" if research_insights else ""
        
        tasks = [self._generate_single_variant_task(i + 1, research_context) for i in range(count)]
        variants = await asyncio.gather(*tasks)
        
        logging.info(f"UI_UX_AGENT: Parallel synthesis complete.")
        return variants

    def ingest_external_reference(self, reference_url):
        """Human-in-the-loop override for Figma/URL references."""
        logging.info(f"UI_UX_AGENT: Processing human designer reference: {reference_url}")
        self._log_cognitive_trace("HUMAN_OVERRIDE", {"reference": reference_url})
        return {
            "variant_name": "Human_Selection_Override",
            "colors": {"primary": "FOLLOW_LINK", "secondary": "FOLLOW_LINK", "bg": "FOLLOW_LINK"},
            "typography": {"heading": "REPLICATE_REFERENCE", "body": "REPLICATE_REFERENCE"},
            "border_radius": "MATCH_REFERENCE",
            "external_link": reference_url
        }

    def save_selected_design(self, design_tokens):
        os.makedirs("data", exist_ok=True)
        try:
            with open(self.design_memory_path, 'w', encoding='utf-8') as f:
                json.dump(design_tokens, f, indent=4)
            logging.info("UI_UX_AGENT: Design tokens persisted.")
            self._log_cognitive_trace("SELECTION_PERSISTED", {"variant": design_tokens.get("variant_name")})
        except Exception as e:
            logging.error(f"UI_UX_AGENT: Persistence failure: {e}")

    def load_cached_design(self):
        if os.path.exists(self.design_memory_path):
            with open(self.design_memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_fallback_variants()[0]

    def _get_fallback_variants(self):
        """Ensures 5 distinct fallbacks are available if the AI is offline."""
        return [{
            "variant_name": f"Stable_Default_{i}",
            "colors": {"primary": "#00FF41", "secondary": "#1A1A1A", "bg": "#0D0D0D"},
            "typography": {"heading": "JetBrains Mono", "body": "Inter"},
            "border_radius": "4px"
        } for i in range(5)]