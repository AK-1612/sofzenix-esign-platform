# Security Architecture & Encryption Specification

---

## 1. Defense-in-Depth Security Layers

The platform enforces security controls across five distinct architectural layers:

```
Client ──► Edge WAF ──► API Gateway ──► Spring Security ──► App Services ──► DB / Storage
 (SSL)     (DDoS/CORS)    (Rate Limit)    (JWT / RBAC)     (Business Logic)  (KMS / AES-256)
```

---

## 2. Encryption Standards

- **Encryption in Transit**: All HTTP communications enforced via TLS 1.3. HSTS enabled with preloading.
- **Encryption at Rest**:
  - PostgreSQL & MongoDB data volumes encrypted using AES-256.
  - PDF document binaries in Object Storage encrypted using Server-Side Encryption with Customer-Managed Keys (SSE-KMS / Envelope Encryption).
- **Secrets Management**: No plaintext passwords or API keys stored in source code. Local development uses `.env` files; production uses HashiCorp Vault / AWS Secrets Manager.
- **Digital Certificates**: X.509 PKI certificates for eSignatures generated and signed using Hardware Security Modules (HSM).
