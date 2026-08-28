# System Architecture Specification

> Sofzenix eSign & Intelligent Document Automation Platform

---

## 1. High-Level Architecture Overview

The platform is designed as a cloud-native, multi-tenant document lifecycle automation system. It combines a **Spring Boot Modular Monolith** for backend domain orchestration with a **Python FastAPI Workspace** for AI/ML capabilities, a **React/Next.js Single-Page Application** for frontend user experiences, and **Apache Kafka** for asynchronous event streaming.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT / FRONTEND TIER                             │
│                  Web SPA (React / Next.js + TS + Tailwind CSS)                  │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ HTTPS / WSS
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               API GATEWAY LAYER                                 │
│                   Spring Cloud Gateway (Rate Limit, CORS, Auth)                 │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
┌───────────────────────────────────────┐ ┌───────────────────────────────────────┐
│        SPRING BOOT BACKEND            │ │           PYTHON AI WORKSPACE         │
│         (Modular Monolith)            │ │          (FastAPI Microservice)      │
│                                       │ │                                       │
│ ┌───────────────────────────────────┐ │ │ ┌───────────────────────────────────┐ │
│ │ Identity & Organization           │ │ │ │ OCR & Text Layer Extraction       │ │
│ │ Document Management               │ │ │ │ Document Taxonomy Classification  │ │
│ │ Document Generation Engine        │ │ │ │ Entity & Key-Value Extraction     │ │
│ │ eSignature & PKI Certificate      │ │ │ │ Legal Contract Clause Analysis    │ │
│ │ Workflow & Approval Engine        │ │ │ │ Clause Risk Detection Engine      │ │
│ │ Communication Hub                 │ │ │ │ Vector Hybrid Smart Search        │ │
│ │ Integration & API Platform        │ │ │ │ Conversational AI Assistant       │ │
│ │ Analytics & Audit Trail           │ │ │ └───────────────────────────────────┘ │
│ │ Multi-Tenant SaaS Billing         │ │ └───────────────────┬───────────────────┘
│ └───────────────────────────────────┘ │                     │
└───────────────────┬───────────────────┘                     │
                    │                                         │
                    ├────────────────────┬────────────────────┘
                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                             EVENT BUS & ORCHESTRATION                           │
│                      Apache Kafka Event Streaming Topics                        │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
┌──────────────┐                 ┌──────────────┐                 ┌──────────────┐
│  POSTGRESQL  │                 │   MONGODB    │                 │    REDIS     │
│(Primary RDBMS│                 │ (Dynamic Doc │                 │ (Token/Cache │
│  Metadata)   │                 │  & AI Data)  │                 │  State Store)│
└──────────────┘                 └──────────────┘                 └──────────────┘
```

---

## 2. Platform Core Architecture Principles

1. **Modular Boundaries First**: Enforce strict package boundaries within the Spring Boot application. Service decomposition into separate microservices will occur only when validated by domain scale or deployment requirements.
2. **Document-Centric State Machine**: Every document transitions through explicit lifecycle states (`CREATE` ➔ `GENERATE` ➔ `REVIEW` ➔ `APPROVE` ➔ `SIGN` ➔ `STORE` ➔ `AUDIT` ➔ `ANALYZE` ➔ `ARCHIVE` ➔ `EXPIRE`).
3. **Decoupled AI Engine**: Artificial Intelligence operations operate as an isolated service boundary, preventing ML compute spikes from impacting core transactional API performance.
4. **Binary & Metadata Separation**: Operational relational metadata resides in PostgreSQL; dynamic document structures in MongoDB; binary PDF assets reside strictly in Object Storage (S3/Blob).
5. **Event-Driven Automation**: Non-blocking asynchronous tasks (email dispatches, webhook delivery, OCR processing, index generation) execute via Apache Kafka topics.
6. **Strict Multi-Tenancy**: Data isolation between organizations is guaranteed across API routes, cache keys, database queries, and storage buckets.

---

## 3. Technology Stack Baseline

| Tier | Component | Technology | Rationale |
| :--- | :--- | :--- | :--- |
| **Frontend** | UI Framework | React / Next.js, TypeScript | Reactive client interface with strong static typing. |
| | Styling | Tailwind CSS | Utility-first responsive design system. |
| **Backend Core** | Runtime / Framework | Java 17+, Spring Boot 3.x | Enterprise transactional stability, Spring ecosystem. |
| | Security | Spring Security, OAuth2, JWT | Stateless token validation and RBAC checks. |
| | Gateway | Spring Cloud Gateway | Unified routing, rate-limiting, CORS handling. |
| **AI Workspace** | Service Runtime | Python 3.11+, FastAPI | Native Python ML/AI ecosystem compatibility. |
| | Frameworks | LangChain, OpenAI / Gemini APIs | LLM orchestration and vector embeddings. |
| **Persistence** | Primary Relational | PostgreSQL 15+ | Multi-tenant ACID relational transaction integrity. |
| | Semi-Structured | MongoDB | Dynamic document metadata and extraction payloads. |
| | Cache & Session | Redis | Session state, rate limits, token revocation lists. |
| **Messaging** | Event Bus | Apache Kafka | High-throughput async message streaming. |
| | Enterprise Integration| Apache Camel | Third-party EIP routing and connectors. |
| | Workflow Engine | Camunda / Flowable | BPMN 2.0 compliant approval engine. |
| **Storage** | Object Storage | AWS S3 / Azure Blob Storage | High durability binary PDF storage. |
| **Infrastructure** | Containerization | Docker, Kubernetes, Nginx | Portable deployment and horizontal scaling. |
