from __future__ import annotations

from pathlib import Path

from fastapi import UploadFile

from app.database import SessionLocal
from app.models import Asset


def save_upload(project_id: int, file: UploadFile, kind: str) -> Asset:
    storage_root = Path(__file__).resolve().parents[1] / "data" / "uploads"
    storage_root.mkdir(parents=True, exist_ok=True)
    safe_name = file.filename.replace("/", "_").replace("\\", "_")
    target = storage_root / safe_name
    content = file.file.read()
    target.write_bytes(content)

    db = SessionLocal()
    asset = Asset(
        project_id=project_id,
        name=safe_name,
        kind=kind,
        file_path=str(target),
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=len(content),
        source="upload",
        license="project-managed",
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    db.close()
    return asset
