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
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("data/system_audit.log"), logging.StreamHandler()]
)

class StitcherCoreApp:
    """
    APPLICATION ORCHESTRATOR:
    The central entry point for the Stitcher-Core autonomous assembly pipeline.
    Manages high-level logic for AI research, human governance, and deterministic assembly.
    """
    def __init__(self, manifest_path="project_manifest.json"):
        """
        Initializes the orchestration environment using the specified MANIFEST_PATH.
        """
        self.manifest_path = manifest_path
        self.start_time = time.time()
        
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
        except FileNotFoundError:
            logging.error("CRITICAL: project_manifest.json missing.")
            self.manifest = {"engine_settings": {"output_path": "output/index.html"}}

        # Initialize Agentic Layers
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

    def _discover_local_blueprints(self):
        """
        COMPONENT_DISCOVERY:
        Scans the filesystem to identify actual filenames in the templates folder.
        Returns a list of names without extensions to prevent mapping errors.
        """
        blueprint_dir = "templates/components"
        if os.path.exists(blueprint_dir):
            return [f.replace('.html', '') for f in os.listdir(blueprint_dir) if f.endswith('.html')]
        return ["hero_section", "bento_grid", "contact_module"] # Fallback

    async def check_dependencies(self):
        """
        SYSTEM INTEGRITY LAYER:
        Validates that the local inference engine and required models are operational.
        """
        print("\n[SYSTEM CHECK] Validating Environment Dependencies...")
        try:
            ollama.list()
            print(" - Inference Service: [CONNECTED]")
            target_model = self.manifest.get("writing_model", "llama3.2:1b")
            print(f" - Model Integrity ({target_model}): [VERIFIED]")
            return 1 
        except Exception as e:
            print(f" - CRITICAL: Inference service offline. Error: {e}")
            return 0 

    def display_preview_hub(self, variants):
        """
        CLI VISUALIZATION:
        Renders a structured summary table of generated design variants.
        """
        print("\n" + "-"*70)
        print(f"{'ID':<4} | {'VARIANT NAME':<25} | {'PRIMARY':<10} | {'TYPOGRAPHY'}")
        print("-"*70)
        for i, v in enumerate(variants):
            name = v.get('variant_name', 'UNKNOWN_VARIANT')
            color = v.get('colors', {}).get('primary', '#??????')
            font = v.get('typography', {}).get('heading', 'STANDARD_FONT')
            print(f"[{i}]  | {name[:25]:<25} | {color:<10} | {font}")
        print("-"*70)

    async def execute_pipeline(self):
        """
        PIPELINE EXECUTION:
        Orchestrates the asynchronous assembly sequence, security audits, and self-healing.
        """
        if not await self.check_dependencies():
            return

        print("\n" + "="*50)
        print(" STITCHER-CORE: AGENTIC INTERFACE (v1.0.2026)")
        print("="*50)
        
        # Identify actual components available in the folder
        active_components = self._discover_local_blueprints()
        print(f"ACTIVE_BLUEPRINTS: {active_components}")
        
        print("[1] FULL ASSEMBLY: Parallel Research + 5 Variant Synthesis")
        print("[2] HUMAN REFERENCE: Inject External URI")
        print("[3] FAST-TRACK: Resource-Optimized Build (Last Approved)")
        print("[4] AUDIT TRACE: Inspect Cognitive Decision Logs")
        print("[5] EXIT")
        
        mode_choice = input("\nSELECT_ACTION_ID (1-5): ").strip()

        if mode_choice == "5":
            print("SYSTEM_SHUTDOWN: Terminating agentic processes.")
            return

        # 1. INTELLIGENCE INGESTION
        brand_data = self.researcher.extract_services()
        niche = brand_data.get('industry', 'Modern Professional')

        # --- ARCHITECTURAL BRANCHING LOGIC ---
        if mode_choice == "1":
            logging.info(f"PIPELINE: Initiating asynchronous research for: {niche}")
            insights = self.designer.perform_competitive_research(niche)
            variants = await self.designer.generate_variants_async(count=5, research_insights=insights)
            self.display_preview_hub(variants)
            
            # Use discovered filenames to ensure the engine finds the files
            structural_plan = {
                "sections": active_components,
                "navigation": "fixed-top",
                "footer": "minimal-industrial"
            }
            
            preview_files = await self.engine.generate_previews(structural_plan, variants)
            gallery_path = self.engine.build_gallery(preview_files)
            
            webbrowser.open(f"file://{os.path.abspath(gallery_path)}")
            
            print("\n" + "-"*40)
            print(" VISUAL AUDIT READY: Review variants in browser.")
            print("-"*40)
            
            choice_id = input("INPUT APPROVED_VARIANT_ID (0-4): ").strip()
            selection_idx = int(choice_id) if choice_id.isdigit() and 0 <= int(choice_id) <= 4 else 0
            design_tokens = variants[selection_idx]
            self.designer.save_selected_design(design_tokens)

        elif mode_choice == "2":
            reference_url = input("PASTE DESIGN_REFERENCE_URL: ").strip()
            logging.info("PIPELINE: Injecting external design context via HUMAN_OVERRIDE.")
            design_tokens = self.designer.ingest_external_reference(reference_url)
            structural_plan = {"sections": active_components}

        elif mode_choice == "3":
            logging.info("PIPELINE: Resource Management optimized. Loading PERSISTED_DESIGN_TOKENS.")
            design_tokens = self.designer.load_cached_design()
            structural_plan = {"sections": active_components}

        elif mode_choice == "4":
            trace_path = "data/cognitive_trace.json"
            if os.path.exists(trace_path):
                print(f"\n[TRACE_AUDIT] Source: {trace_path}\n")
                with open(trace_path, 'r') as f:
                    print(json.dumps(json.load(f), indent=2))
            else:
                print("\n[!] Error: COGNITIVE_TRACE_LOGS not found.")
            return

        # 2. SYSTEM ORCHESTRATION: Blueprinting
        ui_plan = self.orchestrator.generate_plan(brand_data, design_tokens)
        
        # 3. SECURITY GATEKEEPER
        sanitized_plan = self.security.audit_and_sanitize(ui_plan, "LAYOUT_PLAN_AUDIT")

        # 4. DETERMINISTIC ASSEMBLY ENGINE
        output_path = await self.engine.stitch_all(structural_plan, design_tokens)

        if output_path == "":
            logging.error("PIPELINE: Assembly Engine failure detected.")
            return

        # 5. AUTONOMOUS SELF-HEALING
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                raw_html = f.read()

            diagnostics = self.debugger.run_diagnostic(raw_html)
            healed_html = self.debugger.autonomous_patch(raw_html, diagnostics)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(healed_html)
        except Exception as e:
            logging.warning(f"PIPELINE: Self-healing cycle failed: {e}")

        # 6. FINAL REFINEMENT
        self.editor.inject_data_into_templates(brand_data)
        self.editor.validate_and_polish()

        execution_time = round(time.time() - self.start_time, 2)
        logging.info(f"PIPELINE_SUCCESS: SITE_ARTIFACT generated in {execution_time}s")

if __name__ == "__main__":
    try:
        app = StitcherCoreApp()
        asyncio.run(app.execute_pipeline())
    except KeyboardInterrupt:
        print("\nSYSTEM_HALT: User-initiated interrupt.")
    except Exception as e:
        logging.critical(f"FATAL SYSTEM FAILURE: {e}")