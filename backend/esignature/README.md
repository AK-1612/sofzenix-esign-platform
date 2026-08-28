# eSignature Module (`backend/esignature`)

## Architectural Boundary
Handles multi-party electronic signature capture (drawn, typed, image upload), Aadhaar eSign integration, Digital Signature Certificates (DSC / PKI), legal seal stamping, sequential/parallel signing orchestration, signature placement coordinates, hash verification, and completion audit certificate generation.

## Layer Structure
- `controller/`: Signature request & verification controllers.
- `service/`: Signing orchestrator, HSM / PKI wrapper, Completion certificate builder.
- `repository/`: Signature request and certificate JPA repositories.
- `model/`: SignatureRequest, Signer, Certificate, LegalSeal.
- `dto/`: Signing payloads and verification responses.
- `config/`: Crypto provider & Aadhaar eSign configuration.
- `exception/`: InvalidSignatureException, CertificateExpiredException.
- `test/`: Signature verification tests.

> Status: Scaffolding baseline. No domain entities or fake API endpoints implemented.
