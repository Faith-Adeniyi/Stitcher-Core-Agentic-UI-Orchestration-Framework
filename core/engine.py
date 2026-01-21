import os
import logging

class AssemblyEngine:
    """
    ENGINE LAYER: The 'Hands' of the system.
    Responsible for the deterministic assembly of sanitized 
    HTML components into a final production-ready document.
    """
    def __init__(self):
        self.components_path = "templates/components/"
        self.output_path = "output/index.html"
        self.base_template = "templates/base.html"

    def stitch_all(self, ui_plan):
        """
        Takes the structural plan from the Orchestrator and 
        physically assembles the index.html file.
        """
        logging.info("Engine: Commencing final assembly...")
        assembled_content = ""

        # 1. Iterate through the AI-ordered plan
        for component_name in ui_plan:
            file_name = f"{component_name}.html"
            full_path = os.path.join(self.components_path, file_name)

            # 2. Safety Check: Ensure the component actually exists
            if os.path.exists(full_path):
                logging.info(f"Engine: Stitching {file_name}...")
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    assembled_content += f"\n\n"
                    assembled_content += content
            else:
                logging.warning(f"Engine: Component {file_name} not found! Skipping...")

        # 3. Final Compilation
        # We wrap the stitched components in a base layout (Navbar, CSS, etc.)
        return self._finalize_document(assembled_content)

    def _finalize_document(self, body_content):
        """Wraps the body content into the master HTML skeleton."""
        try:
            # If base.html exists, we inject content into it
            if os.path.exists(self.base_template):
                with open(self.base_template, 'r') as f:
                    skeleton = f.read()
                final_html = skeleton.replace("{{CONTENT}}", body_content)
            else:
                # Fallback if base.html is missing
                final_html = f"<html><body>{body_content}</body></html>"

            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
            
            return self.output_path
            
        except Exception as e:
            logging.error(f"Engine: Critical failure during finalization: {e}")
            raise
