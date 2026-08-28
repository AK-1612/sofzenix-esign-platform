# Sofzenix eSign - AI Workspace & Service Boundary

> Python / FastAPI Microservice Workspace for AI & Document Intelligence.

---

## Architectural Boundary

The `ai/` workspace is designed as an autonomous service boundary separate from the primary Java backend. It provides specialized machine learning and document intelligence capabilities via HTTP REST endpoints and asynchronous Kafka event consumers.

### Key Capabilities & Submodules
- `ocr/`: Optical Character Recognition & PDF text layer extraction.
- `classification/`: Document type taxonomy classification (Invoice, NDA, Employment Contract, MSA).
- `extraction/`: Named Entity Recognition (NER), key-value pair extraction (Dates, Amounts, Parties, Tax IDs).
- `contract_analysis/`: Legal clause segmentation and compliance validation.
- `risk_detection/`: Automated risk scoring for non-standard indemnity or termination clauses.
- `smart_search/`: Vector embeddings, HNSW index management, semantic hybrid search.
- `assistant/`: LLM conversational agent for document QA and drafting assistance.
- `common/`: Shared utilities, base models, Pydantic schemas, logging setup.

---

## Technology Stack
- **Framework**: Python 3.11+, FastAPI, Uvicorn
- **AI / LLM Orchestration**: LangChain / LlamaIndex, OpenAI / Gemini API Clients
- **Document Processing**: PyPDF, Tesseract OCR / PDFPlumber, Unstructured
- **Vector Search**: FAISS / Qdrant client

---

## Service Communication Contract

> [!NOTE]
> Communication between the Java Backend and Python AI services will occur via:
> 1. **Synchronous REST API**: High-priority interactive requests (e.g. AI Assistant, Risk Analysis preview).
> 2. **Asynchronous Kafka Events**: Heavy background tasks (e.g. Bulk OCR, Document Classification, Vector Indexing).
>
> Exact API schemas and protobuf/JSON payload contracts will be finalized during API design.
