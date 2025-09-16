# 🚀 NAMASTE-ICD11 Medical Coding Integration API
✨ Bridging 5,000 years of Indian traditional medicine with global healthcare standards

## 📋 Overview
The NAMASTE-ICD11 Integration API connects traditional Indian medicine systems (Ayurveda, Siddha, Unani) with WHO’s ICD-11 standards. It enables smart search, bidirectional translation, and patient encounter recording — empowering healthcare interoperability and insurance coverage.

## 🌟 Features
🔎 Smart fuzzy search across NAMASTE & ICD-11 codes

🔄 Bidirectional code translation

🏥 Patient encounter upload with dual coding

🔐 API key authentication & role management

📄 Auto-generated interactive API docs

🗃️ Audit logging & compliance ready

🌐 FHIR-compliant architecture

## ⚙️ Getting Started
### Prerequisites
Python 3.12+

Internet connection

Installation
bash
### git clone https://github.com/yourusername/namaste-icd-api.git
### cd namaste-icd-api
### pip install -r requirements.txt
### python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
### Open browser and visit:

http://localhost:8000/setup-database

#### To initialize sample data.

🛠️ Usage
Search medical codes
GET /api/search?q={query}&system={namaste|icd11|both}&limit={number}

Translate codes
POST /api/translate

Example request body:

json
{
  "code": "N001",
  "from_system": "NAMASTE",
  "to_system": "ICD-11"
}
Upload patient encounter
POST /api/encounter

#### Requires API key header.

Example body:

json
{
  "patient_id": "P001",
  "namaste_code": "N001",
  "icd11_code": "XM001"
}
## 🔑 API Keys for Testing
User	API Key	Role
Dr. Priya	sk_test_doc001_abc123	Doctor
Admin User	sk_test_admin001_xyz789	Admin
🏗️ Architecture
FastAPI backend

SQLite + SQLAlchemy database

FuzzyWuzzy for search

API key authentication

Deployed with GitHub Codespaces or local Python

## 📞 Contact & Support
For questions or partnership inquiries:
Lead Developer: kshreeshanth@outlook.com
GitHub: shreecodesasap



✨ This project creates a path for traditional Indian medicine to join the global healthcare conversation.

