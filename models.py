from sqlalchemy import Column, String, Integer, Float, Date
from database import Base

class Candidate(Base):
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