# Workflow & Approval Module (`backend/workflow`)

## Architectural Boundary
Powers workflow definition modeling, step transitions, approval matrix evaluation, automated task routing, dynamic escalation, reminder scheduling, and workflow execution tracking.

## Layer Structure
- `controller/`: Workflow definition & execution REST controllers.
- `service/`: Workflow state engine, Approval matrix evaluator, Escalation timer service.
- `repository/`: WorkflowDefinition, WorkflowInstance persistence.
- `model/`: WorkflowInstance, Step, ApprovalRule, EscalationPolicy.
- `dto/`: Action request DTOs (Approve, Reject, Reassign).
- `config/`: Workflow engine (Camunda / Flowable) bean setup.
- `exception/`: InvalidStateTransitionException.
- `test/`: State machine execution tests.

> Status: Scaffolding baseline. No domain entities or fake API endpoints implemented.
