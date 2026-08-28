# Services Directory (`frontend/src/services`)

This directory will encapsulate all API communication abstractions:
- `apiClient.ts`: Base HTTP client instance with authorization interceptors and error handling.
- `documentService.ts`: Document upload, metadata retrieval, and preview calls.
- `esignService.ts`: Signature placement, OTP verification, and certificate downloading.
- `workflowService.ts`: Workflow definition CRUD and step action execution.
- `aiService.ts`: Contract extraction and risk assessment API triggers.
