# SaaS Billing Module (`backend/billing`)

## Architectural Boundary
Manages multi-tenant subscription tiers (Free, Starter, Professional, Enterprise), feature flag entitlement checks, usage metering (signature count, storage volume), GST tax invoice generation, renewal reminders, and payment gateway webhooks.

## Layer Structure
- `controller/`: Subscription management & billing web controllers.
- `service/`: SubscriptionService, UsageMeterService, TaxInvoiceGenerator.
- `repository/`: Subscription, Plan, Invoice JPA repositories.
- `model/`: Plan, Subscription, MeteredUsage, Invoice.
- `dto/`: CheckoutSessionDTO, SubscriptionUpdateDTO.
- `config/`: Payment gateway client configuration.
- `exception/`: EntitlementExceededException, PaymentFailedException.
- `test/`: Subscription tier entitlement tests.

> Status: Scaffolding baseline. No domain entities or fake API endpoints implemented.
