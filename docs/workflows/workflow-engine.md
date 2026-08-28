# Workflow Engine & Event Automation Architecture

---

## 1. Workflow Engine Concept

The workflow engine models business document routing as a deterministic state machine:

```
[DRAFT] ──► [REVIEW] ──► [APPROVED] ──► [SIGNING] ──► [COMPLETED] ──► [VAULTED]
   │           │            │              │              │
   ▼           ▼            ▼              ▼              ▼
[REJECTED]  [EXPIRED]   [DELEGATED]    [RECALLED]     [ARCHIVED]
```

---

## 2. Event-Driven Automation Pipeline

State transitions emit domain events to Kafka, triggering downstream automated actions:

```
Domain Event                    Target Consumer Action
─────────────────────────────────────────────────────────────────────────────
`document.uploaded`          ➔ Trigger AI OCR & Keyword Extraction
`document.approved`          ➔ Dispatch Signature Request to Recipient 1
`signature.completed`        ➔ Check Signer Order ➔ If Pending: Dispatch to Recipient 2
                                                   ➔ If Last: Generate Completion Cert
`workflow.completed`         ➔ Move to Immutable Object Vault & Trigger Webhooks
`document.expired`           ➔ Send Expiry Alert & Revoke Signing Link
`payment.success`            ➔ Activate SaaS Subscription Plan Entitlements
```

---

## 3. Approval Routing Matrix & Escalation

- **Department Rules**: Approvals dynamically routed based on entity attributes (`department == 'LEGAL'`, `contract_value > 50000 USD`).
- **SLA Escalation**: If an approval step remains pending beyond `escalation_hours` (e.g. 24 hours), the workflow engine automatically reassigns the task to the designated fallback manager or dispatches reminder alerts via WhatsApp/SMS.
