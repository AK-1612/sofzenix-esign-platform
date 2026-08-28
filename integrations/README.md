# Integration Connectors Boundary (`integrations/`)

---

## Architecture Overview

The `integrations/` boundary isolates external third-party API clients, software service SDKs, and outbound notification channels from core domain logic.

### Integration Modules
- `crm/`: Enterprise CRM connectors (Salesforce, HubSpot, Zoho CRM, Microsoft Dynamics).
- `hr/`: HRIS platform connectors (Workday, BambooHR, Darwinbox).
- `email/`: Transactional email provider gateways (SMTP, SendGrid, Mailgun, AWS SES).
- `whatsapp/`: WhatsApp Business API messaging gateway adapters.
- `sms/`: Twilio / SMS Gateway OTP and notification dispatchers.
- `storage/`: Object storage client adapters (AWS S3, Azure Blob Storage, Google Cloud Storage).

> [!NOTE]
> All integration adapters are currently architectural scaffolds. Concrete API client implementations will be built during the Integration Phase.
