import re
import json
import os
import logging

class AgenticGuardian:
    """
    SECURITY MIDDLEWARE: 
    Treats AI-generated content as untrusted input. Implements Defense-in-Depth 
    protocols to ensure secure UI assembly through sanitization and size auditing.
    """
    def __init__(self, config=None, manifest_path="project_manifest.json"):
        """
        Initializes the Guardian utilizing security policies defined in the manifest.
        """
        self.logger = logging.getLogger("StitcherCore.Security")

        # Load security configuration from external manifest
        if config is None and os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    full_manifest = json.load(f)
                    self.config = full_manifest.get("security_settings", {})
            except Exception as e:
                self.logger.error(f"Security: Policy ingestion failure: {e}")
                self.config = {}
        else:
            self.config = config or {}

        # Set operational constraints
        self.max_payload_size = self.config.get("max_payload_size", 500000)
        self.patterns = self.config.get("blacklisted_patterns", [])

    def audit_and_sanitize(self, raw_content, component_id):
        """
        Main Security Loop: Validates data integrity and sanitizes malicious vectors.
        
        Args:
            raw_content (str/list): The data payload requiring inspection.
            component_id (str): Identifier for the component under audit.
            
        Returns:
            str: The sanitized and validated content string.
        """
        # Ensure type safety by converting complex objects to strings
        if isinstance(raw_content, list):
            self.logger.info(f"Security: Coercing list payload to string for {component_id}")
            raw_content = str(raw_content)

        # 1. DOS PREVENTION: Audit payload size
        try:
            payload_size = len(raw_content.encode('utf-8'))
            if payload_size > self.max_payload_size:
                self.logger.critical(f"Security: Payload size violation blocked for {component_id}")
                return ""
        except (AttributeError, UnicodeEncodeError) as e:
            self.logger.error(f"Security: Integrity check failure for {component_id}: {e}")
            return ""

        # 2. XSS MITIGATION: Filter blacklisted injection patterns
        sanitized = raw_content
        for pattern in self.patterns:
            if re.search(pattern, sanitized, re.IGNORECASE):
                self.logger.warning(f"Security: Malicious pattern intercepted in {component_id}")
                sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)

        return sanitized

if __name__ == "__main__":
    # Internal validation logic for security policy enforcement
    guardian = AgenticGuardian()
    sample_input = "<script>alert('XSS')</script> Valid Content"
    result = guardian.audit_and_sanitize(sample_input, "TEST_UNIT")
    print(f"Sanitization Result: {result}")