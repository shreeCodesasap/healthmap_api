from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite database file
DATABASE_URL = "sqlite:///./medical_codes.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class NamasteCode(Base):
    __tablename__ = "namaste_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True)
    display = Column(String(200), nullable=False)
    system = Column(String(20), default="NAMASTE")
    category = Column(String(50))  # Ayurveda, Siddha, Unani
    created_at = Column(DateTime, default=datetime.utcnow)

class ICD11Code(Base):
    __tablename__ = "icd11_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True)
    display = Column(String(200), nullable=False)
    system = Column(String(20), nullable=False)  # ICD-11 or ICD-11-TM2
    category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class CodeMapping(Base):
    __tablename__ = "code_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    namaste_code = Column(String(10), nullable=False)
    icd11_code = Column(String(20), nullable=False)
    mapping_type = Column(String(20), default="verified")  # verified, manual, auto
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), unique=True, index=True)
    name = Column(String(100))
    api_key = Column(String(100), unique=True, index=True)
    role = Column(String(20), default="doctor")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserEncounter(Base):
    __tablename__ = "user_encounters"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False)
    patient_id = Column(String(50))
    namaste_code = Column(String(10))
    icd11_code = Column(String(20))
    action_type = Column(String(20))  # search, translate, upload
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
