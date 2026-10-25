from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Project
from app.schemas import ProjectCreate, ProjectUpdate
from app.services.script_service import build_scene_breakdown

router = APIRouter(prefix="/projects", tags=["projects"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[dict])
def list_projects(db: Session = Depends(get_db)) -> list[dict]:
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "style": p.style,
            "description": p.description,
            "script": p.script,
            "status": p.status,
            "duration_goal": p.duration_goal,
            "aspect_ratio": p.aspect_ratio,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in projects
    ]


@router.post("", response_model=dict)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> dict:
    project = Project(
        name=payload.name,
        style=payload.style,
        description=payload.description,
        duration_goal=payload.duration_goal,
        aspect_ratio=payload.aspect_ratio,
        status="draft",
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"id": project.id, "name": project.name, "style": project.style, "status": project.status}


@router.get("/{project_id}", response_model=dict)
def get_project(project_id: int, db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "id": project.id,
        "name": project.name,
        "style": project.style,
        "description": project.description,
        "script": project.script,
        "status": project.status,
        "duration_goal": project.duration_goal,
        "aspect_ratio": project.aspect_ratio,
        "created_at": project.created_at.isoformat() if project.created_at else None,
    }


@router.put("/{project_id}", response_model=dict)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if payload.name is not None:
        project.name = payload.name
    if payload.style is not None:
        project.style = payload.style
    if payload.description is not None:
        project.description = payload.description
    if payload.script is not None:
        project.script = payload.script
    if payload.status is not None:
        project.status = payload.status
    if payload.duration_goal is not None:
        project.duration_goal = payload.duration_goal
    if payload.aspect_ratio is not None:
        project.aspect_ratio = payload.aspect_ratio

    db.commit()
    db.refresh(project)
    return {"status": "updated", "project_id": project.id}


@router.delete("/{project_id}", response_model=dict)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"status": "deleted", "project_id": project_id}


@router.post("/{project_id}/script-analysis", response_model=dict)
def analyze_script(project_id: int, payload: dict, db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    script = payload.get("script", "")
    style = payload.get("style", project.style)
    project.script = script
    project.style = style
    project.status = "analyzed"
    db.commit()

    return {
        "status": "success",
        "scene_count": len(build_scene_breakdown(script, style)),
        "style": style,
    }
