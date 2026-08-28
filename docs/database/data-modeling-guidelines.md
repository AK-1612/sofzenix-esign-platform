# Data Modeling Guidelines

---

## 1. Multi-Tenancy Data Isolation Rules

Every database table representing tenant data must strictly enforce isolation rules:

1. **Discriminator Column**: Every table must contain an `organization_id UUID NOT NULL` indexed column when using shared schema multi-tenancy.
2. **PostgreSQL Row-Level Security (RLS)**: Enforce RLS policies ensuring database connections set to `SET app.current_tenant = '<org_id>'` cannot query or mutate records belonging to other tenants.
3. **Foreign Key Integrity**: Foreign keys referencing tenant entities must validate that both parent and child belong to the same `organization_id`.

---

## 2. Polyglot Persistence Mapping Strategy

- **PostgreSQL**: Transactional entities (Users, Organizations, Roles, Document Metadata, Workflow Instances, Signature Certificates, Audit Logs).
- **MongoDB**: Unstructured/dynamic data (Form field JSON schemas, AI extraction outputs, dynamic template field mappings).
- **Redis**: Key-value cache with strict TTL expiration (JWT revocation list, OTP codes, session state, rate-limiting tokens).

---

## 3. Auditing & Soft Delete Conventions

- Standard columns for PostgreSQL tables:
  - `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
  - `organization_id UUID NOT NULL`
  - `created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()`
  - `updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()`
  - `created_by UUID NOT NULL`
  - `updated_by UUID NOT NULL`
  - `deleted_at TIMESTAMP WITH TIME ZONE NULL` (Soft delete flag)
