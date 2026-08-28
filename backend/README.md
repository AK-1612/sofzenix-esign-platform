# Sofzenix eSign - Core Backend Application Scaffold

> Java / Spring Boot Modular Monolith Architecture for Document Lifecycle Orchestration.

---

## Backend Architecture & Design Principles

The backend is structured as a **Modular Monolith**. Rather than deploying ten separate microservices on day one, the platform establishes strict package-level and module-level boundaries within a unified Spring Boot application.

### Key Architectural Guidelines
1. **Modular Boundaries**: Each of the 10 engineering modules resides in its dedicated top-level package.
2. **Layered Separation**:
   - `controller`: Web HTTP request handling, DTO mapping, and input validation.
   - `service`: Core business logic, transaction boundaries, and event publishing.
   - `repository`: Data access interfaces (Spring Data JPA / MongoRepository).
   - `model`: Domain entities (To be designed in Phase 1 domain modeling).
   - `dto`: Data transfer objects for request/response payloads.
   - `config`: Module-specific Spring bean configurations.
   - `exception`: Module-specific exception handlers and fault contracts.
   - `test`: Unit and integration test suites.
3. **No Domain Models or Endpoints Yet**: This scaffold establishes structural boundaries only. Domain entities, database schemas, and REST endpoints will be added during domain design.

---

## Core Engineering Modules

```
backend/
├── config/             # Global Spring Boot, Security & Gateway configurations
├── identity/           # Organizations, Tenants, Users, RBAC, Permissions
├── documents/          # Document storage metadata, versioning, search, lifecycle
├── generation/         # Template engine, contract dynamic generation, PDF compiler
├── esignature/         # Signature capture, Aadhaar eSign, DSC certs, legal seal
├── workflow/           # Workflow engine, approval matrix, escalation timers
├── ai/                 # AI service integration gateway client & routing
├── communication/      # Email, WhatsApp, and SMS multi-channel notification engine
├── integrations/       # CRM/ERP webhooks and third-party connector boundaries
├── analytics/          # Audit log aggregator, metric generation, reporting
└── billing/            # Multi-tenant SaaS subscription plans and invoicing
```
