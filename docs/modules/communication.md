# Communication Hub Module Specification (`communication`)

---

## 1. Purpose
The Communication Hub module manages multi-channel outbound message dispatch across Email, WhatsApp, and SMS channels for signature invitations, approval alerts, OTP verification, and system reminders.

## 2. Responsibilities
- Email dispatch (SMTP, SendGrid, Mailgun, AWS SES) for invitations, signature requests, and completion certificates.
- WhatsApp messaging (WhatsApp Business API) for instant signature alerts, status updates, and download links.
- SMS dispatch for OTP authentication codes, approval notifications, and reminder alerts.
- Template rendering per communication channel.
- Delivery status tracking, rate-limiting, and provider failover routing.

## 3. Scope
- **In-Scope**: Multi-channel message queuing, template rendering, provider adapters, delivery logging.
- **Out-of-Scope**: Determining *when* a signature request is required (owned by Workflow/eSignature).

## 4. Dependencies
- Redis for message rate limiting and OTP expiration TTL.

## 5. External Integrations
- Transactional Email Services (SendGrid, Mailgun, AWS SES).
- WhatsApp Business API Providers.
- SMS Provider Gateways (Twilio, Kaleyra).

## 6. Future Capabilities
- Smart channel preference routing based on historical user response rates (e.g. fallback to WhatsApp if Email unread after 2 hours).

## 7. Open Questions
- Decision pending on primary WhatsApp Business API aggregator.
