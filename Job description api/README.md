# Job Description API

A REST API that extracts structured information from job descriptions using Gemini 2.5 Flash.

## Endpoints

- `GET /health` — Check if server is running
- `POST /analyze-job` — Extract title, skills, and seniority from a job description

## Tech Stack
- FastAPI
- Google Gemini 2.5 Flash
- Pydantic
- Uvicorn

## How To Run

1. Clone the repo
2. Create `.env` from `.env.example` and add your Gemini API key
3. Install dependencies:
   pip install -r requirements.txt
4. Start the server:
   uvicorn main:app --reload
5. Open http://127.0.0.1:8000/docs

## Example Request

POST /analyze-job
{
  "description": "We are hiring a Senior Python Developer..."
}

## Example Response

{
  "title": "Senior Python Developer",
  "skills": ["Python", "FastAPI", "Docker"],
  "seniority": "Senior"
}