package com.sofzenix.esign.documents.repository;

import com.sofzenix.esign.documents.model.DocumentVersion;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Persistence Repository Interface for Document Versions.
 */
public interface DocumentVersionRepository {
    DocumentVersion save(DocumentVersion version);
    Optional<DocumentVersion> findByIdAndOrganizationId(UUID id, UUID organizationId);
    List<DocumentVersion> findByDocumentIdAndOrganizationIdOrderByVersionNumberDesc(UUID documentId, UUID organizationId);
    Optional<DocumentVersion> findByDocumentIdAndVersionNumber(UUID documentId, Integer versionNumber);
}
