from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1)
    style: str = "Stickman"
    description: str = ""
    duration_goal: int = 60
    aspect_ratio: str = "16:9"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    style: Optional[str] = None
    description: Optional[str] = None
    script: Optional[str] = None
    status: Optional[str] = None
    duration_goal: Optional[int] = None
    aspect_ratio: Optional[str] = None


class ScenePayload(BaseModel):
    title: str
    narration: str = ""
    visual_description: str = ""
    prompt: str = ""
    background: str = ""
    camera: str = "wide shot"
    duration: int = 10
    subtitle_text: str = ""
    status: str = "planned"
    character_ids: List[int] = []


class AssetUploadResponse(BaseModel):
    id: int
    name: str
    kind: str
    file_path: str


class RenderJobCreate(BaseModel):
    project_id: int


class ProviderConfigPayload(BaseModel):
    provider_name: str
    api_key: str = ""
    model_name: str = ""
    enabled: bool = False
    config_json: Dict[str, Any] = Field(default_factory=dict)
