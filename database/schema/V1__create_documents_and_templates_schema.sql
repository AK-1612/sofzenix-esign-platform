-- ==============================================================================
-- SOFZENIX ESIGN PLATFORM - FLYWAY SCHEMA MIGRATION V1
-- Modules 2 & 3: Document Management & Document Generation Schema
-- Enforces Multi-Tenant Isolation via organization_id Discriminator & Row-Level Security (RLS)
-- ==============================================================================

-- Enable UUID extension if not present
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==============================================================================
-- 1. FOLDERS TABLE
-- Stores hierarchical folder structures per organization
-- ==============================================================================
CREATE TABLE folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    parent_folder_id UUID REFERENCES folders(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT uk_folder_org_parent_name UNIQUE (organization_id, parent_folder_id, name)
);

CREATE INDEX idx_folders_org_parent ON folders(organization_id, parent_folder_id) WHERE deleted_at IS NULL;

-- ==============================================================================
-- 2. DOCUMENTS TABLE
-- Primary document aggregate root
-- ==============================================================================
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    folder_id UUID REFERENCES folders(id) ON DELETE SET NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT',
    current_version_number INT NOT NULL DEFAULT 1,
    is_template_generated BOOLEAN NOT NULL DEFAULT FALSE,
    source_template_id UUID NULL,
    retention_expires_at TIMESTAMP WITH TIME ZONE NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT chk_document_status CHECK (status IN ('DRAFT', 'PENDING_REVIEW', 'APPROVED', 'SIGNING', 'SIGNED', 'VAULTED', 'EXPIRED', 'ARCHIVED'))
);

CREATE INDEX idx_documents_org_status ON documents(organization_id, status) WHERE deleted_at IS NULL;
CREATE INDEX idx_documents_org_folder ON documents(organization_id, folder_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_documents_retention ON documents(retention_expires_at) WHERE retention_expires_at IS NOT NULL AND deleted_at IS NULL;

-- ==============================================================================
-- 3. DOCUMENT VERSIONS TABLE
-- Immutable document version snapshot records
-- ==============================================================================
CREATE TABLE document_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL,
    version_number INT NOT NULL,
    storage_provider VARCHAR(50) NOT NULL DEFAULT 'AWS_S3',
    storage_path VARCHAR(1024) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL DEFAULT 'application/pdf',
    checksum_sha256 VARCHAR(64) NOT NULL,
    change_summary VARCHAR(500) NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL,
    CONSTRAINT uk_doc_version UNIQUE (document_id, version_number)
);

CREATE INDEX idx_doc_versions_doc_id ON document_versions(document_id, version_number DESC);
CREATE INDEX idx_doc_versions_checksum ON document_versions(checksum_sha256);

-- Set current_version_id foreign key back on documents table
ALTER TABLE documents ADD COLUMN current_version_id UUID REFERENCES document_versions(id) ON DELETE SET NULL;

-- ==============================================================================
-- 4. DOCUMENT TAGS TABLE
-- Tagging system for metadata categorization
-- ==============================================================================
CREATE TABLE document_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL,
    tag_name VARCHAR(100) NOT NULL,
    color_code VARCHAR(7) NULL DEFAULT '#3B82F6',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL,
    CONSTRAINT uk_doc_tag UNIQUE (document_id, tag_name)
);

CREATE INDEX idx_doc_tags_org_tag ON document_tags(organization_id, tag_name);

-- ==============================================================================
-- 5. DOCUMENT TEMPLATES TABLE
-- Templates for dynamic agreement/contract generation
-- ==============================================================================
CREATE TABLE document_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    template_type VARCHAR(50) NOT NULL DEFAULT 'CONTRACT',
    content_body TEXT NOT NULL, -- HTML / Handlebars markup
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    version_number INT NOT NULL DEFAULT 1,
    header_html TEXT NULL,
    footer_html TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT chk_template_type CHECK (template_type IN ('CONTRACT', 'AGREEMENT', 'OFFER_LETTER', 'INVOICE', 'CUSTOM'))
);

CREATE INDEX idx_templates_org_type ON document_templates(organization_id, template_type) WHERE deleted_at IS NULL AND is_active IS TRUE;

-- ==============================================================================
-- 6. TEMPLATE FIELDS TABLE
-- Dynamic merge field schema markers for templates
-- ==============================================================================
CREATE TABLE template_fields (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID NOT NULL REFERENCES document_templates(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL,
    field_key VARCHAR(100) NOT NULL,
    field_label VARCHAR(255) NOT NULL,
    field_type VARCHAR(50) NOT NULL DEFAULT 'TEXT',
    is_required BOOLEAN NOT NULL DEFAULT TRUE,
    default_value VARCHAR(500) NULL,
    validation_regex VARCHAR(500) NULL,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT uk_template_field_key UNIQUE (template_id, field_key),
    CONSTRAINT chk_field_type CHECK (field_type IN ('TEXT', 'NUMBER', 'DATE', 'CURRENCY', 'BOOLEAN', 'SIGNATURE_MARKER'))
);

CREATE INDEX idx_template_fields_template ON template_fields(template_id, display_order);

-- ==============================================================================
-- 7. GENERATION JOBS TABLE
-- Bulk document generation tracking
-- ==============================================================================
CREATE TABLE generation_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    template_id UUID NOT NULL REFERENCES document_templates(id) ON DELETE RESTRICT,
    job_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'QUEUED',
    total_records INT NOT NULL DEFAULT 0,
    processed_records INT NOT NULL DEFAULT 0,
    failed_records INT NOT NULL DEFAULT 0,
    error_summary TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE NULL,
    created_by UUID NOT NULL,
    CONSTRAINT chk_job_status CHECK (status IN ('QUEUED', 'PROCESSING', 'COMPLETED', 'FAILED', 'CANCELLED'))
);

CREATE INDEX idx_generation_jobs_org ON generation_jobs(organization_id, status);

-- ==============================================================================
-- 8. ROW-LEVEL SECURITY (RLS) POLICIES FOR MULTI-TENANCY
-- Enforces tenant isolation at PostgreSQL kernel layer
-- ==============================================================================
ALTER TABLE folders ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE template_fields ENABLE ROW LEVEL SECURITY;
ALTER TABLE generation_jobs ENABLE ROW LEVEL SECURITY;

-- Tenant Isolation RLS Policy definitions (assumes application sets app.current_tenant)
CREATE POLICY folder_tenant_isolation_policy ON folders
    USING (organization_id = NULLIF(current_setting('app.current_tenant', true), '')::uuid);

CREATE POLICY document_tenant_isolation_policy ON documents
    USING (organization_id = NULLIF(current_setting('app.current_tenant', true), '')::uuid);

CREATE POLICY doc_version_tenant_isolation_policy ON document_versions
    USING (organization_id = NULLIF(current_setting('app.current_tenant', true), '')::uuid);

CREATE POLICY doc_tag_tenant_isolation_policy ON document_tags
    USING (organization_id = NULLIF(current_setting('app.current_tenant', true), '')::uuid);

CREATE POLICY template_tenant_isolation_policy ON document_templates
    USING (organization_id = NULLIF(current_setting('app.current_tenant', true), '')::uuid);

CREATE POLICY template_field_tenant_isolation_policy ON template_fields
    USING (organization_id = NULLIF(current_setting('app.current_tenant', true), '')::uuid);

CREATE POLICY generation_job_tenant_isolation_policy ON generation_jobs
    USING (organization_id = NULLIF(current_setting('app.current_tenant', true), '')::uuid);
