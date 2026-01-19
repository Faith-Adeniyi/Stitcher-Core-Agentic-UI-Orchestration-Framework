import json

class WebResearcher:
    """
    Agent responsible for ingesting raw business data 
    and formatting it for the Stitcher-Core orchestrator.
    """
    def __init__(self, brand_name):
        self.brand_name = brand_name
        self.memory_file = "data/brand_memory.json"

    def extract_services(self):
        """
        In a full build, this would use BeautifulSoup/Crawl4AI.
        For Phase 1, we define the structured data for the Pet Spa.
        """
        # Mocking the scraped data from the 'Luxury Pet Spa' implementation
        raw_data = {
            "brand": self.brand_name,
            "services": [
                {"name": "Full Grooming", "price": "$85", "duration": "2hrs"},
                {"name": "Puppy Social", "price": "$45", "duration": "1hr"},
                {"name": "Medicated Bath", "price": "$60", "duration": "45mins"}
            ],
            "vibe": "High-end, minimalist, serene"
        }
        return raw_data

    def update_brand_memory(self, data):
        """Saves extracted data to the local memory layer."""
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Memory updated for {self.brand_name}")

if __name__ == "__main__":
    agent = WebResearcher("Luxury Pet Spa")
    extracted = agent.extract_services()
    agent.update_brand_memory(extracted)
