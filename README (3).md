# Maave AI API

AI-powered maternal health assistant that explains EPDS (Edinburgh Postnatal
Depression Scale) screening results in warm, simple language via the Gemini API.

## Before you push to GitHub

Your API key must **never** be committed to the repo. Add a `.gitignore` file
containing at least:

```
.env
__pycache__/
*.pyc
```

Do not put your real Gemini key in any file that gets committed. It's read
from an environment variable at runtime (see below).

⚠️ Also: the key that was hardcoded in your original file should be treated as
compromised — rotate/regenerate it in Google AI Studio before deploying, since
it may already be exposed in your local git history or elsewhere.

## Local development

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

export GEMINI_API_KEY=your_key_here   # Windows: set GEMINI_API_KEY=your_key_here
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000` and `http://127.0.0.1:8000/docs` for the
interactive Swagger UI.

## Deploying on Render

1. Push this project (main.py, requirements.txt, .gitignore) to a GitHub repo.
2. On [Render](https://render.com), click **New +** → **Web Service**.
3. Connect your GitHub repo.
4. Configure the service:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Under **Environment Variables**, add:
   - `GEMINI_API_KEY` = your Gemini API key
6. Click **Create Web Service**. Render will build and deploy automatically,
   and redeploy on future pushes to your connected branch.

## Endpoints

- `GET /` — welcome/status check
- `GET /health` — health check (useful for Render's health checks / uptime monitors)
- `POST /epds-ai` — generates a supportive explanation of EPDS results

  Request body:
  ```json
  {
    "mother_name": "Jane",
    "baby_age_weeks": 6,
    "score": 12,
    "risk": "moderate"
  }
  ```

  Response:
  ```json
  {
    "status": "success",
    "message": "..."
  }
  ```
