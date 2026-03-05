# Mini Resume Collector API

## Overview
This project is a **FastAPI-based REST API** that allows uploading candidate resumes and storing candidate metadata.

The application supports:

- Resume upload (PDF/DOC/DOCX)
- Candidate metadata storage
- Candidate filtering and searching
- Retrieve candidate by ID
- Delete candidate
- Health check endpoint

The updated implementation includes **database persistence using SQLite and SQLAlchemy**, ensuring that candidate data remains stored even after server restarts.

---

## Technologies Used

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Pydantic

---

## Installation

Clone the repository:
git clone https://github.com/AslamSuneer/Mini-Resume-Collector-Application.git

## Navigate to the project folder:
cd Mini-Resume-Collector-Application

## Install dependencies:
pip install -r requirements.txt

## Running the Application
Start the FastAPI server:
uvicorn main:app --reload

Server will run at:
http://127.0.0.1:8000

Interactive API documentation:
http://127.0.0.1:8000/docs

## API Endpoints
Health Check:
GET /health

Response:
{
  "status": "healthy"
}

## Upload Resume
POST /upload

Accepts the following form fields:
Full Name,
DOB,
Contact Number,
Contact Address,
Education Qualification,
Graduation Year,
Years of Experience,
Skill Set,
Resume File (PDF/DOC/DOCX)

Example response:
{
  "message": "Candidate uploaded successfully",
  "candidate_id": "uuid-value"
}

## List Candidates
GET /candidates

Optional filters:
skill
experience
graduation_year

Example:
/candidates?skill=python

## Get Candidate by ID
GET /candidates/{candidate_id}

Returns candidate details for the given ID.

## Delete Candidate
DELETE /candidates/{candidate_id}

Deletes the candidate record and associated resume file.

## Database

The application uses SQLite for persistent storage.

Database file created automatically:

resumes.db

Candidate metadata is stored in the candidates table.

## Project Structure
Mini-Resume-Collector-Application
│
├── main.py        # FastAPI application and API endpoints
├── database.py    # Database connection setup
├── models.py      # SQLAlchemy database models
├── schemas.py     # Pydantic validation schemas
├── requirements.txt
├── README.md
│
├── resumes/       # Uploaded resume files
└── resumes.db     # SQLite database
