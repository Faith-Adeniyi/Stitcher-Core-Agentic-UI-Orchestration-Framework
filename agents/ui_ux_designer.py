import json
import os
import logging
import asyncio
import datetime
from ollama import AsyncClient

class UIDesigner:
    """
    COGNITIVE DESIGN LAYER:
    Orchestrates brand-to-visual translation utilizing asynchronous parallelism,
    autonomous error recovery, and comprehensive trace logging for system auditability.
    """
    def __init__(self, manifest_path="project_manifest.json"):
        """
        Initializes the design engine with configuration parameters from the MANIFEST_PATH.
        """
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
        except FileNotFoundError:
            logging.error(f"UI_UX_AGENT: Configuration manifest {manifest_path} not found. Utilizing default parameters.")
            self.manifest = {"vibe": "Cyber-Industrial"}
        
        self.model = self.manifest.get("writing_model", "llama3.2:1b")
        self.design_memory_path = "data/current_design_tokens.json"
        self.trace_path = "data/cognitive_trace.json"

    def _log_cognitive_trace(self, event_type, details):
        """
        OBSERVABILITY LAYER:
        Maintains a serialized record of internal reasoning and state transitions.
        Ensures data integrity across disparate trace schemas (List vs. Dictionary).
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
                    content = json.load(f)
                    
                    if isinstance(content, dict) and "logs" in content:
                        trace_data = content["logs"]
                    elif isinstance(content, list):
                        trace_data = content
                    else:
                        trace_data = []

            trace_data.append(trace_entry)
            
            with open(self.trace_path, 'w', encoding='utf-8') as f:
                json.dump(trace_data, f, indent=4)
        except Exception as e:
            logging.error(f"UI_UX_AGENT: Cognitive trace synchronization failed: {e}")

    def perform_competitive_research(self, niche_context):
        """
        COMPETITIVE ANALYSIS:
        Retrieves contemporary design patterns and market trends to inform the generation phase.
        """
        logging.info(f"UI_UX_AGENT: Analyzing design paradigms for niche: {niche_context}")
        
        research_prompt = f"""
        ACT AS: UI/UX Market Analyst.
        NICHE: {niche_context}
        TASK: Synthesize 2026 high-conversion design trends for industrial/tech brands.
        Return a concise technical summary.
        """
        
        import ollama
        try:
            response = ollama.generate(model=self.model, prompt=research_prompt)
            insight = response['response']
            self._log_cognitive_trace("MARKET_RESEARCH_COMPLETE", {"niche": niche_context, "insight": insight})
            return insight
        except Exception as e:
            logging.error(f"UI_UX_AGENT: Competitive research phase failed: {e}")
            return "Professional modern-industrial layout with high-contrast neon accents and dark mode."

    async def _generate_single_variant_task(self, variant_id, research_context, retry_count=0):
        """
        ASYNC GENERATION UNIT:
        Executes a localized synthesis of a design variant with integrated recursive error handling.
        """
        vibe = self.manifest.get('vibe', 'Cyber-Industrial')
        
        prompt = f"""
        ACT AS: Principal UI/UX Architect.
        VARIANT_ID: {variant_id}
        DESIGN_SPECIFICATION: {vibe} (Bento Grid, Dark Mode, High Contrast)
        CONTEXT: {research_context}
        
        TASK: Generate a unique UI configuration in strict JSON format.
        SCHEMA: {{
            "variant_name": "STR", 
            "colors": {{
                "primary": "HEX", 
                "secondary": "HEX", 
                "bg": "#050505", 
                "text": "#FFFFFF"
            }}, 
            "typography": {{"heading": "JetBrains Mono", "body": "Inter"}}, 
            "border_radius": "2px"
        }}
        """
        
        try:
            response = await AsyncClient().generate(model=self.model, prompt=prompt)
            raw_content = response['response'].strip()
            
            try:
                data = json.loads(raw_content)
                self._log_cognitive_trace("SYNTHESIS_SUCCESS", {"id": variant_id, "variant": data.get("variant_name")})
                return data
            except json.JSONDecodeError as e:
                if retry_count < 2:
                    logging.warning(f"UI_UX_AGENT: Variant {variant_id} schema corruption. Recovery cycle {retry_count + 1}...")
                    return await self._fix_json_output(raw_content, str(e), variant_id, research_context, retry_count + 1)
                raise e

        except Exception as e:
            logging.error(f"UI_UX_AGENT: Asynchronous generation failed for variant {variant_id}: {e}")
            return self._get_fallback_variants()[variant_id % 5]

    async def _fix_json_output(self, bad_json, error_msg, variant_id, context, retry_count):
        """
        RECURSIVE REPAIR LOGIC:
        Analyzes malformed output and re-synthesizes a valid JSON object.
        """
        repair_prompt = (
            f"The following JSON payload for variant {variant_id} failed validation.\n"
            f"VALIDATION_ERROR: {error_msg}\n"
            f"MALFORMED_PAYLOAD: {bad_json}\n"
            "TASK: Re-generate and return ONLY the corrected JSON object."
        )
        try:
            response = await AsyncClient().generate(model=self.model, prompt=repair_prompt)
            fixed_data = json.loads(response['response'].strip())
            self._log_cognitive_trace("RECOVERY_SUCCESS", {"id": variant_id, "cycle": retry_count})
            return fixed_data
        except Exception:
            return self._get_fallback_variants()[variant_id % 5]

    async def generate_variants_async(self, count=5, research_insights=None):
        """
        CONCURRENT ORCHESTRATION:
        Manages the parallel execution of multiple design synthesis tasks.
        """
        logging.info(f"UI_UX_AGENT: Initiating concurrent synthesis of {count} design variants...")
        research_context = f"RESEARCH_INSIGHTS: {research_insights}" if research_insights else ""
        
        tasks = [self._generate_single_variant_task(i + 1, research_context) for i in range(count)]
        variants = await asyncio.gather(*tasks)
        
        logging.info("UI_UX_AGENT: Concurrent design synthesis finalized.")
        return variants

    def ingest_external_reference(self, reference_url):
        """
        REFERENCE INGESTION:
        Allows for manual injection of design specifications via external URI references.
        """
        logging.info(f"UI_UX_AGENT: Integrating external design reference: {reference_url}")
        self._log_cognitive_trace("EXTERNAL_REFERENCE_INJECTED", {"uri": reference_url})
        return {
            "variant_name": "External_Reference_Ingestion",
            "colors": {"primary": "#4ade80", "secondary": "#22c55e", "bg": "#050505", "text": "#ffffff"},
            "typography": {"heading": "JetBrains Mono", "body": "Inter"},
            "border_radius": "2px",
            "external_link": reference_url
        }

    def save_selected_design(self, design_tokens):
        """
        STATE PERSISTENCE:
        Serializes and commits the finalized design tokens to the local memory layer.
        """
        os.makedirs("data", exist_ok=True)
        try:
            with open(self.design_memory_path, 'w', encoding='utf-8') as f:
                json.dump(design_tokens, f, indent=4)
            logging.info("UI_UX_AGENT: Design tokens successfully persisted.")
            self._log_cognitive_trace("PERSISTENCE_COMPLETE", {"variant": design_tokens.get("variant_name")})
        except Exception as e:
            logging.error(f"UI_UX_AGENT: Failed to persist design state: {e}")

    def load_cached_design(self):
        """
        CACHE RETRIEVAL:
        Retrieves the most recent verified design configuration from persistence.
        """
        if os.path.exists(self.design_memory_path):
            with open(self.design_memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_fallback_variants()[0]

    def _get_fallback_variants(self):
        """
        FAILSAFE REDUNDANCY:
        Provides validated default configurations in the event of upstream model failure.
        """
        return [{
            "variant_name": f"Industrial_Standard_Backup_{i}",
            "colors": {"primary": "#4ade80", "secondary": "#1A1A1A", "bg": "#050505", "text": "#ffffff"},
            "typography": {"heading": "JetBrains Mono", "body": "Inter"},
            "border_radius": "2px"
        } for i in range(5)]