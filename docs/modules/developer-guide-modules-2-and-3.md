# Developer Ownership Blueprint: Modules 2 & 3

> **Module 2: Document Management** & **Module 3: Document Generation**
> Targeted Developer Implementation Roadmap & Architectural Boundary Specification.

---

## 1. Overview & Scope of Ownership

As the assigned owner for **Module 2 (Document Management)** and **Module 3 (Document Generation)**, your responsibility spans the entire core engine responsible for creating, rendering, storing, versioning, tagging, indexing, and vaulting documents across the Sofzenix platform.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       MODULE 3: DOCUMENT GENERATION                             │
│                                                                                 │
│   Template Library ──► Data Merge Engine ──► PDF Compiler ──► Watermark / QR    │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ Generated PDF Binary & Metadata
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       MODULE 2: DOCUMENT MANAGEMENT                             │
│                                                                                 │
│   Upload / Ingestion ──► Version Control ──► Object Storage ──► Tag & Archive   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Breakdown: Module 2 (Document Management)

### Responsibilities
1. **Document Ingestion & File Upload**: Accept raw PDF/binary uploads, calculate SHA-256 checksums, validate MIME types and file sizes.
2. **Metadata & Custom Fields**: Store structured metadata (title, description, tenant org ID, folder ID, status, tags, custom key-value metadata pairs).
3. **Folder Hierarchies**: Manage nested directory trees per organization for document organization.
4. **Version Control**: Track document versions (`v1.0`, `v1.1`, `v2.0`). Every update creates a new immutable version record while preserving historical versions.
5. **Search & Index Triggers**: Publish `document.metadata.updated` events to Kafka so AI and search engines update vector and keyword indexes.
6. **Archival & Expiry Lifecycle**: Monitor document retention SLAs, manage soft deletes, automatically mark documents as `EXPIRED` or transition to cold storage (`S3 Glacier`).
7. **Storage Provider Abstraction**: Interact with Object Storage through clean repository interfaces (`ObjectStorageAdapter`).
8. **Duplicate Detection**: Perform hash-based duplicate checks upon upload.

### Core Domain Entities (To Be Modeled in Phase 1)
- `Document`: Primary document aggregate root (`id`, `organization_id`, `title`, `current_version_id`, `status`, `folder_id`, `created_at`).
- `DocumentVersion`: Immutable snapshot (`id`, `document_id`, `version_number`, `storage_path`, `checksum`, `file_size_bytes`, `mime_type`).
- `Folder`: Hierarchical folder structure (`id`, `organization_id`, `name`, `parent_folder_id`).
- `DocumentTag`: Tag assignment entity (`document_id`, `tag_name`, `color_code`).

### Code Package Location
- Backend: [`backend/documents/`](file:///Users/anshulk/Downloads/sofzenix-esign-platform/backend/documents)
- Documentation: [`docs/modules/documents.md`](file:///Users/anshulk/Downloads/sofzenix-esign-platform/docs/modules/documents.md)

---

## 3. Detailed Breakdown: Module 3 (Document Generation)

### Responsibilities
1. **Template Engine Management**: Manage document templates (HTML/Handlebars templates, DOCX templates, field definitions, dynamic markers).
2. **Dynamic Data Merge Engine**: Substitute dynamic field tokens (`{{candidate_name}}`, `{{contract_value}}`) with runtime payloads from forms, CRMs, or ERPs.
3. **PDF Generation & Compiler**: Compile HTML/CSS or DOM representations into high-fidelity PDF documents.
4. **Bulk Batch Generation**: Execute background batch generation jobs for high-volume contract or invoice creation via Kafka events.
5. **QR Code Generation**: Render dynamic verification QR codes on PDF footers linking to document validation URLs.
6. **Dynamic Watermarking**: Overlay dynamic stamps ("DRAFT", "CONFIDENTIAL", "EXPIRED", Tenant Logos) on PDF pages.
7. **AI Drafting Interface**: Integrate with AI Module for automated template generation and smart drafting suggestions.

### Core Domain Entities (To Be Modeled in Phase 1)
- `DocumentTemplate`: Template definition (`id`, `organization_id`, `name`, `template_type`, `content_body`, `status`).
- `TemplateField`: Dynamic field marker schema (`id`, `template_id`, `field_key`, `field_type`, `is_required`, `default_value`).
- `GenerationJob`: Bulk batch generation tracking (`id`, `organization_id`, `template_id`, `total_records`, `processed_records`, `status`).

### Code Package Location
- Backend: [`backend/generation/`](file:///Users/anshulk/Downloads/sofzenix-esign-platform/backend/generation)
- Documentation: [`docs/modules/generation.md`](file:///Users/anshulk/Downloads/sofzenix-esign-platform/docs/modules/generation.md)

---

## 4. Key Handshake & Integration Points Between Module 2 & 3

1. **Generation-to-Management Handoff**:
   - Module 3 compiles a PDF from a template and payload ➔ Module 3 invokes Module 2's `DocumentService.createDocumentFromBinary()` ➔ Module 2 stores the binary in S3, creates the metadata entry, and returns the `Document` object.
2. **Template Document Versioning**:
   - When a generated document is edited or regenerated, Module 3 generates the new PDF binary ➔ Module 2 handles creating `DocumentVersion v2.0` attached to the same parent `Document`.
3. **Watermark & Expiry Lifecycle**:
   - When Module 2 updates a document state to `EXPIRED` or `DRAFT`, it can request Module 3's watermarking utility to apply a "DRAFT" or "EXPIRED" stamp overlay to PDF previews.

---

## 5. Recommended Next Implementation Steps for Your Assigned Modules

1. **Domain Modeling & ERD Schema**: Define explicit Java domain entity classes and DDL tables for `Document`, `DocumentVersion`, `Folder`, `DocumentTag`, `DocumentTemplate`, `TemplateField`.
2. **API Contract Specification**: Draft OpenAPI 3.0 REST endpoints for Document Management (`/api/v1/documents/*`) and Document Generation (`/api/v1/templates/*`).
3. **Storage & Compiler Strategy Selection**:
   - Select and benchmark the PDF compiler library (e.g. OpenHTMLToPDF / Flying Saucer / iText vs. Headless Chrome).
   - Finalize the S3 Object Storage key naming convention (`s3://{bucket}/tenants/{org_id}/documents/{doc_id}/v{version_num}.pdf`).
