package com.sofzenix.esign.generation.dto;

import com.sofzenix.esign.generation.model.WatermarkType;

import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Payload for triggering bulk batch document generation.
 */
public class BulkGenerateRequest {
    private UUID templateId;
    private String jobName;
    private UUID targetFolderId;
    private WatermarkType watermark;
    private List<Map<String, Object>> records;

    public BulkGenerateRequest() {}

    public UUID getTemplateId() { return templateId; }
    public void setTemplateId(UUID templateId) { this.templateId = templateId; }

    public String getJobName() { return jobName; }
    public void setJobName(String jobName) { this.jobName = jobName; }

    public UUID getTargetFolderId() { return targetFolderId; }
    public void setTargetFolderId(UUID targetFolderId) { this.targetFolderId = targetFolderId; }

    public WatermarkType getWatermark() { return watermark; }
    public void setWatermark(WatermarkType watermark) { this.watermark = watermark; }

    public List<Map<String, Object>> getRecords() { return records; }
    public void setRecords(List<Map<String, Object>> records) { this.records = records; }
}
