# Sofzenix eSign & Intelligent Document Automation Platform

> Enterprise Cloud-Native SaaS Platform for Complete Business Document Lifecycle Automation.

---

## Project Overview

**Sofzenix eSign & Intelligent Document Automation Platform** is a multi-tenant enterprise SaaS solution engineered to automate the end-to-end lifecycle of critical business documents—spanning document generation, multi-party electronic signatures, approval workflows, compliance auditing, AI-powered extraction, and enterprise integrations.

---

## Project Vision & Objectives

Modern enterprise document management requires far more than passive storage or basic signature capture. Sofzenix provides an end-to-end orchestration platform where documents are treated as active, state-aware entities moving through defined lifecycle stages:

```
Create ──► Generate ──► Review ──► Approve ──► Sign ──► Store ──► Audit ──► Analyze ──► Archive ──► Expire
```

### Key Objectives
1. **Lifecycle Automation**: Automate creation, review, routing, signature, archiving, and retention.
2. **Multi-Jurisdiction eSignature Compliance**: Support digital certificates, Aadhaar eSign, Hardware Security Modules (HSM), legal seal, and audit certificate generation.
3. **Extensible Business Workflows**: Provide standard engine components to power specialized business processes like HR Onboarding, Sales Contracting, Legal Clause Analysis, and Vendor Invoicing.
4. **AI-Driven Intelligence**: Extract structured entities, classify document types, analyze risk clauses, and power intelligent document search via a dedicated Python AI engine.
5. **Enterprise Integration**: Seamlessly connect with CRMs, ERPs, HRIS systems, and cloud storage providers through webhooks and REST APIs.

---

## Current Status & Non-Goals

> [!IMPORTANT]
> **CURRENT STATUS**: Architecture and repository scaffold baseline.
>
> **NOT YET IMPLEMENTED**:
> Business logic, domain models, API contracts, AI functionality, workflow execution, integrations, authentication, billing, or production deployment pipelines.

---

## Core Engineering Modules

The platform architecture is organized around **10 core engineering modules**:

1. **Identity & Organization**: Multi-tenant hierarchies, teams, RBAC, user identity, activity tracking.
2. **Document Management**: Document storage metadata, versioning, tagging, search, archive, expiry.
3. **Document Generation**: Templates, dynamic merge fields, PDF compilation, QR code generation, watermarking.
4. **eSignature**: Signature capture, digital signatures, Aadhaar eSign, DSC/PKI certificates, signing order, completion certificates.
5. **Workflow & Approval**: Workflow definitions, approval routing matrices, escalation timers, automated notifications.
6. **AI & Document Intelligence**: OCR, text & key-value extraction, document classification, risk clause detection, smart search.
7. **Communication Hub**: Multi-channel delivery system across Email (SMTP/SendGrid), WhatsApp Business API, and SMS gateways.
8. **Integration & API Platform**: REST API gateway, outbound webhook event dispatchers, third-party connectors (Salesforce, HubSpot, etc.).
9. **Analytics, Audit & Administration**: Platform metrics, tamper-evident audit trails, tenant-level administrative consoles.
10. **SaaS Billing**: Subscription tiers, usage metering, GST invoicing, automated renewal management.

---

## Business Workflows

Business domain processes (e.g., HR, Sales, Legal, Procurement) are **not** standalone engineering modules; they are high-level workflows executed using the platform's core capabilities:

- **HR Workflow**: Candidate Offer Letter Generation ➔ Approval ➔ Candidate eSign ➔ HR Signature ➔ Vault Storage ➔ Joining Kit Generation.
- **Sales Workflow**: Sales Won Event ➔ Contract Generation ➔ Internal Approval ➔ Customer eSign ➔ Sales Manager Sign ➔ Invoice Trigger.
- **Legal Workflow**: Contract Upload ➔ AI Risk & Clause Analysis ➔ Legal Counsel Approval ➔ Execution ➔ Archive.
- **Invoice Workflow**: Invoice Creation ➔ Dual Approval ➔ Customer Sign ➔ Payment Gateway ➔ Receipt Generation.

Detailed workflow specifications are documented in [`docs/workflows/business-workflows.md`](file:///Users/anshulk/Downloads/sofzenix-esign-platform/docs/workflows/business-workflows.md).

---

## AI Capabilities & Architecture

Artificial Intelligence and ML features reside in a decoupled service boundary inside the [`ai/`](file:///Users/anshulk/Downloads/sofzenix-esign-platform/ai/) workspace, powered by Python, FastAPI, and LangChain/OpenAI/Gemini APIs. 

Core capabilities to be implemented include:
- Optical Character Recognition (OCR) & PDF Text Extraction.
- Document Type Classification & Key-Value Pair Extraction.
- Automated Contract Clause Risk Detection.
- Semantic Vector Search & AI Assistant.

---

## Technology Stack

| Tier | Primary Technologies | Architectural Notes |
| :--- | :--- | :--- |
| **Frontend** | React / Next.js, TypeScript, Tailwind CSS | Single Page App / SSR framework choice pending confirmation |
| **Backend Core** | Java, Spring Boot, Spring Security, Spring Cloud Gateway | Modular Monolith establishing strict boundaries |
| **AI Workspace** | Python 3.11+, FastAPI, LangChain, OpenAI/Gemini APIs | Decoupled REST microservice boundary |
| **Databases** | PostgreSQL (Primary RDBMS), MongoDB (Docs/Metadata), Redis (Cache) | Data isolation strategy pending confirmation |
| **Events & Orchestration** | Apache Kafka, Apache Camel, Camunda / Flowable | Asynchronous event bus and workflow engine |
| **Storage** | AWS S3 / Azure Blob Storage | Metadata in DB, binary document assets in Object Storage |
| **Infrastructure** | Docker, Kubernetes, Nginx, GitHub Actions | Containerized deployment pipeline |

---

## Repository Structure

```
sofzenix-esign-platform/
├── README.md                           # Root documentation & vision
├── LICENSE                             # Apache License 2.0
├── .gitignore                          # Git ignore configuration
├── .env.example                        # Environment variables template
├── docker-compose.yml                  # Local development compose scaffold
├── frontend/                           # React / Next.js + TS frontend scaffold
├── backend/                            # Spring Boot core backend modular scaffold
├── ai/                                 # Python / FastAPI AI service workspace scaffold
├── database/                           # Database schema, migration & ERD guides
├── integrations/                       # Integration connectors boundary
├── docs/                               # Architecture, module, API & security specs
├── deployment/                         # Infrastructure & Kubernetes manifests scaffold
├── tests/                              # Testing strategy and test suites scaffold
└── .github/workflows/                  # GitHub Actions CI/CD workflows scaffold
```

---

## Development Philosophy & Architectural Principles

1. **Modular Boundaries First**: Enforce strict module isolation within the backend codebase. Service decomposition into standalone microservices will be evaluated after scalability requirements dictate.
2. **Separation of Concerns**: Controllers remain thin; Services own business logic; Repositories handle persistence.
3. **Decoupled AI & Storage**: Metadata stays in PostgreSQL/MongoDB; file binaries stay in Object Storage. AI operates as a isolated HTTP service boundary.
4. **Event-Driven Asynchrony**: Asynchronous tasks (OCR, email dispatches, webhook calls) are processed via event queues (Kafka).
5. **Security at Every Layer**: Multi-tenant isolation, RBAC, encryption at rest/transit, and immutable audit logs.

---

## Local Development Scaffold

Local development services are provisioned via Docker Compose:

```bash
# Start infrastructure containers (PostgreSQL, Redis, Kafka, AI, Backend, Frontend)
docker-compose up -d
```

For detailed setup instructions, see [`docs/deployment/local-development.md`](file:///Users/anshulk/Downloads/sofzenix-esign-platform/docs/deployment/local-development.md).

---

## Future Implementation Roadmap

- **Phase 1**: Architecture, Domain Modeling, Database Schema Design, API Contracts, Security Specifications.
- **Phase 2**: Core Identity & Multi-Tenant Organization, Document Management Baseline.
- **Phase 3**: Document Generation Engine, eSignature & Digital Certificate Processing.
- **Phase 4**: Workflow Engine & Approval Routing Matrix.
- **Phase 5**: Multi-Channel Communication Hub (Email, WhatsApp, SMS).
- **Phase 6**: AI Service Integration (OCR, Entity Extraction, Clause Analysis).
- **Phase 7**: Enterprise Integrations Platform (CRM, HRIS, Cloud Storage).
- **Phase 8**: Analytics, Audit Trail Engine, Administrative Console.
- **Phase 9**: Multi-Tenant SaaS Billing & Metering Engine.
- **Phase 10**: Production Hardening, Observability, K8s Deployment & Security Audit.
