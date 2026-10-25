from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import ProviderConfig
from app.schemas import ProviderConfigPayload

router = APIRouter(prefix="/providers", tags=["providers"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[dict])
def list_configs(db: Session = Depends(get_db)) -> list[dict]:
    configs = db.query(ProviderConfig).all()
    return [
        {
            "id": item.id,
            "provider_name": item.provider_name,
            "model_name": item.model_name,
            "enabled": item.enabled,
            "config_json": item.config_json,
        }
        for item in configs
    ]


@router.post("", response_model=dict)
def upsert_config(payload: ProviderConfigPayload, db: Session = Depends(get_db)) -> dict:
    existing = db.query(ProviderConfig).filter(ProviderConfig.provider_name == payload.provider_name).first()
    if existing:
        existing.model_name = payload.model_name
        existing.enabled = payload.enabled
        existing.config_json = str(payload.config_json)
        existing.api_key = payload.api_key
    else:
        item = ProviderConfig(
            provider_name=payload.provider_name,
            api_key=payload.api_key,
            model_name=payload.model_name,
            enabled=payload.enabled,
            config_json=str(payload.config_json),
        )
        db.add(item)
    db.commit()
    return {"status": "saved", "provider_name": payload.provider_name}


@router.get("/{provider_name}", response_model=dict)
def get_config(provider_name: str, db: Session = Depends(get_db)) -> dict:
    item = db.query(ProviderConfig).filter(ProviderConfig.provider_name == provider_name).first()
    if not item:
        raise HTTPException(status_code=404, detail="Provider config not found")
    return {"provider_name": item.provider_name, "model_name": item.model_name, "enabled": item.enabled}
