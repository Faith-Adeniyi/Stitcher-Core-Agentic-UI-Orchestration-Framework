import logging
import time
import json
import os

# Internal Module Ingestion
from agents.researcher import WebResearcher
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
    Coordinates multi-agent workflows to transform data into production-ready UI.
    """
    def __init__(self, manifest_path="project_manifest.json"):
        """
        Initializes the application lifecycle utilizing the global project manifest.
        """
        self.manifest_path = manifest_path
        self.start_time = time.time()
        
        # Load Global Manifest for Component Initialization
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            self.manifest = json.load(f)

        # Initialize Core and Agentic Modules with Manifest-Driven Configs
        self.researcher = WebResearcher(manifest_path=self.manifest_path)
        self.orchestrator = UIOrchestrator(manifest_path=self.manifest_path)
        self.security = AgenticGuardian(manifest_path=self.manifest_path)
        self.debugger = AgenticDebugger(manifest_path=self.manifest_path)
        self.engine = AssemblyEngine(manifest_path=self.manifest_path)
        self.editor = ComponentEditor(
            file_path=self.manifest["engine_settings"]["output_path"],
            manifest_path=self.manifest_path
        )

    def execute_pipeline(self):
        """
        Executes the end-to-end assembly sequence: Research -> Orchestration -> Security -> Assembly.
        """
        logging.info("PIPELINE: Commencing autonomous build sequence...")

        # 1. DATA INGESTION: Researcher sources verified metrics
        brand_data = self.researcher.extract_services()
        
        # 2. AI ORCHESTRATION: LLM determines layout architecture
        ui_plan = self.orchestrator.generate_plan(brand_data)

        # 3. SECURITY AUDIT: Sanitization of AI-generated structural plans
        sanitized_plan = self.security.audit_and_sanitize(ui_plan, "LAYOUT_PLAN")

        # 4. DETERMINISTIC ASSEMBLY: Engine stitches HTML components
        output_path = self.engine.stitch_all(sanitized_plan)

        # 5. SELF-HEALING & REFINEMENT: Debugger and Editor polish the artifact
        with open(output_path, 'r', encoding='utf-8') as f:
            raw_html = f.read()

        diagnostics = self.debugger.run_diagnostic(raw_html)
        healed_html = self.debugger.autonomous_patch(raw_html, diagnostics)

        # Save healed content back to disk for Editor to finalize
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(healed_html)

        # 6. FINAL POLISH: Deterministic data injection and cleanup
        self.editor.inject_data_into_templates(brand_data)
        self.editor.validate_and_polish()

        execution_time = round(time.time() - self.start_time, 2)
        logging.info(f"PIPELINE COMPLETE: Artifact generated at {output_path} in {execution_time}s")

if __name__ == "__main__":
    """
    APPLICATION ENTRY POINT:
    Instantiates and executes the core application lifecycle.
    """
    try:
        app = StitcherCoreApp()
        app.execute_pipeline()
    except Exception as e:
        logging.critical(f"FATAL PIPELINE FAILURE: {e}")