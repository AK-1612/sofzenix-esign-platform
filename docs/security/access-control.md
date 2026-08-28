# Access Control & Multi-Tenancy Security (`access-control`)

---

## 1. Role-Based Access Control (RBAC) Matrix

| System Role | Scope | Permissions |
| :--- | :--- | :--- |
| **SuperAdmin** | Platform Global | Infrastructure telemetry, system configuration, global tenant monitoring. |
| **OrgAdmin** | Tenant Organization | Manage tenant users, roles, departments, billing plans, integrations. |
| **DeptManager**| Department / Team | Create templates, configure workflows, view team document analytics. |
| **StandardUser**| Personal / Assigned | Upload documents, trigger generation, request signatures, sign documents. |
| **ExternalSigner**| Single Document Token | One-time access token to view and sign specific assigned document. |

---

## 2. Multi-Tenant Logical Isolation Guarantee

> **CRITICAL RULE**: Organization A must NEVER be able to query, mutate, or view Organization B's data under any circumstances.

- Every REST endpoint evaluates the caller's JWT claims (`org_id`, `user_id`, `roles`).
- Database repositories inject `WHERE organization_id = :orgId` or enforce PostgreSQL Row-Level Security (RLS).
- Object Storage paths are partitioned by organization UUID (`s3://bucket/tenants/{org_id}/documents/{doc_id}.pdf`).
