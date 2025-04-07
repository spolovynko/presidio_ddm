# Dynamic Data Masking Engine v0.1.0

## Overview

**Dynamic Data Masking Engine v0.1.0** is a modular and extensible pipeline designed for detecting and anonymizing sensitive information in files and data streams. It combines NLP-powered entity recognition with customizable anonymization/redaction techniques and supports various file types including PDFs and images.

---

## Installation

_TBD_

---

## Usage

### Command Line Arguments

You can run the engine via CLI after installing the package using the entry point `ddm_engine`.

```bash
ddm_engine <input_file_path> [options]
```

### Arguments Table

| Argument               | Type   | Default     | Description |
|------------------------|--------|-------------|-------------|
| `input_file_path`      | str    | _Required_  | Path to the file that needs masking |
| `--lang`               | str    | `en`        | Language of the file (`en`, `fr`, etc.) |
| `--resolution`         | int    | `350`       | Resolution for OCR during file reading |
| `--ocr-config`         | str    | `--oem 3 --psm 6` | Configuration string for OCR |
| `--conf_level`         | str    | `c4`        | Confidentiality level (`c3`, `c4`) |
| `--analyzer_engine`    | str    | `from_config_file` | Analyzer setup method (`from_config_file`, `from_code`) |
| `--customer`           | str    | `fraude`    | Customer-specific logic (`fraude`, ...) |
| `--anonimyzer_operator`| str    | `yes`       | Anonymizer operator toggle |
| `--masking_strategy`   | str    | `blackout`  | Redaction method (`blackout`, etc.) |
| `--output_file_path`   | str    | _Required_  | Path to output the masked file |

### Example

```bash
ddm_engine ./samples/invoice_sample.pdf \
  --lang en \
  --resolution 300 \
  --ocr-config "--oem 1 --psm 3" \
  --conf_level c4 \
  --analyzer_engine from_config_file \
  --customer fraude \
  --anonimyzer_operator yes \
  --masking_strategy blackout \
  --output_file_path ./output/invoice_masked.pdf
```

This example takes an English invoice PDF file, uses OCR to read its content, detects sensitive data according to the 'fraude' customer profile and 'c4' confidentiality level, and outputs a masked version of the document.

---

## Structure

```
dynamic_data_masking/
├── ddm_config/                # Configuration files (env + analyzer settings)
├── ddm_connectors/           # External system connectors (DB, Kafka, etc.)
├── ddm_logger/               # Custom logging module
├── dynamic_data_masking_pipeline/
│   ├── analyzer/             # Named Entity Recognition engine
│   ├── anonymizer/           # Masking, blacking out or replacing sensitive tokens
│   ├── file_processor/       # Extract content from PDFs and images
│   ├── file_redactor/        # Apply redaction strategies
│   └── mappers.py            # Token and label mappers
├── customers.py              # Customer-specific extension logic
└── main.py                   # Pipeline entry point
```

### Pipeline Flow

1. **File Processing**: The engine begins by accepting an input file such as a PDF or an image. This file is read and processed using OCR techniques (via Tesseract) if needed. Textual content is extracted to make it suitable for downstream processing.

2. **Analyzer**: The extracted content is passed through an NLP-based analyzer. Depending on the selected language, customer configuration, and confidentiality level, the engine identifies sensitive entities (PII, financial data, etc.) using Presidio and custom recognizers.

3. **Anonymizer**: Identified sensitive elements are then passed to the anonymizer, which applies the specified anonymization logic. This might include replacement, encryption, or token masking depending on the operator selected.

4. **Redactor**: If visual redaction is needed (e.g., for PDF output), the redactor overlays blackout boxes or alternative masking visualizations on the file to obfuscate sensitive tokens in a human-readable format.

5. **Output Generation**: Finally, the masked or redacted file is saved to the specified output path, ready to be used or archived securely.

Each step in the pipeline is modular and configurable, allowing for flexibility in deployment and use across different domains.

---

