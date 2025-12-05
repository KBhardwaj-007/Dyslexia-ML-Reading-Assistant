# Backend (FastAPI)

Prototype API exposing the five core modules: Listen, Observe, Adapt, Assist, and Mentor.

## Install & Run
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API root: http://localhost:8000
Docs: http://localhost:8000/docs

## Endpoints
- `POST /listen/analyze` — mock speech analysis returns transcript accuracy, pace, and error spans.
- `POST /observe/analyze` — attention/fatigue estimation from focus score and blink rate.
- `POST /adapt/plan` — suggests next difficulty, spacing, and TTS speed.
- `POST /assist/assist` — returns mock TTS preview link and highlight spans.
- `POST /mentor/coach` — persona-based motivational feedback and next steps.
- `POST /sessions/log` — persists session summary (accuracy/focus/pace/level) to SQLite.

These endpoints use lightweight heuristics; swap in Whisper/MediaPipe/RL models via the service layer when available.
