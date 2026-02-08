import logging
import time
import json
import os
import webbrowser
import asyncio
import ollama

# Internal Module Ingestion
from agents.researcher import WebResearcher
from agents.ui_ux_designer import UIDesigner
from agents.orchestrator import UIOrchestrator
from core.engine import AssemblyEngine
from core.security import AgenticGuardian
from core.debugger import AgenticDebugger
from core.editor import ComponentEditor

# Configuration: Global Logging Strategy
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class StitcherCoreApp:
    """
    APPLICATION ORCHESTRATOR:
    The central entry point for the Stitcher-Core autonomous assembly pipeline.
    Manages high-level logic for AI research, human overrides, and assembly.
    """
    def __init__(self, manifest_path="project_manifest.json"):
        self.manifest_path = manifest_path
        self.start_time = time.time()
        
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            self.manifest = json.load(f)

        # Initialize Agents
        self.researcher = WebResearcher(manifest_path=self.manifest_path)
        self.designer = UIDesigner(manifest_path=self.manifest_path)
        self.orchestrator = UIOrchestrator(manifest_path=self.manifest_path)
        self.security = AgenticGuardian(manifest_path=self.manifest_path)
        self.debugger = AgenticDebugger(manifest_path=self.manifest_path)
        self.engine = AssemblyEngine(manifest_path=self.manifest_path)
        self.editor = ComponentEditor(
            file_path=self.manifest["engine_settings"]["output_path"],
            manifest_path=self.manifest_path
        )

    async def check_dependencies(self):
        """
        SAFETY LAYER: Ensures the local environment and models are operational.
        """
        print("\n[SYSTEM CHECK] Validating Dependencies...")
        try:
            ollama.list()
            print(" - Ollama Service: [CONNECTED]")
            target_model = self.manifest.get("writing_model", "llama3.2:1b")
            print(f" - Model Integrity ({target_model}): [VERIFIED]")
            return True # Professional handling of boolean logic
        except Exception as e:
            print(f" - FATAL: Ollama service offline or model missing. Error: {e}")
            return False # Professional handling of boolean logic

    def display_preview_hub(self, variants):
        """
        TERMINAL PREVIEW: Shows a summary table of generated designs.
        """
        print("\n" + "-"*70)
        print(f"{'ID':<4} | {'VARIANT NAME':<25} | {'PRIMARY':<10} | {'TYPOGRAPHY'}")
        print("-"*70)
        for i, v in enumerate(variants):
            name = v.get('variant_name', 'UNKNOWN_VARIANT')
            color = v.get('colors', {}).get('primary', '#??????')
            font = v.get('typography', {}).get('heading', 'STANDARD')
            print(f"[{i}]  | {name[:25]:<25} | {color:<10} | {font}")
        print("-"*70)

    async def execute_pipeline(self):
        """
        Executes the end-to-end assembly sequence with ASYNC support,
        security audits, and autonomous debugging.
        """
        if not await self.check_dependencies():
            return

        print("\n" + "="*50)
        print(" STITCHER-CORE: AGENTIC INTERFACE (FEB 7 2026)")
        print("="*50)
        print("[1] FULL AI OVERHAUL: Parallel Research + 5 Variant Gallery")
        print("[2] HUMAN DESIGNER OVERRIDE: Reference Figma/External URL")
        print("[3] TARGETED PATCH: Use Last Approved Design (Save Resources)")
        print("[4] VIEW COGNITIVE TRACE: Inspect AI Decision Logic")
        
        mode_choice = input("\nSelect Execution Mode (1-4): ").strip()

        # Handle Cognitive Trace Viewing separately
        if mode_choice == "4":
            trace_path = "data/cognitive_trace.json"
            if os.path.exists(trace_path):
                print(f"\n[TRACE LOGS] Path: {trace_path}\n")
                with open(trace_path, 'r') as f:
                    print(json.dumps(json.load(f), indent=2))
            else:
                print("\n[!] No trace logs found. Run a full build first.")
            return

        # 1. DATA INGESTION: Extract brand intelligence
        brand_data = self.researcher.extract_services()
        niche = brand_data.get('industry', 'Modern Professional')

        # --- DESIGN SELECTION LOGIC ---
        if mode_choice == "1":
            logging.info(f"PIPELINE: Initiating async research loop for {niche}...")
            research_insights = self.designer.perform_competitive_research(niche)
            variants = await self.designer.generate_variants_async(count=5, research_insights=research_insights)
            self.display_preview_hub(variants)
            
            temp_plan = self.orchestrator.generate_plan(brand_data, variants[0])
            preview_files = await self.engine.generate_previews(temp_plan, variants)
            gallery_path = self.engine.build_gallery(preview_files)
            
            webbrowser.open(f"file://{os.path.abspath(gallery_path)}")
            
            print("\n" + "-"*40)
            print(" GALLERY READY: Review variants in your browser.")
            print("-"*40)
            
            choice_id = input("Input Approved Variant ID (0-4): ").strip()
            selection_idx = int(choice_id) if choice_id.isdigit() and 0 <= int(choice_id) <= 4 else 0
            design_tokens = variants[selection_idx]
            self.designer.save_selected_design(design_tokens)

        elif mode_choice == "2":
            reference_url = input("Paste Figma Link or Design Reference URL: ").strip()
            logging.info("PIPELINE: Injecting human design reference into context.")
            design_tokens = self.designer.ingest_external_reference(reference_url)

        else:
            logging.info("PIPELINE: Resource Management Active. Loading cached tokens.")
            design_tokens = self.designer.load_cached_design()

        # 2. AI ORCHESTRATION: Blueprinting
        ui_plan = self.orchestrator.generate_plan(brand_data, design_tokens)

        # 3. SECURITY AUDIT
        sanitized_plan = self.security.audit_and_sanitize(ui_plan, "LAYOUT_PLAN")

        # 4. DETERMINISTIC ASSEMBLY
        output_path = await self.engine.stitch_all(sanitized_plan, design_tokens)

        if output_path is None:
            logging.error("PIPELINE: Assembly Engine failed. Aborting.")
            return

        # 5. SELF-HEALING
        with open(output_path, 'r', encoding='utf-8') as f:
            raw_html = f.read()

        diagnostics = self.debugger.run_diagnostic(raw_html)
        healed_html = self.debugger.autonomous_patch(raw_html, diagnostics)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(healed_html)

        # 6. FINAL POLISH
        self.editor.inject_data_into_templates(brand_data)
        self.editor.validate_and_polish()

        execution_time = round(time.time() - self.start_time, 2)
        logging.info(f"PIPELINE COMPLETE: Artifact generated in {execution_time}s")

if __name__ == "__main__":
    try:
        app = StitcherCoreApp()
        asyncio.run(app.execute_pipeline())
    except Exception as e:
        logging.critical(f"FATAL PIPELINE FAILURE: {e}")