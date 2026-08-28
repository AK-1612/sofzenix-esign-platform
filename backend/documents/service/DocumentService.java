package com.sofzenix.esign.documents.service;

import com.sofzenix.esign.documents.dto.*;
import com.sofzenix.esign.documents.model.Document;
import com.sofzenix.esign.documents.model.DocumentVersion;

import java.io.InputStream;
import java.util.List;
import java.util.UUID;

/**
 * Service Interface contract defining domain methods for Document Management.
 */
public interface DocumentService {

    /**
     * Upload and register a new document.
     */
    DocumentResponse uploadDocument(UUID organizationId, UUID userId, DocumentUploadRequest request, InputStream fileStream);

    /**
     * Retrieve document details by ID.
     */
    DocumentResponse getDocumentById(UUID organizationId, UUID documentId);

    /**
     * Update document metadata.
     */
    DocumentResponse updateDocumentMetadata(UUID organizationId, UUID userId, UUID documentId, DocumentMetadataUpdateDTO updateDTO);

    /**
     * Upload a new version to an existing document.
     */
    DocumentResponse createNewVersion(UUID organizationId, UUID userId, UUID documentId, String changeSummary, InputStream fileStream, String fileName, long fileSizeBytes, String checksum);

    /**
     * Retrieve all versions of a document.
     */
    List<DocumentVersion> getDocumentVersions(UUID organizationId, UUID documentId);

    /**
     * Search documents with criteria.
     */
    List<DocumentResponse> searchDocuments(UUID organizationId, DocumentSearchFilterDTO filter);

    /**
     * Soft delete a document.
     */
    void deleteDocument(UUID organizationId, UUID userId, UUID documentId);
}
