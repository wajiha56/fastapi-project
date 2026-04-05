from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ---------------------------------------------------------
# 1. DATABASE SETUP
# ---------------------------------------------------------
DATABASE_URL = "sqlite:///./patients.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# ---------------------------------------------------------
# 2. DATABASE MODEL
# ---------------------------------------------------------
class PatientDB(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

# Create DB tables
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------
# 3. PYDANTIC SCHEMA
# ---------------------------------------------------------
class PatientCreate(BaseModel):
    name: str
    age: int


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int

    model_config = ConfigDict(from_attributes=True)

# ---------------------------------------------------------
# 4. FASTAPI APP
# ---------------------------------------------------------
app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# 5. POST API (SAVE + SMS)
# ---------------------------------------------------------
@app.post("/patients/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):

    new_patient = PatientDB(name=patient.name, age=patient.age)

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    # 👉 Twilio yahan add karna hai
    print(f"SMS sent for {new_patient.name}")

    return new_patient

# ---------------------------------------------------------
# 6. GET API (FETCH DATA)
# ---------------------------------------------------------
@app.get("/patients/", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return db.query(PatientDB).all()