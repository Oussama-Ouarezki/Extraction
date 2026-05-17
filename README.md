# Invoice Data Extractor

> Automated extraction of structured data from scanned invoice images using OCR + regex.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Tesseract](https://img.shields.io/badge/OCR-Tesseract-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

## What it does

Takes a folder of scanned invoice images → preprocesses them → runs OCR → extracts key fields (invoice number, date, amounts, tax IDs, IBAN, seller & client info) → exports to **CSV**, **JSON**, and **SQLite**.

## Pipeline

| Step | Tool | Description |
|------|------|-------------|
| Image preprocessing | Pillow | Brightness, grayscale, binarization |
| OCR | pytesseract | Zone-based text extraction |
| Data extraction | `re` module | Regex patterns per field |
| Export | pandas / sqlite3 | CSV, JSON, SQLite output |

## Install

```bash
pip install pillow pytesseract pandas streamlit
```

## Run

```bash
streamlit run interface.py
```

> Requires [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and added to PATH.

## Full report

📄 [View PDF documentation](https://github.com/user-attachments/files/27897380/Projet_Extraction.pdf)
