from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from typing import Optional
import os
import json
import re

try:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    client = genai.Client(api_key=api_key)

except Exception as e:
    print("Please provide a valid API key.")
    raise e


class JobInfo(BaseModel):
    title: Optional[str] = None
    skills: Optional[list[str]] = None
    seniority: Optional[str] = None


lines = []
print("Give the job description.")
print("Type END on a new line when finished.")

while True:
    line = input()
    if line == "END":
        break
    lines.append(line)

user_input = "\n".join(lines)

toggle = input("Do you want streaming response? (yes/no): ")

if toggle.lower().strip() == "yes":
    streaming = True
else:
    streaming = False

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
{user_input}
"""

try:
    if streaming:
        print("\n=== STREAMING VERSION ===\n")

        chunks = []

        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=prompt
        ):
            print(chunk.text, end="", flush=True)
            chunks.append(chunk.text)

        raw = "".join(chunks)

    else:
        print("\n=== NON STREAMING VERSION ===\n")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        print(response.text)
        raw = response.text

    match = re.search(r"\{.*\}", raw, re.DOTALL)

    if not match:
        raise ValueError(f"No JSON object found in response:\n{raw}")

    clean_response = match.group()

    try:
        data = json.loads(clean_response)

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from model response: {e}")
        print(f"Raw response was:\n{raw}")
        raise

    try:
        job = JobInfo(**data)

        print("\nParsed Data:")
        print(job)

        print("\nTitle:")
        print(job.title)

        print("\nSkills:")
        print(job.skills)

        print("\nSeniority:")
        print(job.seniority)

    except ValidationError as e:
        print("\nValidation Error:")
        print(e)

except Exception as e:
    print(f"\nAPI call failed: {e}")
    raise