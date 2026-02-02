import os
import logging
import ast
import json

class AssemblyEngine:
    """
    ENGINE LAYER:
    Acts as the primary execution arm for deterministic UI assembly.
    Orchestrates the concatenation of sanitized HTML components into a 
    production-ready document based on AI-generated architectural plans.
    """
    def __init__(self, config=None, manifest_path="project_manifest.json"):
        """
        Initializes the Engine utilizing path configurations sourced from the global manifest.
        """
        self.logger = logging.getLogger("StitcherCore.Engine")
        
        # Load configuration from manifest to maintain architectural decoupling
        if config is None and os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    full_manifest = json.load(f)
                    self.config = full_manifest.get("engine_settings", {})
            except Exception as e:
                self.logger.error(f"Engine: Configuration ingestion failure: {e}")
                self.config = {}
        else:
            self.config = config or {}

        # Define operational paths with robust fallbacks
        self.components_path = self.config.get("components_path", "templates/components/")
        self.output_path = self.config.get("output_path", "output/index.html")
        self.base_template = self.config.get("base_template", "templates/base.html")
        self.encoding = self.config.get("encoding", "utf-8")
        
        # Ensure target distribution directory exists prior to assembly
        output_dir = os.path.dirname(self.output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

    def stitch_all(self, ui_plan):
        """
        Executes the assembly sequence by iterating through the validated UI plan.
        
        Args:
            ui_plan (list/str): The ordered sequence of component identifiers.
            
        Returns:
            str: The file path of the successfully assembled document.
        """
        self.logger.info("Engine: Initiating deterministic assembly sequence...")
        assembled_content = ""

        # TYPE VALIDATION: Safely handle string-serialized list objects from inference
        if isinstance(ui_plan, str):
            try:
                self.logger.info("Engine: Coercing string-based plan to iterable list.")
                ui_plan = ast.literal_eval(ui_plan)
            except (ValueError, SyntaxError):
                self.logger.error("Engine: Failed to parse plan string. Input is malformed.")
                ui_plan = []

        # 1. Component Iteration Logic
        if isinstance(ui_plan, list):
            for component_name in ui_plan:
                file_name = f"{component_name}.html"
                full_path = os.path.join(self.components_path, file_name)

                # 2. Resource Verification
                if os.path.exists(full_path):
                    self.logger.info(f"Engine: Integrating component: {file_name}")
                    with open(full_path, 'r', encoding=self.encoding) as f:
                        content = f.read()
                        # Injecting visual separators for production-ready code organization
                        assembled_content += f"\n\n\n"
                        assembled_content += content
                else:
                    self.logger.warning(f"Engine: Resource {file_name} not found in {self.components_path}. Skipping...")
        else:
            self.logger.critical("Engine: Assembly sequence aborted. Invalid UI plan format.")

        # 3. Document Finalization
        return self._finalize_document(assembled_content)

    def _finalize_document(self, body_content):
        """
        Wraps synthesized content into the master HTML skeleton.
        """
        try:
            # Layout Injection Logic
            if os.path.exists(self.base_template):
                with open(self.base_template, 'r', encoding=self.encoding) as f:
                    skeleton = f.read()
                # Deterministic replacement of the content placeholder
                final_html = skeleton.replace("{{CONTENT}}", body_content)
            else:
                self.logger.warning("Engine: Base layout missing. Utilizing fallback HTML5 skeleton.")
                final_html = f"<!DOCTYPE html>\n<html>\n<body>\n{body_content}\n</body>\n</html>"

            # Persist finalized artifact to disk
            with open(self.output_path, 'w', encoding=self.encoding) as f:
                f.write(final_html)
            
            self.logger.info(f"Engine: Assembly successful. Production artifact persisted to {self.output_path}")
            return self.output_path
            
        except Exception as e:
            self.logger.error(f"Engine: Critical failure during document finalization: {e}")
            raise

if __name__ == "__main__":
    """
    INTERNAL MODULE VALIDATION:
    Performs a controlled test of the assembly sequence using a standard manifest.
    """
    engine_test = AssemblyEngine()
    mock_plan = ["hero", "footer"]
    engine_test.stitch_all(mock_plan)