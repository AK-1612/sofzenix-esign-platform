# AI Service Boundary Client Layers

- `controller/`: Internal triggers for manual AI analysis.
- `service/`: AI HTTP Client (WebClient) and Kafka event publishing services.
- `repository/`: AI metadata storage interfaces.
- `model/`: AI extraction domain boundaries.
- `dto/`: AI Request/Response payload wrappers.
- `config/`: Connection timeouts & retry backoff config.
- `exception/`: AI client exceptions.
- `test/`: Mocked AI service client test cases.
