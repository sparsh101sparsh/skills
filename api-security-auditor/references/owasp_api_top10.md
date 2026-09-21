# OWASP API Security Top 10 Reference

| ID | Vulnerability Name | Severity | Attack Mechanism | Hardening Remediation |
|---|---|---|---|---|
| **API1** | Broken Object Level Authorization (BOLA) | Critical | Manipulating object IDs in endpoint URI | Check user ownership in database query |
| **API2** | Broken Authentication | High | Weak tokens, missing expiration | Use signed JWT / cryptographically random tokens |
| **API3** | Broken Object Property Level Authorization | High | Mass assignment of sensitive fields (`is_admin`) | Pydantic strict schemas with field allowlists |
| **API4** | Unrestricted Resource Consumption | High | ReDoS, unlimited page size, missing rate limits | `slowapi` rate limiting, pagination `le=100` |
| **API5** | Broken Function Level Authorization | High | Regular user calling `/admin/...` endpoints | Role-based dependency guards (`Depends(require_admin)`) |
| **API6** | Unrestricted Access to Sensitive Business Flows | High | Scalping, bot checkout, rapid voting | Captcha, action tokens, proof-of-work |
| **API7** | Server Side Request Forgery (SSRF) | High | Fetching arbitrary internal IP (`169.254.169.254`) | Validate against private IP CIDR ranges |
| **API8** | Security Misconfiguration | Medium | Uncaught exceptions showing stack trace | Custom global exception handler returning clean JSON |
| **API9** | Improper Inventory Management | Medium | Exposing deprecated `/api/v0/` or test endpoints | Deprecate and remove stale route mounts |
| **API10** | Unsafe Consumption of APIs | High | Blindly trusting 3rd-party webhook payloads | Verify HMAC-SHA256 signature on inbound webhooks |
