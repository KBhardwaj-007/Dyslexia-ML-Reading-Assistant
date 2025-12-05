# Frontend Prototype

React + Vite frontend for the Dyslexia ML Reading Assistant.

## Run (dev)
```bash
cd frontend
npm install
npm run dev -- --host
```
Frontend runs on http://localhost:5173. Set backend API base via `VITE_API_BASE` (default http://localhost:8000).

## Build
```bash
npm run build
npm run preview
```

## Features
- Reading workspace with text area, target word entry, and module buttons.
- Record + Whisper: captures 4s audio and sends to `/listen/upload`.
- Attention: optional webcam frames streamed to `/observe/analyze`.
- Adaptation, assist, mentor, and session logging wired to FastAPI endpoints.
- Metrics for accuracy, pace, focus, and next level.
