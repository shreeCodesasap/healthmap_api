# Sample NAMASTE codes (Traditional Indian Medicine)
NAMASTE_CODES = [
    {"code": "N001", "display": "Jwara (Fever)", "category": "Ayurveda"},
    {"code": "N002", "display": "Kasa (Cough)", "category": "Ayurveda"},
    {"code": "N003", "display": "Atisara (Diarrhea)", "category": "Ayurveda"},
    {"code": "N004", "display": "Shiroroga (Headache)", "category": "Ayurveda"},
    {"code": "N005", "display": "Vatarakta (Arthritis)", "category": "Ayurveda"},
    {"code": "N006", "display": "Prameha (Diabetes)", "category": "Ayurveda"},
    {"code": "N007", "display": "Hridroga (Heart Disease)", "category": "Ayurveda"},
    {"code": "N008", "display": "Netrарoga (Eye Disease)", "category": "Ayurveda"},
    {"code": "N009", "display": "Karnaroga (Ear Disease)", "category": "Ayurveda"},
    {"code": "N010", "display": "Nasaroga (Nasal Disease)", "category": "Ayurveda"},
    
    # Siddha Medicine Codes
    {"code": "S001", "display": "Suram (Fever)", "category": "Siddha"},
    {"code": "S002", "display": "Irumal (Cough)", "category": "Siddha"},
    {"code": "S003", "display": "Vayiru Kedu (Stomach Pain)", "category": "Siddha"},
    
    # Unani Medicine Codes  
    {"code": "U001", "display": "Humma (Fever)", "category": "Unani"},
    {"code": "U002", "display": "Sual (Cough)", "category": "Unani"},
    {"code": "U003", "display": "Ishal (Diarrhea)", "category": "Unani"},
]

# Sample ICD-11 codes
ICD11_CODES = [
    {"code": "XM001", "display": "Traditional Medicine Fever", "system": "ICD-11-TM2", "category": "Traditional Medicine"},
    {"code": "XM002", "display": "Traditional Medicine Cough", "system": "ICD-11-TM2", "category": "Traditional Medicine"},
    {"code": "XM003", "display": "Traditional Medicine Diarrhea", "system": "ICD-11-TM2", "category": "Traditional Medicine"},
    {"code": "XM004", "display": "Traditional Medicine Headache", "system": "ICD-11-TM2", "category": "Traditional Medicine"},
    {"code": "XM005", "display": "Traditional Medicine Arthritis", "system": "ICD-11-TM2", "category": "Traditional Medicine"},
    
    # Standard ICD-11 Codes
    {"code": "CA80", "display": "Cough", "system": "ICD-11", "category": "Respiratory"},
    {"code": "DA14", "display": "Diarrhea", "system": "ICD-11", "category": "Digestive"},
    {"code": "8A80", "display": "Headache", "system": "ICD-11", "category": "Neurological"},
    {"code": "BA00", "display": "Heart failure", "system": "ICD-11", "category": "Cardiovascular"},
    {"code": "5A11", "display": "Type 2 diabetes", "system": "ICD-11", "category": "Endocrine"},
]

# Simple code mappings
CODE_MAPPINGS = [
    {"namaste_code": "N001", "icd11_code": "XM001", "mapping_type": "verified"},
    {"namaste_code": "N002", "icd11_code": "XM002", "mapping_type": "verified"},
    {"namaste_code": "N003", "icd11_code": "XM003", "mapping_type": "verified"},
    {"namaste_code": "N004", "icd11_code": "XM004", "mapping_type": "verified"},
    {"namaste_code": "N005", "icd11_code": "XM005", "mapping_type": "verified"},
    
    {"namaste_code": "S001", "icd11_code": "XM001", "mapping_type": "verified"},
    {"namaste_code": "U001", "icd11_code": "XM001", "mapping_type": "verified"},
    {"namaste_code": "N002", "icd11_code": "CA80", "mapping_type": "manual"},
    {"namaste_code": "N003", "icd11_code": "DA14", "mapping_type": "manual"},
]

# Sample users
SAMPLE_USERS = [
    {"user_id": "doc001", "name": "Dr. Priya Sharma", "api_key": "sk_test_doc001_abc123", "role": "doctor"},
    {"user_id": "admin001", "name": "Admin User", "api_key": "sk_test_admin001_xyz789", "role": "admin"},
]
