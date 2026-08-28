package com.sofzenix.esign.generation.dto;

import com.sofzenix.esign.generation.model.WatermarkType;

import java.util.Map;
import java.util.UUID;

/**
 * Payload for generating a PDF document from a template and merge data map.
 */
public class GenerateDocumentRequest {
    private UUID templateId;
    private String documentTitle;
    private UUID folderId;
    private Map<String, Object> mergeData;
    private WatermarkType watermark;
    private Boolean includeQrCodeVerification;

    public GenerateDocumentRequest() {
        this.watermark = WatermarkType.NONE;
        this.includeQrCodeVerification = true;
    }

    public UUID getTemplateId() { return templateId; }
    public void setTemplateId(UUID templateId) { this.templateId = templateId; }

    public String getDocumentTitle() { return documentTitle; }
    public void setDocumentTitle(String documentTitle) { this.documentTitle = documentTitle; }

    public UUID getFolderId() { return folderId; }
    public void setFolderId(UUID folderId) { this.folderId = folderId; }

    public Map<String, Object> getMergeData() { return mergeData; }
    public void setMergeData(Map<String, Object> mergeData) { this.mergeData = mergeData; }

    public WatermarkType getWatermark() { return watermark; }
    public void setWatermark(WatermarkType watermark) { this.watermark = watermark; }

    public Boolean getIncludeQrCodeVerification() { return includeQrCodeVerification; }
    public void setIncludeQrCodeVerification(Boolean includeQrCodeVerification) { this.includeQrCodeVerification = includeQrCodeVerification; }
}
