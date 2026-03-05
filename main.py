from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import os
import shutil
import uuid

from sqlalchemy import create_engine, Column, String, Integer, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI(title="Mini Resume Collector API")

# DATABASE SETUP

DATABASE_URL = "sqlite:///./resumes.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# DATABASE MODEL

class CandidateDB(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    dob = Column(Date)
    contact_number = Column(String)
    contact_address = Column(String)
    education_qualification = Column(String)
    graduation_year = Column(Integer)
    years_of_experience = Column(Float)
    skill_set = Column(String)
    resume_filename = Column(String)


Base.metadata.create_all(bind=engine)


# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# File Storage

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


<<<<<<< HEAD

# Health Check
=======
# Health Check
>>>>>>> 6704288 (Added database persistence using SQLite and SQLAlchemy)

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}


<<<<<<< HEAD

# Candidate Response Model
=======
# Response Model
>>>>>>> 6704288 (Added database persistence using SQLite and SQLAlchemy)

class Candidate(BaseModel):
    id: str
    full_name: str
    dob: date
    contact_number: str
    contact_address: str
    education_qualification: str
    graduation_year: int
    years_of_experience: float
    skill_set: List[str]
    resume_filename: str


# Upload Resume

@app.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    full_name: str = Form(...),
    dob: date = Form(...),
    contact_number: str = Form(...),
    contact_address: str = Form(...),
    education_qualification: str = Form(...),
    graduation_year: int = Form(...),
    years_of_experience: float = Form(...),
    skill_set: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]

    if resume.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOC, DOCX files are allowed"
        )

    candidate_id = str(uuid.uuid4())

    file_path = os.path.join(UPLOAD_FOLDER, f"{candidate_id}_{resume.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    db_candidate = CandidateDB(
        id=candidate_id,
        full_name=full_name.strip(),
        dob=dob,
        contact_number=contact_number.strip(),
        contact_address=contact_address.strip(),
        education_qualification=education_qualification.strip(),
        graduation_year=graduation_year,
        years_of_experience=years_of_experience,
        skill_set=skill_set,
        resume_filename=file_path
    )

    db.add(db_candidate)
    db.commit()

    return {
        "message": "Candidate uploaded successfully",
        "candidate_id": candidate_id
    }


<<<<<<< HEAD

# List Candidates (with filters)
=======
# List Candidates
>>>>>>> 6704288 (Added database persistence using SQLite and SQLAlchemy)

@app.get("/candidates", response_model=List[Candidate])
def list_candidates(
    skill: Optional[str] = None,
    experience: Optional[float] = None,
    graduation_year: Optional[int] = None,
    db: Session = Depends(get_db)
):

    candidates = db.query(CandidateDB).all()

    results = []

    for c in candidates:
        skills = [s.strip() for s in c.skill_set.split(",")]

        if skill and skill.lower() not in [s.lower() for s in skills]:
            continue

        if experience is not None and c.years_of_experience < experience:
            continue

        if graduation_year and c.graduation_year != graduation_year:
            continue

        results.append(
            Candidate(
                id=c.id,
                full_name=c.full_name,
                dob=c.dob,
                contact_number=c.contact_number,
                contact_address=c.contact_address,
                education_qualification=c.education_qualification,
                graduation_year=c.graduation_year,
                years_of_experience=c.years_of_experience,
                skill_set=skills,
                resume_filename=c.resume_filename
            )
        )

    return results


<<<<<<< HEAD

#  Get Candidate by ID
=======
# Get Candidate by ID
>>>>>>> 6704288 (Added database persistence using SQLite and SQLAlchemy)

@app.get("/candidates/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: str, db: Session = Depends(get_db)):

    candidate = db.query(CandidateDB).filter(CandidateDB.id == candidate_id).first()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    return Candidate(
        id=candidate.id,
        full_name=candidate.full_name,
        dob=candidate.dob,
        contact_number=candidate.contact_number,
        contact_address=candidate.contact_address,
        education_qualification=candidate.education_qualification,
        graduation_year=candidate.graduation_year,
        years_of_experience=candidate.years_of_experience,
        skill_set=[s.strip() for s in candidate.skill_set.split(",")],
        resume_filename=candidate.resume_filename
    )


<<<<<<< HEAD
#  Delete Candidate

@app.delete("/candidates/{candidate_id}", status_code=status.HTTP_200_OK)
def delete_candidate(candidate_id: str):
    candidate = candidates.get(candidate_id)
=======
# Delete Candidate

@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: str, db: Session = Depends(get_db)):

    candidate = db.query(CandidateDB).filter(CandidateDB.id == candidate_id).first()
>>>>>>> 6704288 (Added database persistence using SQLite and SQLAlchemy)

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    if os.path.exists(candidate.resume_filename):
        os.remove(candidate.resume_filename)

    db.delete(candidate)
    db.commit()

    return {"message": "Candidate deleted successfully"}