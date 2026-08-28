# Analytics, Audit & Administration Module (`backend/analytics`)

## Architectural Boundary
Responsible for capturing immutable, tamper-evident audit trails (IP, User Agent, Geolocation, Timestamp, Action), aggregating organization metrics (document counts, workflow turnaround velocity), and providing administrative telemetry views.

## Layer Structure
- `controller/`: Analytics & Audit log query REST endpoints.
- `service/`: AuditTrailAspect, MetricsAggregatorService, ExportService.
- `repository/`: AuditLog Mongo/JPA repositories.
- `model/`: AuditEntry, DailyMetric.
- `dto/`: AnalyticsFilterDTO, AuditReportDTO.
- `config/`: AspectJ audit interceptor configuration.
- `exception/`: ExportFailedException.
- `test/`: Audit log immutability tests.

> Status: Scaffolding baseline. No domain entities or fake API endpoints implemented.
