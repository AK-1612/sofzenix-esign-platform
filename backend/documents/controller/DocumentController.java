package com.sofzenix.esign.documents.controller;

import com.sofzenix.esign.documents.dto.*;
import com.sofzenix.esign.documents.model.DocumentVersion;
import com.sofzenix.esign.documents.service.DocumentService;

import java.util.List;
import java.util.UUID;

/**
 * REST Controller Contract for Document Management API endpoints.
 * Note: Method signatures establish API contracts. Production implementation will be injected during feature phase.
 */
public class DocumentController {

    private final DocumentService documentService;

    public DocumentController(DocumentService documentService) {
        this.documentService = documentService;
    }

    public DocumentResponse uploadDocument(UUID orgId, UUID userId, DocumentUploadRequest request) {
        // Defined API Controller Boundary contract method
        throw new UnsupportedOperationException("Phase 1 Interface Specification Boundary");
    }

    public DocumentResponse getDocument(UUID orgId, UUID documentId) {
        return documentService.getDocumentById(orgId, documentId);
    }

    public DocumentResponse updateMetadata(UUID orgId, UUID userId, UUID documentId, DocumentMetadataUpdateDTO updateDTO) {
        return documentService.updateDocumentMetadata(orgId, userId, documentId, updateDTO);
    }

    public List<DocumentVersion> getVersions(UUID orgId, UUID documentId) {
        return documentService.getDocumentVersions(orgId, documentId);
    }

    public List<DocumentResponse> searchDocuments(UUID orgId, DocumentSearchFilterDTO filter) {
        return documentService.searchDocuments(orgId, filter);
    }

    public void deleteDocument(UUID orgId, UUID userId, UUID documentId) {
        documentService.deleteDocument(orgId, userId, documentId);
    }
}
