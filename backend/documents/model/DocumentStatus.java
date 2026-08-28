package com.sofzenix.esign.documents.model;

/**
 * Domain Lifecycle States for Business Documents.
 */
public enum DocumentStatus {
    DRAFT,
    PENDING_REVIEW,
    APPROVED,
    SIGNING,
    SIGNED,
    VAULTED,
    EXPIRED,
    ARCHIVED
}
