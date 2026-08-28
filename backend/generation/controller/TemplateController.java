package com.sofzenix.esign.generation.controller;

import com.sofzenix.esign.documents.dto.DocumentResponse;
import com.sofzenix.esign.generation.dto.*;
import com.sofzenix.esign.generation.model.GenerationJob;
import com.sofzenix.esign.generation.service.TemplateService;

import java.util.List;
import java.util.UUID;

/**
 * REST Controller Contract for Document Generation API endpoints.
 * Note: Method signatures establish API contracts. Production implementation will be injected during feature phase.
 */
public class TemplateController {

    private final TemplateService templateService;

    public TemplateController(TemplateService templateService) {
        this.templateService = templateService;
    }

    public TemplateResponse createTemplate(UUID orgId, UUID userId, CreateTemplateRequest request) {
        return templateService.createTemplate(orgId, userId, request);
    }

    public TemplateResponse getTemplate(UUID orgId, UUID templateId) {
        return templateService.getTemplateById(orgId, templateId);
    }

    public List<TemplateResponse> getTemplates(UUID orgId) {
        return templateService.getTemplates(orgId);
    }

    public DocumentResponse generateDocument(UUID orgId, UUID userId, GenerateDocumentRequest request) {
        return templateService.generateDocument(orgId, userId, request);
    }

    public GenerationJob bulkGenerate(UUID orgId, UUID userId, BulkGenerateRequest request) {
        return templateService.startBulkGeneration(orgId, userId, request);
    }

    public void deleteTemplate(UUID orgId, UUID userId, UUID templateId) {
        templateService.deleteTemplate(orgId, userId, templateId);
    }
}
