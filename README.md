# A M AI Studio

A professional AI-powered video production platform for turning scripts into cinematic storyboards, narrated scenes, and rendered MP4 videos.

## Features

- Responsive dashboard and project workspace
- Script analysis and storyboard generation
- Character library and style presets
- Scene management, asset assignment, timeline editing
- Audio and subtitle settings
- FFmpeg-based video render pipeline with validation
- Provider abstraction for AI services
- SQLite-backed persistence for local development
- Demo mode when no external providers are configured

## Stack

- Frontend: React + TypeScript + Vite
- Backend: FastAPI + Python
- Database: SQLite + SQLAlchemy
- Rendering: FFmpeg / FFprobe
- Testing: Pytest

## Quick start

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

### 3) Open the app

Visit:

- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs

## Required environment variables

```bash
OPENAI_API_KEY=
GOOGLE_API_KEY=
ELEVENLABS_API_KEY=
STABILITY_API_KEY=
```

Only set values for providers you actually use. The app remains usable in demo mode without credentials.

## Notes

- The project uses SQLite for easy local development and can be migrated to PostgreSQL later.
- Video export depends on FFmpeg being installed on the host machine.
- If FFmpeg or provider credentials are missing, the app will expose honest error states instead of fake success.

## Future enhancements

- PostgreSQL migration
- Job queue with Celery/Redis
- S3-compatible storage
- Real LLM, TTS, and image-generation adapters
- Advanced multi-track editing and subtitle timing validation
