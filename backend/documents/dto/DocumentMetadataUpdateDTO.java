package com.sofzenix.esign.documents.dto;

import com.sofzenix.esign.documents.model.DocumentStatus;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

/**
 * Payload for updating document metadata.
 */
public class DocumentMetadataUpdateDTO {
    private String title;
    private String description;
    private UUID folderId;
    private DocumentStatus status;
    private List<String> tags;
    private OffsetDateTime retentionExpiresAt;

    public DocumentMetadataUpdateDTO() {}

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public UUID getFolderId() { return folderId; }
    public void setFolderId(UUID folderId) { this.folderId = folderId; }

    public DocumentStatus getStatus() { return status; }
    public void setStatus(DocumentStatus status) { this.status = status; }

    public List<String> getTags() { return tags; }
    public void setTags(List<String> tags) { this.tags = tags; }

    public OffsetDateTime getRetentionExpiresAt() { return retentionExpiresAt; }
    public void setRetentionExpiresAt(OffsetDateTime retentionExpiresAt) { this.retentionExpiresAt = retentionExpiresAt; }
}
