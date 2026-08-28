# AI Microservice Architecture

---

## 1. Service Isolation Model

The AI workspace operates as a dedicated Python FastAPI service boundary:

```
┌───────────────────────────────────────┐
│          JAVA BACKEND CORE            │
└───────────────────┬───────────────────┘
                    │
          ┌─────────┴─────────┐
          │ Synchronous HTTP  │ Asynchronous Kafka
          ▼                   ▼
┌───────────────────────────────────────┐
│         FASTAPI AI SERVICE            │
│  ┌─────────────────────────────────┐  │
│  │ OCR / PyPDF Text Layer Parser   │  │
│  │ Unstructured Text Chunking      │  │
│  │ LangChain / LlamaIndex Pipeline │  │
│  │ OpenAI / Gemini LLM Connectors  │  │
│  │ FAISS / Qdrant Vector Search    │  │
│  └─────────────────────────────────┘  │
└───────────────────────────────────────┘
```

---

## 2. Asynchronous Heavy Task Processing

For heavy operations (Bulk OCR, Contract Clause Segmentation), the Java Backend emits a Kafka event to `ai.document.process`. The AI Service consumes the event, performs extraction, persists raw vectors in Qdrant, and posts structured results back to `ai.document.completed`.
