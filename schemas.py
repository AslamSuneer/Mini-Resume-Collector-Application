from pydantic import BaseModel
from datetime import date
from typing import List

class CandidateCreate(BaseModel):
    full_name: str
    dob: date
    contact_number: str
    contact_address: str
    education_qualification: str
    graduation_year: int
    years_of_experience: float
    skill_set: List[str]

class CandidateResponse(CandidateCreate):
    id: str
    resume_filename: str