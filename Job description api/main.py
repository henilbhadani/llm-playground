from json import JSONDecodeError

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import Optional
from google import genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
api_key = os.getenv("API_KEY")

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    raise RuntimeError(f"Failed to initialize gemini client: {e}")

app = FastAPI()

class JobRequest(BaseModel):
    description: str

class JobResponse(BaseModel):
    title: Optional[str] = None
    skills: Optional[list[str]] = None
    seniority: Optional[str] = None

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running"}

@app.post("/analyze-job", response_model = JobResponse)
async def analyze_job(request: JobRequest):

    prompt = f"""
    You are an information extraction system.
    
    Extract information from the job description.
    
    Rules:
    1. Return ONLY valid JSON.
    2. Do not include explanations.
    3. Extract every skill mentioned.
    4. If information is missing, use null.
    
    JSON Schema:
    {{
      "title": "",
      "skills": [],
      "seniority": ""
    }}
    
    Job Description:
    {request.description}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents = prompt
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini api call failed :{str(e)}")

    raw = response.text
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        raise HTTPException(status_code=500, detail=f"no json found in model response: {raw}")

    try:
        data= json.loads(match.group())
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"failed to parse JSON: {str(e)}")

    try:
        job = JobResponse(**data)
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"response validation failed :{str(e)}")

    return job