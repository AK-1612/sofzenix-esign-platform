-- ==============================================================================
-- SOFZENIX ESIGN PLATFORM - FLYWAY SCHEMA MIGRATION V2
-- AI Call Automation from Excel: Leads & Call Results
-- Enforces Multi-Tenant Isolation via organization_id Discriminator
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==============================================================================
-- 1. LEADS TABLE
-- One row per lead imported from an Excel sheet (Name, Service, Budget, City)
-- ==============================================================================
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    service VARCHAR(255) NULL,
    budget VARCHAR(100) NULL,
    city VARCHAR(120) NULL,
    source_file_name VARCHAR(500) NULL,
    call_status VARCHAR(30) NOT NULL DEFAULT 'NOT_CALLED',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by UUID NULL,
    deleted_at TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT chk_lead_call_status CHECK (call_status IN (
        'NOT_CALLED', 'CALLING', 'CONNECTED', 'NO_ANSWER', 'BUSY', 'FAILED',
        'INTERESTED', 'NOT_INTERESTED', 'FOLLOW_UP', 'APPOINTMENT', 'CONVERTED'
    ))
);

CREATE INDEX idx_leads_org_status ON leads(organization_id, call_status) WHERE deleted_at IS NULL;
CREATE INDEX idx_leads_org_mobile ON leads(organization_id, mobile) WHERE deleted_at IS NULL;

-- ==============================================================================
-- 2. CALL_RESULTS TABLE
-- Automatically written after every AI call attempt for a lead
-- ==============================================================================
CREATE TABLE call_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    call_status VARCHAR(30) NOT NULL DEFAULT 'NOT_CALLED',
    duration_seconds INT NOT NULL DEFAULT 0,
    interest VARCHAR(20) NOT NULL DEFAULT 'NONE',
    score SMALLINT NULL CHECK (score BETWEEN 0 AND 100),
    next_action VARCHAR(120) NOT NULL DEFAULT 'Call Lead',
    transcript TEXT NULL,
    notes TEXT NULL,
    ai_prompt_snapshot JSONB NULL,
    attempted_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_call_result_status CHECK (call_status IN (
        'NOT_CALLED', 'CALLING', 'CONNECTED', 'NO_ANSWER', 'BUSY', 'FAILED',
        'INTERESTED', 'NOT_INTERESTED', 'FOLLOW_UP', 'APPOINTMENT', 'CONVERTED'
    )),
    CONSTRAINT chk_call_result_interest CHECK (interest IN ('HIGH', 'MEDIUM', 'LOW', 'NONE'))
);

CREATE INDEX idx_call_results_org_status ON call_results(organization_id, call_status);
CREATE INDEX idx_call_results_lead ON call_results(lead_id);
CREATE INDEX idx_call_results_score ON call_results(score DESC NULLS LAST);

-- Keep leads.call_status in sync whenever a new call result is recorded.
CREATE OR REPLACE FUNCTION sync_lead_call_status() RETURNS TRIGGER AS $$
BEGIN
    UPDATE leads SET call_status = NEW.call_status, updated_at = NOW() WHERE id = NEW.lead_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_lead_call_status
AFTER INSERT OR UPDATE ON call_results
FOR EACH ROW EXECUTE FUNCTION sync_lead_call_status();
