# Technical Architecture & Pipeline Design: Modules 2 & 3

> **Module 2: Document Management** & **Module 3: Document Generation**
> End-to-End Deep-Dive Architecture & Data Pipeline Specification.

---

## 1. Object Storage Architecture & KMS Envelope Encryption

Document binaries are stored strictly in Object Storage (AWS S3 / Azure Blob Storage). Metadata and storage keys are stored in PostgreSQL.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            UPLOAD PIPELINE                                  │
│                                                                             │
│  Client ──► Request Presigned URL ──► Document Service                      │
│                                             │ Generates AWS S3 KMS Presigned URL│
│  Client ──► Direct S3 Upload (AES-256) ◄────┘                               │
│    │                                                                        │
│    └──────► Complete Upload Webhook ──► Register `DocumentVersion` Record  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Storage Key Partitioning Scheme
```
s3://{bucket-name}/tenants/{organization_id}/documents/{document_id}/v{version_number}/{checksum_sha256}.pdf
```

### Security & Access Control
- All objects are encrypted using AWS KMS Customer Managed Keys (CMK) / SSE-KMS.
- Direct public bucket access is prohibited (`BlockPublicAccess: true`).
- Client downloads utilize short-lived time-bounded presigned GET URLs (TTL <= 15 minutes).

---

## 2. Document Generation Engine & PDF Rendering Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PDF COMPILATION PIPELINE                             │
│                                                                             │
│ ┌────────────────┐     ┌──────────────────┐     ┌────────────────────────┐ │
│ │ HTML Template  ├────►│ Data Merge Engine├────►│ CSS Paged Media Render │ │
│ └────────────────┘     └──────────────────┘     └───────────┬────────────┘ │
│                                                             │ Raw PDF      │
│ ┌────────────────┐     ┌──────────────────┐                 ▼              │
│ │ QR Verification│────►│ Watermark Overlay├────► Final PDF Output Stream   │
│ └────────────────┘     └──────────────────┘                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### CSS Paged Media Standard for Templates
Templates enforce standard print page formatting:

```css
@page {
    size: A4 portrait;
    margin: 20mm 15mm 20mm 15mm;
    @top-right { content: element(header); }
    @bottom-center { content: "Page " counter(page) " of " counter(pages); }
}
div.header { position: running(header); }
```

### QR Code Verification Link Placement
- QR codes encode an immutable SHA-256 document verification link:
  `https://esign.sofzenix.com/verify?docId={doc_id}&hash={checksum_sha256}`
- Placed on the bottom-right footer of generated PDF documents.

---

## 3. Kafka Event Streaming Payload Schemas

Modules 2 and 3 publish event notifications to Apache Kafka for asynchronous automation downstream.

### Event 1: `document.uploaded`
- **Topic**: `sofzenix.documents.uploaded`
- **Payload**:
```json
{
  "eventId": "evt_99812489",
  "eventType": "DOCUMENT_UPLOADED",
  "timestamp": "2026-08-28T11:45:00Z",
  "organizationId": "a1b2c3d4-0000-0000-0000-000000000001",
  "documentId": "d1e2f3a4-1111-1111-1111-111111111111",
  "versionId": "v1e2f3a4-2222-2222-2222-222222222222",
  "versionNumber": 1,
  "fileSizeBytes": 2048500,
  "checksumSha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "uploadedBy": "u1b2c3d4-3333-3333-3333-333333333333"
}
```

### Event 2: `document.generated`
- **Topic**: `sofzenix.documents.generated`
- **Payload**:
```json
{
  "eventId": "evt_99812490",
  "eventType": "DOCUMENT_GENERATED",
  "timestamp": "2026-08-28T11:45:05Z",
  "organizationId": "a1b2c3d4-0000-0000-0000-000000000001",
  "documentId": "d1e2f3a4-1111-1111-1111-111111111111",
  "templateId": "t1e2f3a4-4444-4444-4444-444444444444",
  "generationJobId": null,
  "watermarkApplied": "DRAFT",
  "generatedBy": "u1b2c3d4-3333-3333-3333-333333333333"
}
```

### Event 3: `document.expired`
- **Topic**: `sofzenix.documents.expired`
- **Payload**:
```json
{
  "eventId": "evt_99812491",
  "eventType": "DOCUMENT_EXPIRED",
  "timestamp": "2026-08-28T11:45:10Z",
  "organizationId": "a1b2c3d4-0000-0000-0000-000000000001",
  "documentId": "d1e2f3a4-1111-1111-1111-111111111111",
  "expiredAt": "2026-08-28T11:45:10Z"
}
```
