package com.sofzenix.esign.generation.dto;

import com.sofzenix.esign.generation.model.TemplateType;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

/**
 * Standard DTO representation of a Document Template.
 */
public class TemplateResponse {
    private UUID id;
    private UUID organizationId;
    private String name;
    private String description;
    private TemplateType templateType;
    private String contentBody;
    private Boolean isActive;
    private Integer versionNumber;
    private List<CreateTemplateRequest.TemplateFieldDTO> fields;
    private OffsetDateTime createdAt;
    private OffsetDateTime updatedAt;
    private UUID createdBy;

    public TemplateResponse() {}

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getOrganizationId() { return organizationId; }
    public void setOrganizationId(UUID organizationId) { this.organizationId = organizationId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public TemplateType getTemplateType() { return templateType; }
    public void setTemplateType(TemplateType templateType) { this.templateType = templateType; }

    public String getContentBody() { return contentBody; }
    public void setContentBody(String contentBody) { this.contentBody = contentBody; }

    public Boolean getIsActive() { return isActive; }
    public void setIsActive(Boolean isActive) { this.isActive = isActive; }

    public Integer getVersionNumber() { return versionNumber; }
    public void setVersionNumber(Integer versionNumber) { this.versionNumber = versionNumber; }

    public List<CreateTemplateRequest.TemplateFieldDTO> getFields() { return fields; }
    public void setFields(List<CreateTemplateRequest.TemplateFieldDTO> fields) { this.fields = fields; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(OffsetDateTime createdAt) { this.createdAt = createdAt; }

    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(OffsetDateTime updatedAt) { this.updatedAt = updatedAt; }

    public UUID getCreatedBy() { return createdBy; }
    public void setCreatedBy(UUID createdBy) { this.createdBy = createdBy; }
}
