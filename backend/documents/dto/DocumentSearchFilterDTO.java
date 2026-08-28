package com.sofzenix.esign.documents.dto;

import com.sofzenix.esign.documents.model.DocumentStatus;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

/**
 * Criteria payload for searching and filtering documents.
 */
public class DocumentSearchFilterDTO {
    private String query;
    private DocumentStatus status;
    private UUID folderId;
    private List<String> tags;
    private OffsetDateTime createdAfter;
    private OffsetDateTime createdBefore;
    private Integer page = 0;
    private Integer size = 20;

    public DocumentSearchFilterDTO() {}

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }

    public DocumentStatus getStatus() { return status; }
    public void setStatus(DocumentStatus status) { this.status = status; }

    public UUID getFolderId() { return folderId; }
    public void setFolderId(UUID folderId) { this.folderId = folderId; }

    public List<String> getTags() { return tags; }
    public void setTags(List<String> tags) { this.tags = tags; }

    public OffsetDateTime getCreatedAfter() { return createdAfter; }
    public void setCreatedAfter(OffsetDateTime createdAfter) { this.createdAfter = createdAfter; }

    public OffsetDateTime getCreatedBefore() { return createdBefore; }
    public void setCreatedBefore(OffsetDateTime createdBefore) { this.createdBefore = createdBefore; }

    public Integer getPage() { return page; }
    public void setPage(Integer page) { this.page = page; }

    public Integer getSize() { return size; }
    public void setSize(Integer size) { this.size = size; }
}
