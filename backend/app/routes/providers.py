from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Project, RenderJob
from app.services.script_service import build_project_render, ffmpeg_available

router = APIRouter(prefix="/jobs", tags=["jobs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[dict])
def list_jobs(db: Session = Depends(get_db)) -> list[dict]:
    jobs = db.query(RenderJob).order_by(RenderJob.created_at.desc()).all()
    return [
        {
            "id": job.id,
            "project_id": job.project_id,
            "status": job.status,
            "progress": job.progress,
            "output_path": job.output_path,
            "error_message": job.error_message,
            "created_at": job.created_at.isoformat() if job.created_at else None,
        }
        for job in jobs
    ]


@router.post("/render/{project_id}", response_model=dict)
def create_render_job(project_id: int, db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    job = RenderJob(project_id=project_id, status="queued", progress=5)
    db.add(job)
    db.commit(); db.refresh(job)

    if not ffmpeg_available():
        job.status = "failed"
        job.progress = 0
        job.error_message = "FFmpeg is not installed or not executable in this environment."
        db.commit()
        return {"status": "failed", "job_id": job.id, "error": job.error_message}

    try:
        output = build_project_render(project_id)
        job.status = "completed"
        job.progress = 100
        job.output_path = output
        job.completed_at = datetime.utcnow()
        db.commit()
        return {"status": "completed", "job_id": job.id, "output_path": output}
    except Exception as exc:  # pragma: no cover
        job.status = "failed"
        job.progress = 0
        job.error_message = str(exc)
        db.commit()
        return {"status": "failed", "job_id": job.id, "error": str(exc)}


@router.get("/{job_id}", response_model=dict)
def get_job(job_id: int, db: Session = Depends(get_db)) -> dict:
    job = db.query(RenderJob).filter(RenderJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": job.id,
        "project_id": job.project_id,
        "status": job.status,
        "progress": job.progress,
        "output_path": job.output_path,
        "error_message": job.error_message,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
    }
