package com.sofzenix.esign.generation.model;

import java.time.OffsetDateTime;
import java.util.UUID;

/**
 * Dynamic Merge Field marker definition.
 */
public class TemplateField {
    private UUID id;
    private UUID templateId;
    private UUID organizationId;
    private String fieldKey;
    private String fieldLabel;
    private String fieldType; // TEXT, NUMBER, DATE, CURRENCY, BOOLEAN, SIGNATURE_MARKER
    private Boolean isRequired;
    private String defaultValue;
    private String validationRegex;
    private Integer displayOrder;
    private OffsetDateTime createdAt;

    public TemplateField() {
        this.fieldType = "TEXT";
        this.isRequired = true;
        this.displayOrder = 0;
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getTemplateId() { return templateId; }
    public void setTemplateId(UUID templateId) { this.templateId = templateId; }

    public UUID getOrganizationId() { return organizationId; }
    public void setOrganizationId(UUID organizationId) { this.organizationId = organizationId; }

    public String getFieldKey() { return fieldKey; }
    public void setFieldKey(String fieldKey) { this.fieldKey = fieldKey; }

    public String getFieldLabel() { return fieldLabel; }
    public void setFieldLabel(String fieldLabel) { this.fieldLabel = fieldLabel; }

    public String getFieldType() { return fieldType; }
    public void setFieldType(String fieldType) { this.fieldType = fieldType; }

    public Boolean getIsRequired() { return isRequired; }
    public void setIsRequired(Boolean isRequired) { this.isRequired = isRequired; }

    public String getDefaultValue() { return defaultValue; }
    public void setDefaultValue(String defaultValue) { this.defaultValue = defaultValue; }

    public String getValidationRegex() { return validationRegex; }
    public void setValidationRegex(String validationRegex) { this.validationRegex = validationRegex; }

    public Integer getDisplayOrder() { return displayOrder; }
    public void setDisplayOrder(Integer displayOrder) { this.displayOrder = displayOrder; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(OffsetDateTime createdAt) { this.createdAt = createdAt; }
}
