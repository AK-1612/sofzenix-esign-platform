# Architectural Decisions Log (ADR)

> Documenting key technical decisions, trade-offs, and pending architectural confirmations.

---

## Decision Log Summary

| ADR ID | Title | Status | Primary Decision |
| :--- | :--- | :--- | :--- |
| **ADR-001** | Service Boundary & Microservices Strategy | **APPROVED** | Enforce Modular Monolith initially; decompose to microservices post-scale validation. |
| **ADR-002** | Frontend Framework Selection | **DECISION PENDING** | Evaluating React.js SPA vs Next.js SSR/ISR framework. |
| **ADR-003** | Workflow Engine Standard | **DECISION PENDING** | Evaluating Camunda BPM 7/8 vs Flowable Engine. |
| **ADR-004** | Object Storage Provider | **DECISION PENDING** | Evaluating AWS S3 vs Azure Blob Storage. |
| **ADR-005** | Multi-Tenancy Data Isolation Strategy | **DECISION PENDING** | Evaluating Schema-per-tenant vs Database-per-tenant vs Shared Schema with Discriminator Column / RLS. |

---

## Detailed Architectural Decision Records

### ADR-001: Service Boundary & Microservices Strategy
- **Status**: Approved
- **Context**: The platform contains 10 functional modules. Deploying 10 independent microservices from day one introduces severe operational complexity and network latency.
- **Decision**: Establish strict modular boundaries within a unified Spring Boot application (Modular Monolith). Service decomposition will be performed module-by-module after scalability and deployment requirements are validated.

---

### ADR-002: Frontend Framework Selection
- **Status**: **Decision Pending**
- **Options**:
  1. *React.js Single Page Application (Vite)*: Simpler client rendering, lower server footprint.
  2. *Next.js (App Router)*: Native Server-Side Rendering (SSR), static site generation for public signing links, SEO benefits.
- **Next Step**: To be finalized during Phase 1 design after recipient load requirements are confirmed.

---

### ADR-003: Workflow Engine Standard
- **Status**: **Decision Pending**
- **Options**:
  1. *Camunda BPM*: Enterprise standard BPMN 2.0 engine, robust cockpit UI.
  2. *Flowable Engine*: Lightweight embeddable BPMN/CMMN/DMN engine with low memory footprint.
- **Next Step**: Benchmarking engine memory overhead and Spring Boot integration simplicity.

---

### ADR-004: Object Storage Provider
- **Status**: **Decision Pending**
- **Options**:
  1. *AWS S3*: Industry standard Object Storage with Object Lock for immutability compliance.
  2. *Azure Blob Storage*: Immutable Blob storage with WORM compliance.
- **Next Step**: Finalize based on enterprise customer cloud deployment preference.

---

### ADR-005: Multi-Tenancy Data Isolation Strategy
- **Status**: **Decision Pending**
- **Options**:
  1. *Shared Schema with Tenant ID Column*: Maximum resource density, enforces logical row-level security (RLS).
  2. *Schema-per-Tenant*: Stronger logical isolation within a shared PostgreSQL database instance.
  3. *Database-per-Tenant*: Physical isolation for strict Enterprise compliance.
- **Next Step**: Documenting trade-offs and selecting default tier-based tenant isolation strategy during domain modeling.
