# Integrations & API Platform Module (`backend/integrations`)

## Architectural Boundary
Manages public REST API rate limiting, webhook subscription registration, signature payload signing, and outbound enterprise connector handlers (Salesforce, HubSpot, Zoho, HRIS systems).

## Layer Structure
- `controller/`: Webhook management & public API controllers.
- `service/`: WebhookDispatcherService, OAuth Integration Handlers.
- `repository/`: WebhookSubscription, IntegrationCredential repositories.
- `model/`: WebhookSubscription, WebhookEventLog.
- `dto/`: EventPayload DTOs.
- `config/`: Connector OAuth2 configuration.
- `exception/`: WebhookDeliveryFailedException.
- `test/`: Webhook payload verification tests.

> Status: Scaffolding baseline. No domain entities or fake API endpoints implemented.
