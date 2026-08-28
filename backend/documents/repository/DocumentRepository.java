package com.sofzenix.esign.documents.repository;

import com.sofzenix.esign.documents.model.Document;
import com.sofzenix.esign.documents.model.DocumentStatus;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Persistence Repository Interface for Document aggregate root.
 */
public interface DocumentRepository {
    Document save(Document document);
    Optional<Document> findByIdAndOrganizationId(UUID id, UUID organizationId);
    List<Document> findByOrganizationIdAndFolderId(UUID organizationId, UUID folderId);
    List<Document> findByOrganizationIdAndStatus(UUID organizationId, DocumentStatus status);
    void softDelete(UUID id, UUID organizationId, UUID deletedBy);
}
