# 📄 Invoice Data Extractor
> Automated extraction from scanned invoices — OCR + Regex + Streamlit.

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![Tesseract](https://img.shields.io/badge/OCR-Tesseract-orange)](https://github.com/tesseract-ocr/tesseract)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🎬 Demo Video

> 📽️ **Watch the full walkthrough** — uploading scanned invoices, OCR extraction, regex parsing, and export to CSV / JSON / SQLite via the Streamlit interface.

[![▶ Watch Demo on Google Drive](https://img.shields.io/badge/▶%20Watch%20Full%20Demo-Google%20Drive-blue?style=for-the-badge&logo=googledrive)](https://drive.google.com/file/d/1TvIJYx5l-oWytF_C5mEQoPIYXN34BVjW/view)

---

## 🧠 Overview

This project automates the extraction of structured data from scanned invoice images using a combination of image preprocessing, zonal OCR, and regular expressions. Results are stored in CSV, JSON, and a relational SQLite database, and exposed through a clean Streamlit UI.

**✅ 0 missing values across the entire tested dataset.**

---

## ⚙️ Pipeline

```
Scanned Image → Preprocessing (Pillow) → Zonal OCR (pytesseract) → Regex Extraction → CSV / JSON / SQLite
```

<img width="571" height="318" alt="OCR Steps" src="https://github.com/user-attachments/assets/8b0de149-edb0-466c-9612-e88dec31a6ab" />

---

## 🚀 Installation & Launch

**Prerequisites:** Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and make sure it's available in your `PATH`.

```bash
pip install pillow pytesseract pandas streamlit
streamlit run interface.py
```

---

## 📊 Extracted Fields

| Field | Field |
|---|---|
| Invoice Number | IBAN |
| Date | Tax ID (vendor & client) |
| Net / VAT / Gross Amount | Name & Address (vendor & client) |

<img width="748" height="395" alt="Regex Extraction" src="https://github.com/user-attachments/assets/e2754e22-248e-4cc8-9ed9-d50fd845c790" />

---

## 🗄️ Database Schema

Relational SQLite model with 3 normalized tables: `Invoices`, `Clients`, `Sellers`.

<img width="726" height="351" alt="Database Schema" src="https://github.com/user-attachments/assets/24082f10-201f-41c2-a9db-3e58ae5397d2" />

---

## 🖥️ User Interface

Upload multiple files → OCR extraction → results table → export to CSV / SQL.

<img width="726" height="351" alt="Streamlit Interface" src="https://github.com/user-attachments/assets/d42a6aa7-ad7c-49f9-9de9-72414c3c5683" />

---

## 🔮 Possible Extensions

| Direction | Description |
|---|---|
| 🤖 LLM Vision | Replace OCR with GPT-4o / Claude for direct image reading |
| 🧠 NLP Extraction | Replace regex with an LLM for unstructured documents |
| ☁️ REST API | Expose via FastAPI for ERP / accounting integration |
| 🗄️ ETL + BI | Connect to PostgreSQL + Power BI for a real-time dashboard |
| 🌍 Multi-format | Extend to native PDFs, multilingual invoices, other document types |

---

## ✅ Conclusion

This project demonstrates how to automate information extraction from scanned documents by combining OCR and regular expressions. Data is structured into CSV, JSON, and SQLite, and visualized through a simple Streamlit interface — a solid foundation in text processing, Python, and interface design.

---

## 📄 Full Report

<img width="800" height="847" alt="Table of Contents" src="https://github.com/user-attachments/assets/ed6810fe-0d2a-4137-9481-a7a3359d81d3" />

<h3 align="center">
  <a href="https://github.com/user-attachments/files/27897380/Projet_Extraction.pdf">
    📄 Click Here to See the Full Document (PDF Report)
  </a>
</h3>
