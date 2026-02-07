import os
import json
import logging
import ollama

class AssemblyEngine:
    """
    CONSTRUCTION LAYER:
    The deterministic assembly point of the framework. Translates architectural 
    plans and design tokens into production-ready HTML/CSS artifacts.
    """
    def __init__(self, manifest_path="project_manifest.json"):
        """
        Initializes the engine with manifest-driven configurations for 
        the specialized Coder model.
        """
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
            self.model = self.manifest.get("model", "qwen2.5-coder:7b")
        except FileNotFoundError:
            logging.error(f"ENGINE: {manifest_path} not found. Reverting to default configurations.")
            self.model = "qwen2.5-coder:7b"
            self.manifest = {}

        self.output_dir = "output"
        self.preview_dir = os.path.join(self.output_dir, "previews")

    def stitch_all(self, sanitized_plan, design_tokens, output_override=None):
        """
        Synthesizes the final HTML based on structural logic and visual tokens.
        Utilizes output_override to support multi-variant preview generation.
        """
        logging.info(f"ENGINE: Executing assembly for variant: {design_tokens.get('variant_name', 'Final')}")
        
        # Determine destination: standard output or preview subdirectory
        target_path = output_override if output_override else os.path.join(self.output_dir, "index.html")
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        construction_prompt = f"""
        ACT AS: Senior Frontend Architect.
        MODEL_CONTEXT: {self.model}
        STRUCTURAL_PLAN: {json.dumps(sanitized_plan)}
        DESIGN_TOKENS: {json.dumps(design_tokens)}
        
        TASK: Generate a high-performance index.html using Tailwind CSS.
        STYLING_RULES:
        - Primary Color: {design_tokens.get('colors', {}).get('primary', '#333')}
        - Font: {design_tokens.get('typography', {}).get('heading', 'sans-serif')}
        - Components: {self.manifest.get('available_components', [])}

        NOTE: Follow the STRUCTURAL_PLAN strictly. Return ONLY raw HTML/CSS.
        """

        try:
            response = ollama.generate(model=self.model, prompt=construction_prompt)
            html_content = response['response']

            with open(target_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            return target_path 
        except Exception as e:
            logging.error(f"ENGINE: Synthesis failure at {target_path}: {e}")
            return None

    def generate_previews(self, sanitized_plan, variants):
        """
        Batch-processes multiple design directions to create a suite of 
        interactive HTML instances for comparison.
        """
        logging.info("ENGINE: Commencing batch generation of 5 design previews.")
        preview_paths = []
        
        for i, variant in enumerate(variants):
            file_name = f"variant_{i}.html"
            preview_path = os.path.join(self.preview_dir, file_name)
            
            # Recursive call to stitch_all with the specific variant data
            result = self.stitch_all(sanitized_plan, variant, output_override=preview_path)
            if result:
                preview_paths.append(result)
        
        return preview_paths

    def build_gallery(self, preview_paths):
        """
        Constructs an interactive Selection Hub (gallery.html) that serves as 
        the visual interface for design approval.
        """
        logging.info("ENGINE: Finalizing Selection Gallery for stakeholder review.")
        
        cards_html = ""
        for i, path in enumerate(preview_paths):
            file_name = os.path.basename(path)
            cards_html += f"""
            <div style="background: #111; border: 1px solid #333; padding: 25px; border-radius: 12px; transition: 0.3s hover;">
                <h3 style="color: #00FF41; margin-top: 0; letter-spacing: 1px;">VARIANT {i}</h3>
                <p style="color: #888; font-size: 0.9em; margin-bottom: 20px;">Deterministic layout via Qwen2.5-Coder.</p>
                <a href="{file_name}" target="_blank" style="display: inline-block; background: #3B82F6; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold;">
                    Open Preview
                </a>
            </div>
            """

        gallery_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Stitcher-Core | Design Review</title>
            <style>
                body {{ background-color: #000; color: #FFF; font-family: 'Segoe UI', sans-serif; padding: 60px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }}
                h1 {{ font-size: 2.5em; font-weight: 900; border-left: 5px solid #3B82F6; padding-left: 20px; margin-bottom: 50px; }}
            </style>
        </head>
        <body>
            <h1>DESIGN SELECTION HUB</h1>
            <div class="grid">{cards_html}</div>
            <div style="margin-top: 60px; padding: 20px; background: #1a1a1a; border-radius: 8px; text-align: center;">
                <p style="color: #AAA;">Review the variants above. Return to your CLI to input the ID of your choice.</p>
            </div>
        </body>
        </html>
        """
        
        gallery_file = os.path.join(self.preview_dir, "gallery.html")
        with open(gallery_file, "w", encoding="utf-8") as f:
            f.write(gallery_html)
            
        return gallery_file