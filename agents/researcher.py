import json
import os
import logging

class WebResearcher:
    """
    INGESTION LAYER:
    Responsible for sourcing, sanitizing, and structuring entity-specific data.
    Acts as the primary data interface for the Stitcher-Core pipeline.
    """
    def __init__(self, config=None, manifest_path="project_manifest.json"):
        """
        Initializes the Researcher with parameters sourced from the global manifest.
        """
        # Load configuration from manifest if not explicitly provided
        if config is None and os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r') as f:
                    full_manifest = json.load(f)
                    self.config = full_manifest.get("researcher_settings", {})
                logging.info(f"RESEARCHER: Configuration successfully ingested from {manifest_path}")
            except Exception as e:
                logging.error(f"RESEARCHER: Manifest ingestion failure: {e}")
                self.config = {}
        else:
            self.config = config or {}

        # Define data source and memory persistence paths
        self.source_data_path = self.config.get("source_data", "data/brand_memory.json")
        self.depth = self.config.get("depth", "standard")

    def extract_services(self):
        """
        Sourcing Logic: Retrieves structured data from the local memory layer.
        In advanced iterations, this module integrates BeautifulSoup/Crawl4AI for live scraping.
        """
        logging.info(f"RESEARCHER: Commencing data extraction from {self.source_data_path}")
        
        try:
            if os.path.exists(self.source_data_path):
                with open(self.source_data_path, 'r', encoding='utf-8') as f:
                    extracted_data = json.load(f)
                logging.info("RESEARCHER: Data extraction successful.")
                return extracted_data
            else:
                logging.warning(f"RESEARCHER: Source data not found at {self.source_data_path}. Utilizing fallback schema.")
                return self._get_fallback_data()
        except Exception as e:
            logging.error(f"RESEARCHER: Extraction error: {e}")
            return self._get_fallback_data()

    def _get_fallback_data(self):
        """Internal safety mechanism to ensure pipeline continuity."""
        return {
            "brand": "Stitcher-Core Project",
            "services": [],
            "vibe": "Professional, Scalable, Agentic"
        }

    def update_brand_memory(self, data):
        """
        Persistence Logic: Updates the local repository with sanitized data structures.
        """
        try:
            # Ensure the directory exists prior to file I/O
            os.makedirs(os.path.dirname(self.source_data_path), exist_ok=True)
            
            with open(self.source_data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            logging.info(f"RESEARCHER: Local memory layer updated at {self.source_data_path}")
        except Exception as e:
            logging.error(f"RESEARCHER: Memory update failure: {e}")

if __name__ == "__main__":
    # Unit test demonstrating generic execution
    agent = WebResearcher()
    data = agent.extract_services()
    print(f"Extracted Brand: {data.get('brand')}")