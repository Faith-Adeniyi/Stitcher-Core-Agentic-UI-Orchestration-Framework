import os
import json
import logging
import asyncio
from ollama import AsyncClient

class AssemblyEngine:
    """
    CONSTRUCTION LAYER:
    The deterministic assembly point. Translates architectural plans and 
    design tokens into HTML/CSS artifacts using parallel synthesis.
    """
    def __init__(self, manifest_path="project_manifest.json"):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
            # Professional setting: Using the heavier Coder model for logic
            self.model = self.manifest.get("model", "qwen2.5-coder:7b")
        except FileNotFoundError:
            logging.error(f"ENGINE: {manifest_path} not found. Using defaults.")
            self.model = "qwen2.5-coder:7b"
            self.manifest = {}

        self.output_dir = "output"
        self.preview_dir = os.path.join(self.output_dir, "previews")

    async def stitch_all(self, sanitized_plan, design_tokens, output_override=None):
        """
        Synthesizes the final HTML based on structural logic and visual tokens.
        Upgraded to be ASYNCHRONOUS for high-speed assembly.
        """
        variant_label = design_tokens.get('variant_name', 'Final')
        logging.info(f"ENGINE: Synthesizing HTML for: {variant_label}")
        
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

        NOTE: Return ONLY the raw HTML/CSS code. No markdown formatting.
        """

        try:
            # Using AsyncClient for non-blocking inference
            response = await AsyncClient().generate(model=self.model, prompt=construction_prompt)
            html_content = response['response'].strip()

            # Remove markdown backticks if the model ignores instructions
            if html_content.startswith("```html"):
                html_content = html_content.replace("```html", "").replace("```", "")

            with open(target_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            return target_path 
        except Exception as e:
            logging.error(f"ENGINE: Synthesis failure at {target_path}: {e}")
            return None

    async def generate_previews(self, sanitized_plan, variants):
        """
        HIGH-CONCURRENCY BATCH:
        Uses asyncio.gather to build all 5 variants at once.
        """
        logging.info("ENGINE: Triggering parallel generation for 5 design directions.")
        
        tasks = []
        for i, variant in enumerate(variants):
            file_name = f"variant_{i}.html"
            preview_path = os.path.join(self.preview_dir, file_name)
            # Queue the async task
            tasks.append(self.stitch_all(sanitized_plan, variant, output_override=preview_path))
        
        # Execute all 5 coding tasks simultaneously
        preview_paths = await asyncio.gather(*tasks)
        
        # Filter out any failed builds (None)
        return [path for path in preview_paths if path]

    def build_gallery(self, preview_paths):
        """
        Constructs the selection hub for visual approval.
        """
        logging.info("ENGINE: Finalizing Selection Gallery.")
        
        cards_html = ""
        for i, path in enumerate(preview_paths):
            file_name = os.path.basename(path)
            cards_html += f"""
            <div style="background: #111; border: 1px solid #333; padding: 25px; border-radius: 12px;">
                <h3 style="color: #00FF41; margin-top: 0;">VARIANT {i}</h3>
                <p style="color: #888; font-size: 0.9em; margin-bottom: 20px;">Built by Qwen2.5-Coder.</p>
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
                h1 {{ font-size: 2.5em; border-left: 5px solid #3B82F6; padding-left: 20px; margin-bottom: 50px; }}
            </style>
        </head>
        <body>
            <h1>DESIGN SELECTION HUB</h1>
            <div class="grid">{cards_html}</div>
            <div style="margin-top: 60px; padding: 20px; background: #1a1a1a; border-radius: 8px; text-align: center;">
                <p style="color: #AAA;">Review variants. Then, return to CLI to approve a Variant ID.</p>
            </div>
        </body>
        </html>
        """
        
        gallery_file = os.path.join(self.preview_dir, "gallery.html")
        with open(gallery_file, "w", encoding="utf-8") as f:
            f.write(gallery_html)
            
        return gallery_file