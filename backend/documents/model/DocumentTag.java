package com.sofzenix.esign.documents.model;

import java.time.OffsetDateTime;
import java.util.UUID;

/**
 * Document Tag entity for metadata filtering and categorization.
 */
public class DocumentTag {
    private UUID id;
    private UUID documentId;
    private UUID organizationId;
    private String tagName;
    private String colorCode;
    private OffsetDateTime createdAt;
    private UUID createdBy;

    public DocumentTag() {}

    public DocumentTag(UUID id, UUID documentId, UUID organizationId, String tagName, String colorCode, UUID createdBy) {
        this.id = id;
        this.documentId = documentId;
        this.organizationId = organizationId;
        this.tagName = tagName;
        this.colorCode = colorCode;
        this.createdBy = createdBy;
        this.createdAt = OffsetDateTime.now();
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getDocumentId() { return documentId; }
    public void setDocumentId(UUID documentId) { this.documentId = documentId; }

    public UUID getOrganizationId() { return organizationId; }
    public void setOrganizationId(UUID organizationId) { this.organizationId = organizationId; }

    public String getTagName() { return tagName; }
    public void setTagName(String tagName) { this.tagName = tagName; }

    public String getColorCode() { return colorCode; }
    public void setColorCode(String colorCode) { this.colorCode = colorCode; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(OffsetDateTime createdAt) { this.createdAt = createdAt; }

    public UUID getCreatedBy() { return createdBy; }
    public void setCreatedBy(UUID createdBy) { this.createdBy = createdBy; }
}
