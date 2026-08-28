# Platform Test Suites & Strategy (`tests/`)

---

## Test Architecture Overview

The testing directory anchors cross-cutting end-to-end integration, performance, load, security, and API contract test suites.

### Sub-directory Strategy
- `unit/`: Core module unit test reference patterns.
- `integration/`: Cross-module Spring Boot `@SpringBootTest` and Kafka integration tests.
- `e2e/`: Playwright / Cypress browser automation flows for signature capture and workflow steps.
- `performance/`: k6 / JMeter performance & SLA latency load scripts.
- `contract/`: Pact API consumer-driven contract tests between Java Backend and Python AI Service.

> Status: Scaffolding baseline for future test suite implementations.
