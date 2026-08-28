# Identity & Organization Module (`backend/identity`)

## Architectural Boundary
This module manages multi-tenant hierarchy, organization structures (Branches, Departments, Teams), user identities, roles, RBAC permissions, and tenant context propagation.

## Layer Structure
- `controller/`: Tenant & user admin API endpoints.
- `service/`: RBAC validation, tenant isolation context, user lifecycle.
- `repository/`: User and organization persistence interfaces.
- `model/`: Entity boundaries (Organization, User, Role, Permission).
- `dto/`: Request/Response data transfer objects.
- `config/`: Security permission evaluators.
- `exception/`: TenantNotFoundException, AccessDeniedException.
- `test/`: Identity module unit & integration tests.

> Status: Scaffolding baseline. No domain entities or fake API endpoints implemented.
