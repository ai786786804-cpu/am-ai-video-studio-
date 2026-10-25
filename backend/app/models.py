from __future__ import annotations

import json
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    style = Column(String(80), nullable=False, default="Stickman")
    description = Column(Text, default="")
    script = Column(Text, default="")
    status = Column(String(80), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    aspect_ratio = Column(String(20), default="16:9")
    duration_goal = Column(Integer, default=60)


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(255), default="")
    visual_style = Column(String(80), default="Stickman")
    palette = Column(Text, default="[]")
    description = Column(Text, default="")
    expressions = Column(Text, default="[]")
    poses = Column(Text, default="[]")
    voice_profile = Column(String(255), default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    title = Column(String(255), nullable=False)
    narration = Column(Text, default="")
    visual_description = Column(Text, default="")
    prompt = Column(Text, default="")
    character_ids = Column(Text, default="[]")
    camera = Column(String(255), default="wide shot")
    background = Column(String(255), default="")
    duration = Column(Integer, default=10)
    order_index = Column(Integer, default=0)
    status = Column(String(80), default="planned")
    subtitle_text = Column(Text, default="")
    generated_asset = Column(String(255), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def set_character_ids(self, values: List[int]) -> None:
        self.character_ids = json.dumps(values)

    def get_character_ids(self) -> List[int]:
        try:
            return json.loads(self.character_ids or "[]")
        except Exception:
            return []


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    name = Column(String(255), nullable=False)
    kind = Column(String(80), nullable=False)
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(120), default="application/octet-stream")
    size_bytes = Column(Integer, default=0)
    source = Column(String(255), default="upload")
    license = Column(String(255), default="project-managed")
    created_at = Column(DateTime, default=datetime.utcnow)


class RenderJob(Base):
    __tablename__ = "render_jobs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    status = Column(String(80), default="queued")
    progress = Column(Integer, default=0)
    output_path = Column(String(500), default="")
    error_message = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class ProviderConfig(Base):
    __tablename__ = "provider_configs"

    id = Column(Integer, primary_key=True, index=True)
    provider_name = Column(String(120), nullable=False, unique=True)
    api_key = Column(String(255), default="")
    model_name = Column(String(255), default="")
    enabled = Column(Boolean, default=False)
    config_json = Column(Text, default="{}")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
