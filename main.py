from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db, create_tables, NamasteCode, ICD11Code, CodeMapping, User, UserEncounter
from sampledata import NAMASTE_CODES, ICD11_CODES, CODE_MAPPINGS, SAMPLE_USERS
from datetime import datetime
from fuzzywuzzy import fuzz
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI(title="NAMASTE-ICD11 Integration API", version="1.0.0")

# Pydantic models for API requests/responses
class SearchResult(BaseModel):
    code: str
    display: str
    system: str
    category: str
    relevance_score: int

class TranslationRequest(BaseModel):
    code: str
    from_system: str
    to_system: str

class TranslationResult(BaseModel):
    source_code: str
    target_code: str
    target_display: str
    mapping_type: str

class EncounterRequest(BaseModel):
    patient_id: str
    namaste_code: str
    icd11_code: str

# Authentication helper
def verify_api_key(api_key: Optional[str] = Header(None)):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    return api_key

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    create_tables()
    print("✅ Database tables created successfully!")

@app.get("/")
async def root():
    return {
        "message": "NAMASTE-ICD11 Medical Coding API", 
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {"status": "ok", "service": "namaste-icd-api"}

@app.get("/setup-database")
async def setup_database(db: Session = Depends(get_db)):
    """Load sample data into database"""
    try:
        # Check if data already exists
        if db.query(NamasteCode).first():
            return {"message": "Database already has data", "status": "skipped"}
        
        # Load NAMASTE codes
        for code_data in NAMASTE_CODES:
            namaste_code = NamasteCode(**code_data)
            db.add(namaste_code)
        
        # Load ICD-11 codes
        for code_data in ICD11_CODES:
            icd11_code = ICD11Code(**code_data)
            db.add(icd11_code)
        
        # Load code mappings
        for mapping_data in CODE_MAPPINGS:
            mapping = CodeMapping(**mapping_data)
            db.add(mapping)
        
        # Load sample users
        for user_data in SAMPLE_USERS:
            user = User(**user_data)
            db.add(user)
        
        db.commit()
        
        # Count records
        namaste_count = db.query(NamasteCode).count()
        icd11_count = db.query(ICD11Code).count()
        mapping_count = db.query(CodeMapping).count()
        user_count = db.query(User).count()
        
        return {
            "message": "Database setup complete!",
            "data_loaded": {
                "namaste_codes": namaste_count,
                "icd11_codes": icd11_count, 
                "code_mappings": mapping_count,
                "users": user_count
            }
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database setup failed: {str(e)}")

@app.get("/database-status")
async def database_status(db: Session = Depends(get_db)):
    """Check database status and record counts"""
    try:
        namaste_count = db.query(NamasteCode).count()
        icd11_count = db.query(ICD11Code).count()
        mapping_count = db.query(CodeMapping).count()
        user_count = db.query(User).count()
        
        return {
            "status": "connected",
            "tables": {
                "namaste_codes": namaste_count,
                "icd11_codes": icd11_count,
                "code_mappings": mapping_count,
                "users": user_count,
                "user_encounters": db.query(UserEncounter).count()
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 1. SMART SEARCH ENDPOINT
@app.get("/api/search", response_model=List[SearchResult])
async def search_codes(
    q: str, 
    system: str = "both", 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Search for medical codes across NAMASTE and ICD-11 systems
    - q: search query (e.g., "fever", "cough")
    - system: "namaste", "icd11", or "both"
    - limit: maximum number of results
    """
    results = []
    
    try:
        # Search NAMASTE codes
        if system in ["namaste", "both"]:
            namaste_codes = db.query(NamasteCode).all()
            for code in namaste_codes:
                # Calculate relevance using fuzzy matching
                display_score = fuzz.partial_ratio(q.lower(), code.display.lower())
                code_score = fuzz.partial_ratio(q.lower(), code.code.lower())
                max_score = max(display_score, code_score)
                
                if max_score > 50:  # Only include if relevance > 50%
                    results.append(SearchResult(
                        code=code.code,
                        display=code.display,
                        system=code.system,
                        category=code.category,
                        relevance_score=max_score
                    ))
        
        # Search ICD-11 codes
        if system in ["icd11", "both"]:
            icd11_codes = db.query(ICD11Code).all()
            for code in icd11_codes:
                display_score = fuzz.partial_ratio(q.lower(), code.display.lower())
                code_score = fuzz.partial_ratio(q.lower(), code.code.lower())
                max_score = max(display_score, code_score)
                
                if max_score > 50:
                    results.append(SearchResult(
                        code=code.code,
                        display=code.display,
                        system=code.system,
                        category=code.category,
                        relevance_score=max_score
                    ))
        
        # Sort by relevance score (highest first) and limit results
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# 2. CODE TRANSLATION ENDPOINT
@app.post("/api/translate", response_model=List[TranslationResult])
async def translate_code(
    request: TranslationRequest,
    db: Session = Depends(get_db)
):
    """
    Translate codes between NAMASTE and ICD-11 systems
    """
    results = []
    
    try:
        if request.from_system == "NAMASTE" and request.to_system == "ICD-11":
            # NAMASTE to ICD-11 translation
            mappings = db.query(CodeMapping).filter(
                CodeMapping.namaste_code == request.code
            ).all()
            
            for mapping in mappings:
                icd11_code = db.query(ICD11Code).filter(
                    ICD11Code.code == mapping.icd11_code
                ).first()
                
                if icd11_code:
                    results.append(TranslationResult(
                        source_code=request.code,
                        target_code=icd11_code.code,
                        target_display=icd11_code.display,
                        mapping_type=mapping.mapping_type
                    ))
        
        elif request.from_system == "ICD-11" and request.to_system == "NAMASTE":
            # ICD-11 to NAMASTE translation
            mappings = db.query(CodeMapping).filter(
                CodeMapping.icd11_code == request.code
            ).all()
            
            for mapping in mappings:
                namaste_code = db.query(NamasteCode).filter(
                    NamasteCode.code == mapping.namaste_code
                ).first()
                
                if namaste_code:
                    results.append(TranslationResult(
                        source_code=request.code,
                        target_code=namaste_code.code,
                        target_display=namaste_code.display,
                        mapping_type=mapping.mapping_type
                    ))
        
        if not results:
            raise HTTPException(
                status_code=404, 
                detail=f"No translation found for {request.code} from {request.from_system} to {request.to_system}"
            )
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

# 3. ENCOUNTER UPLOAD ENDPOINT (with authentication)
@app.post("/api/encounter")
async def upload_encounter(
    request: EncounterRequest,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    Upload patient encounter with dual coding (requires API key)
    """
    try:
        # Verify API key exists
        user = db.query(User).filter(User.api_key == api_key).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        # Verify codes exist
        namaste_code = db.query(NamasteCode).filter(
            NamasteCode.code == request.namaste_code
        ).first()
        icd11_code = db.query(ICD11Code).filter(
            ICD11Code.code == request.icd11_code
        ).first()
        
        if not namaste_code:
            raise HTTPException(status_code=400, detail=f"NAMASTE code {request.namaste_code} not found")
        if not icd11_code:
            raise HTTPException(status_code=400, detail=f"ICD-11 code {request.icd11_code} not found")
        
        # Create encounter record
        encounter = UserEncounter(
            user_id=user.user_id,
            patient_id=request.patient_id,
            namaste_code=request.namaste_code,
            icd11_code=request.icd11_code,
            action_type="upload"
        )
        
        db.add(encounter)
        db.commit()
        
        return {
            "message": "Encounter uploaded successfully",
            "encounter_id": encounter.id,
            "patient_id": request.patient_id,
            "codes": {
                "namaste": {
                    "code": namaste_code.code,
                    "display": namaste_code.display
                },
                "icd11": {
                    "code": icd11_code.code,
                    "display": icd11_code.display
                }
            },
            "uploaded_by": user.name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# 4. GET USER'S ENCOUNTERS
@app.get("/api/encounters")
async def get_encounters(
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Get all encounters for the authenticated user"""
    try:
        user = db.query(User).filter(User.api_key == api_key).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        encounters = db.query(UserEncounter).filter(
            UserEncounter.user_id == user.user_id
        ).order_by(UserEncounter.timestamp.desc()).all()
        
        return {
            "user": user.name,
            "total_encounters": len(encounters),
            "encounters": [
                {
                    "id": enc.id,
                    "patient_id": enc.patient_id,
                    "namaste_code": enc.namaste_code,
                    "icd11_code": enc.icd11_code,
                    "action_type": enc.action_type,
                    "timestamp": enc.timestamp
                }
                for enc in encounters
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get encounters: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
