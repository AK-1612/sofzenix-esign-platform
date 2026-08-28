package com.sofzenix.esign.generation.model;

import java.time.OffsetDateTime;
import java.util.UUID;

/**
 * Bulk Generation Job tracking record.
 */
public class GenerationJob {
    private UUID id;
    private UUID organizationId;
    private UUID templateId;
    private String jobName;
    private String status; // QUEUED, PROCESSING, COMPLETED, FAILED, CANCELLED
    private Integer totalRecords;
    private Integer processedRecords;
    private Integer failedRecords;
    private String errorSummary;
    private OffsetDateTime createdAt;
    private OffsetDateTime completedAt;
    private UUID createdBy;

    public GenerationJob() {
        this.status = "QUEUED";
        this.totalRecords = 0;
        this.processedRecords = 0;
        this.failedRecords = 0;
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getOrganizationId() { return organizationId; }
    public void setOrganizationId(UUID organizationId) { this.organizationId = organizationId; }

    public UUID getTemplateId() { return templateId; }
    public void setTemplateId(UUID templateId) { this.templateId = templateId; }

    public String getJobName() { return jobName; }
    public void setJobName(String jobName) { this.jobName = jobName; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Integer getTotalRecords() { return totalRecords; }
    public void setTotalRecords(Integer totalRecords) { this.totalRecords = totalRecords; }

    public Integer getProcessedRecords() { return processedRecords; }
    public void setProcessedRecords(Integer processedRecords) { this.processedRecords = processedRecords; }

    public Integer getFailedRecords() { return failedRecords; }
    public void setFailedRecords(Integer failedRecords) { this.failedRecords = failedRecords; }

    public String getErrorSummary() { return errorSummary; }
    public void setErrorSummary(String errorSummary) { this.errorSummary = errorSummary; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(OffsetDateTime createdAt) { this.createdAt = createdAt; }

    public OffsetDateTime getCompletedAt() { return completedAt; }
    public void setCompletedAt(OffsetDateTime completedAt) { this.completedAt = completedAt; }

    public UUID getCreatedBy() { return createdBy; }
    public void setCreatedBy(UUID createdBy) { this.createdBy = createdBy; }
}
