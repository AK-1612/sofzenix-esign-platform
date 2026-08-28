# AI Service Boundary Client (`backend/ai`)

## Architectural Boundary
Serves as the internal backend gateway client communicating with the external Python AI Workspace microservice (`ai/`). Manages async event publishing to Kafka for OCR/Extraction and REST RPC calls for contract analysis.

## Layer Structure
- `controller/`: Internal endpoints for triggering manual AI analysis.
- `service/`: AI HTTP Client (WebClient), Kafka event publisher, result mapper.
- `repository/`: AI extraction metadata storage.
- `model/`: ExtractionResult, RiskReport.
- `dto/`: AI Request/Response wrappers.
- `config/`: AI client connection timeouts & retry backoff config.
- `exception/`: AIServiceUnavailableException.
- `test/`: Mocked AI service client tests.

> Status: Scaffolding baseline. No domain entities or fake API endpoints implemented.
