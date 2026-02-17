from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import os
import shutil
import uuid

app = FastAPI(title="Mini Resume Collector API")

# In-memory storage
candidates = {}

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# Health Check Endpoint

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}



# Candidate Response Model

class Candidate(BaseModel):
    id: str
    full_name: str = Field(..., min_length=2)
    dob: date
    contact_number: str = Field(..., min_length=10, max_length=15)
    contact_address: str
    education_qualification: str
    graduation_year: int = Field(..., ge=1950, le=2100)
    years_of_experience: float = Field(..., ge=0)
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
    resume: UploadFile = File(...)
):

    # Validate file type (extension check + content type)
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

    candidate = Candidate(
        id=candidate_id,
        full_name=full_name.strip(),
        dob=dob,
        contact_number=contact_number.strip(),
        contact_address=contact_address.strip(),
        education_qualification=education_qualification.strip(),
        graduation_year=graduation_year,
        years_of_experience=years_of_experience,
        skill_set=[s.strip() for s in skill_set.split(",") if s.strip()],
        resume_filename=file_path
    )

    candidates[candidate_id] = candidate

    return {
        "message": "Candidate uploaded successfully",
        "candidate_id": candidate_id
    }



# List Candidates (with filters)

@app.get("/candidates", response_model=List[Candidate])
def list_candidates(
    skill: Optional[str] = None,
    experience: Optional[float] = None,
    graduation_year: Optional[int] = None
):

    results = list(candidates.values())

    if skill:
        results = [
            c for c in results
            if skill.lower() in [s.lower() for s in c.skill_set]
        ]

    if experience is not None:
        results = [
            c for c in results
            if c.years_of_experience >= experience
        ]

    if graduation_year:
        results = [
            c for c in results
            if c.graduation_year == graduation_year
        ]

    return results



#  Get Candidate by ID

@app.get("/candidates/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: str):
    candidate = candidates.get(candidate_id)

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    return candidate


#  Delete Candidate

@app.delete("/candidates/{candidate_id}", status_code=status.HTTP_200_OK)
def delete_candidate(candidate_id: str):
    candidate = candidates.get(candidate_id)

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    # Delete stored file
    if os.path.exists(candidate.resume_filename):
        os.remove(candidate.resume_filename)

    del candidates[candidate_id]

    return {"message": "Candidate deleted successfully"}
