# 📄 Extracteur de Données de Factures

> Extraction automatique depuis des factures scannées — OCR + Regex + Streamlit.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Tesseract](https://img.shields.io/badge/OCR-Tesseract-orange) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

## Pipeline

```
Image scannée → Prétraitement (Pillow) → OCR par zones (pytesseract) → Extraction regex → CSV / JSON / SQLite
```

## Installation & lancement

```bash
pip install pillow pytesseract pandas streamlit
streamlit run interface.py
```

## Données extraites

| Champ | Champ |
|---|---|
| Numéro de facture | IBAN |
| Date | Tax ID (vendeur & client) |
| Montant net / TVA / brut | Nom & adresse (vendeur & client) |

✅ 0 valeurs manquantes sur l'ensemble du jeu de données testé.

## Extensions possibles

| Direction | Description |
|---|---|
| 🤖 LLM Vision | Remplacer l'OCR par GPT-4o / Claude pour lire les images directement |
| 🧠 Extraction NLP | Remplacer les regex par un LLM pour des documents non structurés |
| ☁️ API REST | Exposer via FastAPI pour intégration ERP / comptabilité |
| 🗄️ ETL + BI | Connecter à PostgreSQL + Power BI pour un tableau de bord temps réel |
| 🌍 Multi-format | Étendre aux PDFs natifs, factures multilingues, autres documents |

## 📄 Rapport complet

[![Rapport PDF](https://img.shields.io/badge/Rapport-PDF-red?logo=adobeacrobatreader)](https://github.com/user-attachments/files/27897380/Projet_Extraction.pdf)
