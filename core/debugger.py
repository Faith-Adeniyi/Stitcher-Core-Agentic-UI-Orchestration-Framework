import logging
import re

class AgenticDebugger:
    """
    AUTONOMOUS SELF-HEALING MODULE: Identifies structural failures 
    in AI-generated components and injects surgical fixes.
    """
    def __init__(self):
        self.log_file = "data/debug_logs.log"

    def run_diagnostic(self, generated_html):
        """Tests the output for common AI-generated breakage."""
        issues_found = []
        
        # Test 1: Check for unclosed div tags (common AI error)
        if generated_html.count('<div') != generated_html.count('</div'):
            issues_found.append("DIV_MISMATCH")

        # Test 2: Check for empty Tailwind class strings
        if 'class=""' in generated_html:
            issues_found.append("EMPTY_CLASSES")

        return issues_found

    def autonomous_patch(self, html_content, issues):
        """Targets specific failures and injects updates without full rewrite."""
        patched_html = html_content
        
        for issue in issues:
            if issue == "DIV_MISMATCH":
                # Surgical fix: Appends a closing div if one is missing at the end
                patched_html += "\n</div>"
                logging.warning("DEBUGGER: Fixed DIV_MISMATCH by surgical injection.")
            
            if issue == "EMPTY_CLASSES":
                # Surgical fix: Removes empty class attributes to keep HTML valid
                patched_html = patched_html.replace('class=""', '')
                logging.warning("DEBUGGER: Cleaned EMPTY_CLASSES from output.")

        return patched_html
