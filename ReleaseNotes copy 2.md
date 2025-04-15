# 🔄 PowerShell Trigger Script for DDM Engine

This PowerShell script activates a Python virtual environment and executes the `ddm_engine` CLI with customizable arguments for dynamic data masking.

---

## ✅ Requirements

- Python virtual environment must already be created
- The virtual environment path must be correct and point to the `activate.ps1` script
- `ddm_engine` must be installed in the virtual environment
- Windows PowerShell

---

## ⚙️ Script Parameters

| Parameter             | Description                                                  | Required | Default                |
|-----------------------|--------------------------------------------------------------|----------|------------------------|
| `InputFilePath`       | Path to the input file to be masked                         | ✅ Yes   | –                      |
| `OutputFilePath`      | Path where the masked file should be saved                  | ✅ Yes   | –                      |
| `Lang`                | Language of the file content                                | No       | `en`                   |
| `Resolution`          | Resolution (DPI) for image/PDF reading                      | No       | `350`                  |
| `OcrConfig`           | OCR engine config for Tesseract                            | No       | `--oem 3 --psm 6`      |
| `ConfLevel`           | Confidentiality level configuration                        | No       | `c4`                   |
| `AnalyzerEngine`      | Analyzer engine selection                                  | No       | `from_config_file`     |
| `Customer`            | Customer profile to use                                     | No       | `fraude`               |
| `AnonymizerOperator`  | Anonymizer operator configuration                          | No       | `yes`                  |
| `MaskingStrategy`     | Strategy used to redact sensitive information              | No       | `blackout`             |

---

## 🚀 Usage

```powershell
.\trigger.ps1 \
    -InputFilePath "C:\docs\my_input.pdf" \
    -OutputFilePath "C:\docs\masked_output.pdf"
```

You can also customize optional parameters:

```powershell
.\trigger.ps1 \
    -InputFilePath "C:\test\fraude.pdf" \
    -OutputFilePath "C:\test\output.pdf" \
    -Lang "fr" \
    -Customer "fraude" \
    -MaskingStrategy "blur"
```

---

## 📁 Virtual Environment Location

The script assumes the virtual environment is located at:

```
C:\Users\CR29QG\OneDrive - ING\Documents\DDM\TESTING_ENV\testing_ddm\Scripts\activate.ps1
```

Make sure this path matches the location of your `activate.ps1`.

---

## 🚧 Troubleshooting

- If you see `❌ Virtual environment not found`, verify the `$VenvActivatePath` is correct
- Ensure PowerShell execution policy allows running scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass
```

---

Let me know if you want to make this script reusable across different environments!

