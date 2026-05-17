# 📄 Extracteur de Données de Factures

> Extraction automatique depuis des factures scannées — OCR + Regex + Streamlit.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Tesseract](https://img.shields.io/badge/OCR-Tesseract-orange) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

---

## Pipeline

```
Image scannée → Prétraitement (Pillow) → OCR par zones (pytesseract) → Extraction regex → CSV / JSON / SQLite
```

<img width="571" height="318" alt="Étapes OCR" src="https://github.com/user-attachments/assets/8b0de149-edb0-466c-9612-e88dec31a6ab" />

---

## Installation & lancement

```bash
pip install pillow pytesseract pandas streamlit
streamlit run interface.py
```

---

## Données extraites

| Champ | Champ |
|---|---|
| Numéro de facture | IBAN |
| Date | Tax ID (vendeur & client) |
| Montant net / TVA / brut | Nom & adresse (vendeur & client) |

<img width="748" height="395" alt="Extraction regex" src="https://github.com/user-attachments/assets/e2754e22-248e-4cc8-9ed9-d50fd845c790" />

✅ 0 valeurs manquantes sur l'ensemble du jeu de données testé.

---

## Base de données

Modèle relationnel SQLite avec 3 tables : `Invoices`, `Clients`, `Sellers`.

<img width="726" height="351" alt="Schéma base de données" src="https://github.com/user-attachments/assets/24082f10-201f-41c2-a9db-3e58ae5397d2" />

---

## Interface utilisateur

Upload multiple fichiers → extraction OCR → tableau de résultats → export CSV / SQL.

<img width="726" height="351" alt="Interface Streamlit" src="https://github.com/user-attachments/assets/d42a6aa7-ad7c-49f9-9de9-72414c3c5683" />

---

## Extensions possibles

| Direction | Description |
|---|---|
| 🤖 LLM Vision | Remplacer l'OCR par GPT-4o / Claude pour lire les images directement |
| 🧠 Extraction NLP | Remplacer les regex par un LLM pour des documents non structurés |
| ☁️ API REST | Exposer via FastAPI pour intégration ERP / comptabilité |
| 🗄️ ETL + BI | Connecter à PostgreSQL + Power BI pour un tableau de bord temps réel |
| 🌍 Multi-format | Étendre aux PDFs natifs, factures multilingues, autres documents |

---

## Conclusion

Ce projet démontre comment automatiser l'extraction d'informations à partir de documents scannés en combinant OCR et expressions régulières. Les données sont structurées en CSV, JSON et SQLite, et visualisées via une interface Streamlit simple. Un bon socle en traitement de texte, Python et conception d'interfaces.

---

## 📄 Rapport complet

<img width="800" height="847" alt="Table des matières" src="https://github.com/user-attachments/assets/ed6810fe-0d2a-4137-9481-a7a3359d81d3" />

[![Rapport PDF](https://img.shields.io/badge/Rapport-PDF-red?logo=adobeacrobatreader)](https://github.com/user-attachments/files/27897380/Projet_Extraction.pdf)
