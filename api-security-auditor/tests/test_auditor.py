import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from sqli_scanner import check_sqli_vulnerability, generate_sqli_test_urls, SQLI_PAYLOADS
from path_traversal_scanner import check_traversal_vulnerability, generate_traversal_tests, TRAVERSAL_PAYLOADS
from audit_api import run_mock_audit

def test_sqli_detection_on_leaked_db_error():
    vulnerable_response = "Internal Server Error: sqlite3.OperationalError: near 'OR': syntax error"
    is_vuln, reason = check_sqli_vulnerability(500, vulnerable_response)
    assert is_vuln is True
    assert "leaked in response" in reason

def test_sqli_safe_rejection():
    safe_response = '{"detail": "Invalid search parameter"}'
    is_vuln, reason = check_sqli_vulnerability(400, safe_response)
    assert is_vuln is False

def test_path_traversal_detection():
    leak_response = "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin"
    is_vuln, reason = check_traversal_vulnerability(200, leak_response)
    assert is_vuln is True
    assert "Sensitive file contents leaked" in reason

def test_path_traversal_safe_rejection():
    safe_response = '{"detail": "File not found"}'
    is_vuln, reason = check_traversal_vulnerability(404, safe_response)
    assert is_vuln is False

def test_url_generation():
    cases = generate_sqli_test_urls("https://api.example.com/search", {"q": "deepfake", "limit": "10"})
    assert len(cases) == len(SQLI_PAYLOADS) * 2

    traversal_cases = generate_traversal_tests("https://api.example.com/files", "filename")
    assert len(traversal_cases) == len(TRAVERSAL_PAYLOADS)

def test_audit_runner():
    res = run_mock_audit()
    assert res["verdict"] == "SECURE"
    assert res["vulnerabilities_found"] == 0
