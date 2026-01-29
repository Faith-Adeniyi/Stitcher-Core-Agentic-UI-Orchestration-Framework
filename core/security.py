import re
import logging

class AgenticGuardian:
    """
    SECURITY MIDDLEWARE: Treats AI-generated code as untrusted user input.
    Implements Defense-in-Depth to ensure secure UI assembly.
    """
    def __init__(self):
        # Prevention of XSS & Injection Attacks
        self.blacklisted_patterns = [
            r"<script.*?>",   # JavaScript Injection
            r"onload=",       # Event Handler Injection
            r"onerror=",      # Common XSS vector
            r"<iframe.*?>",   # Clickjacking/Redirection protection
            r"javascript:"    # Protocol-based execution
        ]
        self.max_payload_size = 500000 # DoS Mitigation: 500KB Limit

    def audit_and_sanitize(self, raw_content, component_id):
        """
        Main Security Loop: Validates Integrity & Sanitizes Input.
        """
        # Ensure raw_content is a string before processing
        if isinstance(raw_content, list):
            logging.info(f"SECURITY: Converting list payload to string for {component_id}")
            raw_content = str(raw_content)

        # 1. DOS PREVENTION: Audit payload size before processing
        try:
            payload_size = len(raw_content.encode('utf-8'))
            if payload_size > self.max_payload_size:
                logging.critical(f"DoS Attempt/Resource Bloat Blocked: {component_id}")
                return ""
        except AttributeError as e:
            logging.error(f"SECURITY ERROR: Encoding failed for {component_id}. Data type: {type(raw_content)}")
            return ""

        # 2. XSS MITIGATION: Sanitize malicious scripting
        sanitized = raw_content
        for pattern in self.blacklisted_patterns:
            if re.search(pattern, sanitized, re.IGNORECASE):
                logging.warning(f"Injection Pattern Blocked in {component_id}: {pattern}")
                sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)

        return sanitized