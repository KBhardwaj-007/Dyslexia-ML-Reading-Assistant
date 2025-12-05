# Frontend Prototype

Static HTML/CSS/JS demo (no build step) showcasing the reading workspace and calls to the FastAPI backend.

## Run
Open `frontend/index.html` in a browser. The buttons call the backend at `http://localhost:8000`.

## Panels
- Reading workspace with text area, target word entry, and module buttons.
- Metrics chips for accuracy, pace, focus, and next difficulty level.
- Mentor persona card that shows supportive feedback.

The calls are mocked today; connect to live ASR/gaze endpoints by swapping the FastAPI services.
