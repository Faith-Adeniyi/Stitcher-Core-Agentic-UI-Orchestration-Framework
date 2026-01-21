"""
STITCHER-CORE: ARCHITECTURAL ORCHESTRATOR
Main execution pipeline for the autonomous web-assembly framework.

This script coordinates the transition from raw brand data to a secured, 
debugged, and production-ready UI output. 

Target Hardware: 8GB RAM (Optimized for local inference)
"""

import sys
import logging
from agents.researcher import WebResearcher
from agents.orchestrator import UIOrchestrator
from core.security import AgenticGuardian
from core.engine import AssemblyEngine
from core.editor import ComponentEditor
from core.debugger import AgenticDebugger

# Centralized Logging Configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_agentic_pipeline(brand_name):
    logging.info(f"--- INITIALIZING STITCHER-CORE PIPELINE FOR: {brand_name} ---")

    try:
        # 1. DATA INGESTION & RESEARCH
        # Extracts 'Brand Memory' from data/brand_memory.json
        researcher = WebResearcher(brand_name)
        brand_data = researcher.extract_services()
        logging.info("RESEARCH: Brand memory ingestion successful.")

        # 2. PRE-PROCESSING (SURGICAL DATA INJECTION)
        # Injects verified data into templates to ensure 100% accuracy 
        # before the LLM handles layout orchestration.
        pre_editor = ComponentEditor()
        pre_editor.inject_data_into_templates(brand_data)
        logging.info("EDITOR: Pre-processing surgical patch complete.")

        # 3. AI ORCHESTRATION (COGNITIVE PLANNING)
        # Local LLM (Ollama) decides the component order and site structure.
        orchestrator = UIOrchestrator()
        ui_plan = orchestrator.generate_plan(brand_data)
        logging.info(f"ORCHESTRATOR: AI has generated the UI blueprint: {ui_plan}")

        # 4. AUTONOMOUS SELF-HEALING (DEBUGGING LOOP)
        # Validates LLM output for structural integrity before assembly.
        debugger = AgenticDebugger()
        diagnostics = debugger.run_diagnostic(str(ui_plan))
        if diagnostics:
            logging.warning(f"DEBUGGER: Structural issues found: {diagnostics}. Healing...")
            ui_plan = debugger.autonomous_patch(str(ui_plan), diagnostics)
        else:
            logging.info("DEBUGGER: UI Plan integrity verified.")

        # 5. SECURITY GUARDIAN (DEFENSE-IN-DEPTH)
        # Sanitizes plan against XSS/Injection and enforces DoS memory guardrails.
        guardian = AgenticGuardian()
        secure_plan = guardian.audit_and_sanitize(ui_plan, "Master_Orchestration_Plan")
        logging.info("SECURITY: Multi-layer audit passed. Forensic log updated.")

        # 6. DETERMINISTIC ASSEMBLY (THE STITCHER)
        # Physically compiles modular components into the final index.html.
        engine = AssemblyEngine()
        output_path = engine.stitch_all(secure_plan)
        logging.info(f"ENGINE: Assembly successful. Production file: {output_path}")

        # 7. POST-ASSEMBLY VALIDATION
        # Final polish to remove AI artifacts and verify final code readiness.
        final_qc = ComponentEditor(file_path=output_path)
        final_qc.validate_and_polish()
        logging.info("QC: Final surgical polish complete. Pipeline finalized.")

    except Exception as e:
        logging.critical(f"PIPELINE FAILURE: {str(e)}")
        sys.exit(1)

    logging.info(f"--- [PIPELINE SUCCESS] {brand_name} is now LIVE ---")

if __name__ == "__main__":
    # Execute with the updated Luxury Pet Spa brand data
    run_agentic_pipeline("Luxury Pet Spa")
