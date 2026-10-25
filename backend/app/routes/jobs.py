from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Asset, Project
from app.services.storage_service import save_upload

router = APIRouter(prefix="/assets", tags=["assets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/project/{project_id}", response_model=list[dict])
def list_assets(project_id: int, db: Session = Depends(get_db)) -> list[dict]:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    assets = db.query(Asset).filter(Asset.project_id == project_id).order_by(Asset.created_at.desc()).all()
    return [
        {
            "id": asset.id,
            "name": asset.name,
            "kind": asset.kind,
            "file_path": asset.file_path,
            "mime_type": asset.mime_type,
            "source": asset.source,
            "license": asset.license,
            "size_bytes": asset.size_bytes,
        }
        for asset in assets
    ]


@router.post("/project/{project_id}/upload", response_model=dict)
def upload_asset(project_id: int, file: UploadFile = File(...), kind: str = "image", db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    asset = save_upload(project_id=project_id, file=file, kind=kind)
    return {
        "status": "uploaded",
        "asset_id": asset.id,
        "name": asset.name,
        "kind": asset.kind,
        "file_path": asset.file_path,
    }
