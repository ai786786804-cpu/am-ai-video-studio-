# A M AI Studio

A professional AI-powered video creation platform for turning scripts into cinematic storyboards, narrated scenes, and rendered MP4 videos.

## Features implemented

- Responsive dashboard and project workspace
- New project creation and project persistence
- Script analysis workflow with scene breakdown generation
- Character-centric project data model
- Asset uploads and media library
- Timeline scene management
- FFmpeg render job support with validation and truthful error states
- Provider configuration storage for AI integrations
- Demo-mode workflow without paid AI providers

## Stack

- Frontend: React + TypeScript + Vite
- Backend: FastAPI + Python
- Database: SQLite + SQLAlchemy
- Rendering: FFmpeg / FFprobe
- Testing: Pytest (ready for workflow tests)

## Start backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Start frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Open the app

- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs

## Required environment variables

```bash
OPENAI_API_KEY=
GOOGLE_API_KEY=
ELEVENLABS_API_KEY=
STABILITY_API_KEY=
```

These are optional. The app can run in demo mode when providers are not configured.

## Notes

- SQLite is used for development simplicity and can be migrated to Postgres later.
- FFmpeg output is generated only when FFmpeg is installed and valid.
- The app intentionally reports errors when external services or rendering dependencies are unavailable.
