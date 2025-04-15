# Dynamic Data Masking Engine 
## Overview

**Dynamic Data Masking Engine (DDM Engine) v0.1.0** is a robust, modular, and extensible system designed to detect, anonymize, and redact sensitive information across unstructured documents and data streams. It is tailored for enterprise-grade compliance, data protection, and information security workflows.

At its core, the DDM Engine leverages natural language processing (NLP), OCR, and configurable customer strategies to handle sensitive content in real-time or batch processing environments. The system is capable of integrating with Kafka for event-based document processing, making it suitable for high-throughput data masking pipelines.

The masking logic adapts based on the customer requirements, building a pipeline strategy dynamically that reflects the customer profile, language, document type, and confidentiality level. This flexibility allows teams to process data in multilingual environments while staying compliant with internal and external data protection standards.

---

## Installation

_TBD_

---

## Usage

### CLI Command

```bash
ddm_engine --event <event_payload.json> --customer <customer_name>
```

### Arguments Table

| Argument         | Type | Default    | Description                                                                 |
|------------------|------|------------|-----------------------------------------------------------------------------|
| `--event`        | str  | _Required_ | Path to a JSON file or JSON string that includes metadata like Kafka topic and document path |
| `--customer`     | str  | _Required_ | Customer profile to use. Determines how the pipeline is built dynamically   |

---

## Customers

The DDM Engine supports multiple customer profiles. Each customer configuration determines the behavior of the pipeline, including analyzer logic, masking strategies, redaction policies, and supported entity types.

| Customer | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| `fraude` | Fraud detection and compliance use-case. Includes strict PII recognition, French/English NLP support, and blackout-style redaction for PDFs. Tailored anonymizer operators for financial and personal data masking. |

---

## Pipeline Flow for `fraude`

1. **Input Handling**:
   - The engine listens to a Kafka topic and consumes event payloads.
   - Each event includes metadata such as file path, language, and document type.

2. **File Processing**:
   - Files (e.g., PDFs) are read and optionally passed through OCR (Tesseract) to extract textual content.

3. **Analyzer**:
   - Language-specific NLP models (e.g., `fr_core_news_sm` for French) are used.
   - Custom recognizers and Presidio are configured to detect C4 data (health issues, racial details, religious beliefs etc.), and other sensitive tokens.

4. **Anonymizer**:
   - The analyzer output is passed through an anonymizer engine.
   - For `fraude`, anonymization includes token masking and black-box visual redaction.

5. **Redactor**:
   - Visual redaction (e.g., blackout boxes) is applied to sensitive tokens within the original PDF.

6. **Output**:
   - The redacted file is saved to a target directory.
   - Kafka can be used to notify downstream systems about the processing status.

---

## Example

```bash
ddm_engine --event ./events/sample_event_fraude.json --customer fraude
```

This command will load the configuration for the "fraude" customer, consume the event metadata, and apply the corresponding masking logic on the specified file.

---