import os
import logging
import ast

class AssemblyEngine:
    """
    ENGINE LAYER: The execution arm of the framework.
    Responsible for the deterministic assembly of sanitized 
    HTML components into a final production-ready document.
    """
    def __init__(self):
        # Configuration for source and distribution paths
        self.components_path = "templates/components/"
        self.output_path = "output/index.html"
        self.base_template = "templates/base.html"
        
        # Ensure output directory exists to maintain system integrity
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def stitch_all(self, ui_plan):
        """
        Takes the structural plan from the Orchestrator and 
        physically assembles the index.html file.
        """
        logging.info("Engine: Commencing deterministic assembly sequence...")
        assembled_content = ""

        # VALIDATION: Ensure ui_plan is an iterable list.
        # If the LLM returns a string representation of a list, convert it safely.
        if isinstance(ui_plan, str):
            try:
                logging.info("Engine: String-based plan detected. Attempting type coercion to list.")
                ui_plan = ast.literal_eval(ui_plan)
            except (ValueError, SyntaxError):
                logging.error("Engine: Failed to parse plan string. Plan is malformed.")
                ui_plan = []

        # 1. Iterate through the validated, AI-ordered plan
        if isinstance(ui_plan, list):
            for component_name in ui_plan:
                file_name = f"{component_name}.html"
                full_path = os.path.join(self.components_path, file_name)

                # 2. Integrity Check: Verify component existence prior to I/O
                if os.path.exists(full_path):
                    logging.info(f"Engine: Stitching component: {file_name}")
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        assembled_content += f"\n\n\n"
                        assembled_content += content
                else:
                    logging.warning(f"Engine: Resource {file_name} not found in {self.components_path}. Skipping...")
        else:
            logging.critical("Engine: Assembly aborted. Provided UI plan is not a valid list.")

        # 3. Final Compilation and Wrapping
        return self._finalize_document(assembled_content)

    def _finalize_document(self, body_content):
        """Wraps the assembled body content into the master HTML skeleton."""
        try:
            # Injection logic for the master layout
            if os.path.exists(self.base_template):
                with open(self.base_template, 'r', encoding='utf-8') as f:
                    skeleton = f.read()
                # Use a professional placeholder replacement strategy
                final_html = skeleton.replace("{{CONTENT}}", body_content)
            else:
                logging.warning("Engine: Base template missing. Utilizing fallback skeleton.")
                final_html = f"<!DOCTYPE html><html><body>{body_content}</body></html>"

            # Write final production-ready file
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
            
            logging.info(f"Engine: Assembly successful. Output persisted to {self.output_path}")
            return self.output_path
            
        except Exception as e:
            logging.error(f"Engine: Critical failure during document finalization: {e}")
            raise