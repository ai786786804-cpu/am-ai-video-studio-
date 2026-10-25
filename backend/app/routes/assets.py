from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Project, Scene
from app.schemas import ScenePayload
from app.services.script_service import build_scene_breakdown

router = APIRouter(prefix="/scenes", tags=["scenes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/project/{project_id}", response_model=list[dict])
def list_scenes(project_id: int, db: Session = Depends(get_db)) -> list[dict]:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    scenes = db.query(Scene).filter(Scene.project_id == project_id).order_by(Scene.order_index.asc()).all()
    return [
        {
            "id": s.id,
            "project_id": s.project_id,
            "title": s.title,
            "narration": s.narration,
            "visual_description": s.visual_description,
            "prompt": s.prompt,
            "background": s.background,
            "camera": s.camera,
            "duration": s.duration,
            "order_index": s.order_index,
            "subtitle_text": s.subtitle_text,
            "status": s.status,
            "generated_asset": s.generated_asset,
        }
        for s in scenes
    ]


@router.post("/project/{project_id}/generate", response_model=dict)
def generate_scenes(project_id: int, db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not project.script:
        raise HTTPException(status_code=400, detail="Project script is empty")

    breakdown = build_scene_breakdown(project.script, project.style)
    existing = db.query(Scene).filter(Scene.project_id == project_id).all()
    for item in existing:
        db.delete(item)
    db.commit()

    for idx, scene_payload in enumerate(breakdown, start=1):
        record = Scene(
            project_id=project_id,
            title=scene_payload["title"],
            narration=str(scene_payload["narration"]),
            visual_description=str(scene_payload["visual_description"]),
            prompt=str(scene_payload["prompt"]),
            background=str(scene_payload["background"]),
            camera=str(scene_payload["camera"]),
            duration=int(scene_payload["duration"]),
            order_index=idx,
            subtitle_text=str(scene_payload["subtitle_text"]),
            status="planned",
        )
        db.add(record)
    db.commit()
    return {"status": "success", "count": len(breakdown)}


@router.post("/project/{project_id}", response_model=dict)
def create_scene(project_id: int, payload: ScenePayload, db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    count = db.query(Scene).filter(Scene.project_id == project_id).count()
    scene = Scene(
        project_id=project_id,
        title=payload.title,
        narration=payload.narration,
        visual_description=payload.visual_description,
        prompt=payload.prompt,
        background=payload.background,
        camera=payload.camera,
        duration=payload.duration,
        order_index=count + 1,
        subtitle_text=payload.subtitle_text,
        status=payload.status,
    )
    scene.set_character_ids(payload.character_ids)
    db.add(scene)
    db.commit()
    db.refresh(scene)
    return {"id": scene.id, "title": scene.title, "status": scene.status}


@router.put("/project/{project_id}/{scene_id}", response_model=dict)
def update_scene(project_id: int, scene_id: int, payload: dict, db: Session = Depends(get_db)) -> dict:
    scene = db.query(Scene).filter(Scene.id == scene_id, Scene.project_id == project_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    for field in ["title", "narration", "visual_description", "prompt", "background", "camera", "subtitle_text", "status"]:
        if field in payload:
            setattr(scene, field, payload[field])
    if "duration" in payload:
        scene.duration = int(payload["duration"])
    if "character_ids" in payload:
        scene.set_character_ids(payload["character_ids"])
    db.commit()
    return {"status": "updated", "scene_id": scene.id}
