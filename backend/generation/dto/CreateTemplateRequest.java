package com.sofzenix.esign.generation.dto;

import com.sofzenix.esign.generation.model.TemplateType;

import java.util.List;

/**
 * Payload for creating a new document template.
 */
public class CreateTemplateRequest {
    private String name;
    private String description;
    private TemplateType templateType;
    private String contentBody;
    private String headerHtml;
    private String footerHtml;
    private List<TemplateFieldDTO> fields;

    public CreateTemplateRequest() {}

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public TemplateType getTemplateType() { return templateType; }
    public void setTemplateType(TemplateType templateType) { this.templateType = templateType; }

    public String getContentBody() { return contentBody; }
    public void setContentBody(String contentBody) { this.contentBody = contentBody; }

    public String getHeaderHtml() { return headerHtml; }
    public void setHeaderHtml(String headerHtml) { this.headerHtml = headerHtml; }

    public String getFooterHtml() { return footerHtml; }
    public void setFooterHtml(String footerHtml) { this.footerHtml = footerHtml; }

    public List<TemplateFieldDTO> getFields() { return fields; }
    public void setFields(List<TemplateFieldDTO> fields) { this.fields = fields; }

    public static class TemplateFieldDTO {
        private String fieldKey;
        private String fieldLabel;
        private String fieldType;
        private Boolean isRequired;
        private String defaultValue;
        private String validationRegex;
        private Integer displayOrder;

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
    }
}
