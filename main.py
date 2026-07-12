from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import os

# -----------------------------
# Initialize FastAPI
# -----------------------------
app = FastAPI(
    title="Maave AI API",
    description="AI-powered maternal health assistant",
    version="1.0.0"
)

# -----------------------------
# Gemini Client
# -----------------------------
# The API key is read from the GEMINI_API_KEY environment variable.
# On Render, set this under your service's "Environment" tab.
# Locally, you can set it via: export GEMINI_API_KEY=your_key_here
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set. "
        "Set it in your environment (or Render's dashboard) before starting the app."
    )

client = genai.Client(api_key="GEMINI_API_KEY")

# -----------------------------
# Request Model
# -----------------------------
class EPDSRequest(BaseModel):
    mother_name: str
    baby_age_weeks: int
    score: int
    risk: str

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Welcome to the Maave AI API."
    }

# -----------------------------
# Health Check Endpoint
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# -----------------------------
# AI Function
# -----------------------------
def generate_epds_ai_response(
    mother_name,
    baby_age_weeks,
    score,
    risk
):

    prompt = f"""
You are Maave AI.

A mother has completed the Edinburgh Postnatal Depression Scale screening.

Mother Name:
{mother_name}

Baby Age:
{baby_age_weeks} weeks

EPDS Score:
{score}

Risk Category:
{risk}

Your task:

Explain the results in simple language.

Rules:
- Do NOT diagnose postpartum depression.
- Do NOT change the score.
- Do NOT change the risk category.
- Be warm and supportive.
- Recommend speaking to a healthcare professional when appropriate.
- Keep the response below 150 words.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# -----------------------------
# AI Endpoint
# -----------------------------
@app.post("/epds-ai")
def epds_ai(request: EPDSRequest):

    try:

        message = generate_epds_ai_response(
            request.mother_name,
            request.baby_age_weeks,
            request.score,
            request.risk
        )

        return {
            "status": "success",
            "message": message
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
