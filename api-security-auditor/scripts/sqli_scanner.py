#!/usr/bin/env python3
"""
SQL Injection Adversarial Scanner.
Tests HTTP endpoints against classic, union-based, and error-based injection payloads.
"""

from __future__ import annotations
import urllib.parse
from typing import List, Dict, Any, Tuple

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "\" OR 1=1 --",
    "1' UNION SELECT NULL, NULL, NULL --",
    "admin' --",
    "'; DROP TABLE test; --",
    "1 AND 1=2 UNION SELECT 'inject', 'probe'--"
]

SQL_ERROR_PATTERNS = [
    "sqlite3.operationalerror",
    "syntax error near",
    "unclosed quotation mark",
    "pg_query",
    "mysql_fetch_array",
    "ora-01756",
    "psycopg2.errors",
    "sqlalchemy.exc"
]

def check_sqli_vulnerability(response_status: int, response_text: str) -> Tuple[bool, str]:
    """
    Evaluates response for SQL injection vulnerability indicators.
    Returns (is_vulnerable, reason).
    """
    # 1. Check for database error disclosure in response body (Critical API8 vulnerability)
    lower_text = response_text.lower()
    for pattern in SQL_ERROR_PATTERNS:
        if pattern in lower_text:
            return True, f"Database error leaked in response: '{pattern}'"

    # 2. 500 Internal Server Error under injection indicates unhandled crash
    if response_status == 500:
        return True, "Endpoint crashed with HTTP 500 Internal Server Error under SQL injection payload."

    return False, "Endpoint handled payload safely."

def generate_sqli_test_urls(base_url: str, params: Dict[str, str]) -> List[Dict[str, Any]]:
    """Generates test cases injecting payloads across every query parameter."""
    test_cases = []
    for param_key in params:
        for payload in SQLI_PAYLOADS:
            modified_params = dict(params)
            modified_params[param_key] = payload
            encoded_query = urllib.parse.urlencode(modified_params)
            test_url = f"{base_url}?{encoded_query}"
            test_cases.append({
                "target_param": param_key,
                "payload": payload,
                "url": test_url
            })
    return test_cases
