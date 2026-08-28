package com.sofzenix.esign.generation.service;

import com.sofzenix.esign.documents.dto.DocumentResponse;
import com.sofzenix.esign.generation.dto.*;
import com.sofzenix.esign.generation.model.DocumentTemplate;
import com.sofzenix.esign.generation.model.GenerationJob;

import java.util.List;
import java.util.UUID;

/**
 * Service Interface contract defining domain methods for Document Template administration.
 */
public interface TemplateService {

    /**
     * Create a new document template.
     */
    TemplateResponse createTemplate(UUID organizationId, UUID userId, CreateTemplateRequest request);

    /**
     * Retrieve template details by ID.
     */
    TemplateResponse getTemplateById(UUID organizationId, UUID templateId);

    /**
     * List templates by organization.
     */
    List<TemplateResponse> getTemplates(UUID organizationId);

    /**
     * Trigger dynamic PDF generation for a single document.
     */
    DocumentResponse generateDocument(UUID organizationId, UUID userId, GenerateDocumentRequest request);

    /**
     * Trigger asynchronous bulk batch document generation.
     */
    GenerationJob startBulkGeneration(UUID organizationId, UUID userId, BulkGenerateRequest request);

    /**
     * Delete a template.
     */
    void deleteTemplate(UUID organizationId, UUID userId, UUID templateId);
}
