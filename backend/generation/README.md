# Document Generation Module (`backend/generation`)

## Architectural Boundary
Manages document templates, dynamic field merge engines, automated contract generation, bulk generation pipelines, PDF compilation, QR code generation, and watermarking.

## Layer Structure
- `controller/`: Template administration & generation triggers.
- `service/`: PDF compiler service, merge engine, QR code generator.
- `repository/`: Template persistence layer.
- `model/`: Template entity, MergeField definition.
- `dto/`: Generation request payloads.
- `config/`: PDF engine configuration.
- `exception/`: TemplateRenderException.
- `test/`: PDF generation tests.

> Status: Scaffolding baseline. No domain entities or fake API endpoints implemented.
