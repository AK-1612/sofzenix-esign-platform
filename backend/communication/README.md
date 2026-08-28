# Communication Hub Module (`backend/communication`)

## Architectural Boundary
Manages multi-channel notification dispatch across Email (SMTP, SendGrid), WhatsApp Business API, and SMS gateways. Responsible for signature invitations, approval notifications, reminders, OTP delivery, and expiry alerts.

## Layer Structure
- `controller/`: Communication log & retry web controllers.
- `service/`: EmailService, WhatsAppService, SMSService, Provider Fallback Router.
- `repository/`: CommunicationLog JPA repositories.
- `model/`: NotificationMessage, Template, DispatchStatus.
- `dto/`: SendMessageRequest, DeliveryStatusDTO.
- `config/`: Gateway credentials & template engine setup.
- `exception/`: NotificationDeliveryException.
- `test/`: Mock gateway delivery tests.

> Status: Scaffolding baseline. No domain entities or fake API endpoints implemented.
