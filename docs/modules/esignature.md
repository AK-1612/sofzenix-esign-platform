# eSignature Module Specification (`esignature`)

---

## 1. Purpose
The eSignature module orchestrates legal electronic signature capture, digital PKI certificate signing, Aadhaar eSign integration, signature coordinate placement, and tamper-evident completion certificate generation.

## 2. Responsibilities
- Signature capture modalities: Drawn signature canvas, typed signature font rasterization, image upload.
- Aadhaar eSign integration and Hardware Security Module (HSM) digital certificate signing.
- Support for Digital Signature Certificates (DSC Class 2 / Class 3).
- Signature field coordinate placement and recipient mapping.
- Multi-signer routing orchestration (Sequential signing, Parallel signing).
- Document hash verification (SHA-256) pre- and post-signature.
- Generation of legally binding Signature Completion Audit Certificates.

## 3. Scope
- **In-Scope**: Recipient signing session state, signature coordinate overlay, digital certificate embedding, audit certificate rendering.
- **Out-of-Scope**: Delivery of signature invitation emails/SMS (owned by Communication Hub).

## 4. Dependencies
- Document Management Module (for fetching source PDF and persisting signed PDF).
- Identity Module (for user signer identity verification).

## 5. External Integrations
- Aadhaar eSign ESP Gateways (C-DAC, NSDL e-Gov, eMudhra).
- Licensed Certifying Authorities (CA) for DSC verification.

## 6. Future Capabilities
- Biometric facial recognition and video-based signer verification (eKYC).
- Geolocation capturing and IP timestamp stamping per signature action.

## 7. Open Questions
- Decision pending on primary HSM provider for centralized cloud X.509 digital certificate signing.
