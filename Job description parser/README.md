# Job Description Parser

Extracts structured information from job descriptions using Gemini 2.5 Flash + Pydantic.

## What it does
Paste any job description → get back structured JSON with title, required skills, and seniority level.

## Tech used
- Google Gemini 2.5 Flash API
- Pydantic for data validation
- Python-dotenv for environment variables

## How to run
1. Clone the repo
2. Create `.env` file from `.env.example` and add your Gemini API key
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`
5. Paste job description, type END when done

## Example output
{
  "title": "Junior AI Engineer",
  "skills": ["Python", "FastAPI", "LLM applications", "Git"],
  "seniority": "Junior"
}