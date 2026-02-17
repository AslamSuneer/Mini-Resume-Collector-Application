\# Mini Resume Collector API



\## Python Version

Python 3.13.0



\## Installation



1\. Clone the repository

2\. Install dependencies



pip install -r requirements.txt



\## Run Application



uvicorn main:app --reload



Application runs at:

http://127.0.0.1:8000



Swagger Documentation:

http://127.0.0.1:8000/docs



\## API Endpoints



GET /health  

POST /upload  

GET /candidates  

GET /candidates/{candidate\_id}  

DELETE /candidates/{candidate\_id}



\## Example Response



{

&nbsp; "message": "Candidate uploaded successfully",

&nbsp; "candidate\_id": "uuid-value"

}



