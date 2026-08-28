# REST API Guidelines & Standards

---

## 1. Architectural Principles

1. **RESTful Resource Modeling**: Standard URL structures (`/api/v1/documents`, `/api/v1/workflows`).
2. **HTTP Verb Conventions**:
   - `GET`: Retrieve resource or collection.
   - `POST`: Create new resource or trigger action execution.
   - `PUT`: Replace resource completely.
   - `PATCH`: Partial resource updates.
   - `DELETE`: Soft delete resource.
3. **Stateless Bearer Authentication**: Requests must include `Authorization: Bearer <JWT>` headers.
4. **Tenant Isolation Context**: `X-Tenant-ID` header required on all internal microservice calls.

---

## 2. Standard Response Envelope

All API endpoints must return a consistent JSON response envelope:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Operation completed successfully",
  "data": {},
  "error": null,
  "timestamp": "2026-08-28T11:15:00Z"
}
```

Standard Error Envelope:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Validation failed",
  "data": null,
  "error": {
    "code": "INVALID_SIGNER_EMAIL",
    "details": "The specified recipient email address format is invalid",
    "fieldErrors": [
      {
        "field": "signerEmail",
        "message": "Must be a valid email address"
      }
    ]
  },
  "timestamp": "2026-08-28T11:15:00Z"
}
```

---

## 3. Versioning & Deprecation

- Versioning strategy: URL path prefix (`/api/v1/`, `/api/v2/`).
- Deprecation policy: `Deprecation: true` and `Sunset: <date>` HTTP response headers.
