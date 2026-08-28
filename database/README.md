# Database Architecture & Scaffolding Strategy (`database/`)

---

## Architectural Strategy

The database layer underpins the multi-tenant document automation platform.

> [!IMPORTANT]
> **DATABASE MODELING DEFERRED**: Actual database schemas, SQL DDL tables, ORM entity maps, and Flyway/Liquibase migration scripts are **intentionally not created** at this stage. Database design will be finalized during **Phase 1: Domain Modeling & API Contract Specification**.

---

## Targeted Polyglot Persistence Architecture

1. **Relational Database (PostgreSQL)**:
   - Primary operational store for structured platform state: Users, Organizations, Permissions, Document Metadata, Workflow Definitions, Signature Certificates, Audit Log references, and SaaS Billing records.
2. **Document Database (MongoDB)**:
   - Semi-structured storage for dynamic workflow state trees, AI extracted entity payloads, and template merge field definitions.
3. **In-Memory Cache & Key-Value Store (Redis)**:
   - Session storage, multi-tenant RBAC token caching, API rate-limiting buckets, and temporary signature OTP verification keys.

---

## Directory Layout

```
database/
├── schema/                 # Relational schema DDL definitions (Pending Phase 1)
├── migrations/             # Version-controlled migration scripts (Flyway/Liquibase)
├── seeds/                  # Baseline seed data for development & testing
├── erd/                    # Entity Relationship Diagrams & visual data models
└── README.md               # Database architectural documentation
```
