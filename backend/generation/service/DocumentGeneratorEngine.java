package com.sofzenix.esign.generation.service;

import com.sofzenix.esign.generation.model.WatermarkType;

import java.io.OutputStream;
import java.util.Map;

/**
 * Low-level Rendering Engine Interface for HTML-to-PDF compilation, variable merging, QR code stamping, and watermarking.
 */
public interface DocumentGeneratorEngine {

    /**
     * Merge dynamic field data into HTML markup template.
     */
    String mergeTemplateData(String htmlContent, Map<String, Object> mergeData);

    /**
     * Compile merged HTML markup into a PDF byte output stream.
     */
    void compileHtmlToPdf(String mergedHtml, String headerHtml, String footerHtml, OutputStream outputStream);

    /**
     * Stamp a dynamic watermark onto a PDF document.
     */
    byte[] applyWatermark(byte[] pdfBytes, WatermarkType watermarkType, String customWatermarkText);

    /**
     * Stamp a verification QR code image onto a PDF document page.
     */
    byte[] applyQrCodeVerification(byte[] pdfBytes, String verificationUrl);
}
