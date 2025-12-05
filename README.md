# Dyslexia ML Reading Assistant

AI-powered assistive reading companion for dyslexic learners. The system combines speech analysis, gaze/attention sensing, adaptive difficulty, multisensory cues, and a supportive mentor persona to improve fluency, confidence, and engagement.

## Problem & Goal
- Dyslexic learners face persistent hurdles in fluency, pace, and confidence; existing tools are static and costly.
- Goal: deliver adaptive, real-time support that senses attention, detects pronunciation issues, and responds with human-like coaching.

## High-Level Architecture
- **Frontend (web)**: reading workspace (text pane, TTS controls, highlight cues), attention/focus indicator, mentor chat panel, progress widgets.
- **Backend (FastAPI)**: modular services for ASR, attention signals, adaptive difficulty engine, multisensory assistance, and mentor persona orchestration.
- **ML/Signals**:
	- ASR: Whisper API / local Whisper as default; supports Google/Azure pluggability.
	- Attention: webcam gaze + blink metrics via MediaPipe/OpenCV (placeholder API for now).
	- Adaptation: rules + future RL/clustering to adjust word complexity, speed, font spacing.
- **Data**: session logs (errors, pace, gaze), user profiles, content library tagged by level.

## Modules
1) **Listen (Speech Analysis)**: ingest mic audio → ASR → detect mispronunciations, skipped words, timing; return corrective cues and replay samples.
2) **Observe (Attention)**: webcam frames → gaze direction, blink/focus scores; flag fatigue/distraction trends.
3) **Adapt (Difficulty Engine)**: adjust text difficulty, TTS speed, font spacing, hint frequency based on pace/error/engagement signals.
4) **Assist (Multisensory Layer)**: TTS narration, color highlights, syllable segmentation, inline hints.
5) **Mentor Persona**: context-grounded coach that summarizes progress, encourages, and recommends drills; tone configurable (friendly/teacher/calm).

## Tech Stack (proposed)
- **Backend**: Python, FastAPI, pydantic, uvicorn; stub ML hooks for Whisper, MediaPipe/OpenCV; room for RLlib/LightGBM for adaptation.
- **Frontend**: HTML/JS prototype (no build step) with modular CSS; later upgrade to React/Vite if time permits.
- **Persistence**: in-memory session store now; swap to PostgreSQL/Redis in production.
- **TTS/ASR**: Whisper (local or API), Azure Speech, or Google Speech; pluggable provider interface.

## Demo Scenarios (MVP)
- Record or upload audio, get transcript + error spans + suggested pronunciations.
- Simulated attention score returned from backend; UI displays focus bar and suggests breaks.
- Adaptive slider auto-updates reading speed and text complexity from combined signals.
- Mentor panel shows personalized summary: e.g., "Improved 'th' by 20%, focused 7 min; try a quick break." 

## Roadmap
- v0: Static text + mocked ASR/attention + rules-based adaptation + mentor summarization.
- v1: Integrate Whisper ASR + MediaPipe gaze; add syllable highlighting and color cues.
- v2: Add learning-to-rank/RL for difficulty, persistence layer, educator dashboard.

## Running (planned)
- Backend: `cd backend && uvicorn app.main:app --reload`
- Frontend: open `frontend/index.html` in a browser; expects backend at `http://localhost:8000`.

## Inspiration
- Inspired by Lexy: dyslexia-focused ML reading assistants that blend ASR accuracy with supportive coaching; this project mirrors that intent with modular, swappable models.