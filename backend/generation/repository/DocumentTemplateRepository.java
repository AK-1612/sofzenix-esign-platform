package com.sofzenix.esign.generation.repository;

import com.sofzenix.esign.generation.model.DocumentTemplate;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Persistence Repository Interface for Document Templates.
 */
public interface DocumentTemplateRepository {
    DocumentTemplate save(DocumentTemplate template);
    Optional<DocumentTemplate> findByIdAndOrganizationId(UUID id, UUID organizationId);
    List<DocumentTemplate> findByOrganizationIdAndIsActiveTrue(UUID organizationId);
    void softDelete(UUID id, UUID organizationId, UUID deletedBy);
}
