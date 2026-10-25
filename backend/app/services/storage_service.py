from __future__ import annotations

import shutil
from pathlib import Path
import subprocess

from app.database import SessionLocal
from app.models import Project, Scene


def ensure_storage_dirs() -> Path:
    root = Path(__file__).resolve().parents[1] / "data"
    root.mkdir(exist_ok=True)
    (root / "uploads").mkdir(exist_ok=True)
    (root / "renders").mkdir(exist_ok=True)
    return root


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def build_project_render(project_id: int) -> str:
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")

        scenes = db.query(Scene).filter(Scene.project_id == project_id).order_by(Scene.order_index.asc()).all()
        if not scenes:
            raise ValueError("Project has no scenes to render.")

        storage = ensure_storage_dirs()
        output = storage / "renders" / f"project_{project_id}_final.mp4"
        scene_assets = [scene.generated_asset for scene in scenes if scene.generated_asset]
        if not scene_assets:
            raise ValueError("No valid scene assets available for render.")

        concat_file = storage / "renders" / f"project_{project_id}_concat.txt"
        text_lines = []
        for index, asset_path in enumerate(scene_assets):
            clean = asset_path.replace("\\", "/").replace("'", "\\'")
            text_lines.append(f"file '{clean}'")
            text_lines.append(f"duration {max(3, scenes[index].duration if index < len(scenes) else 3)}")
        concat_file.write_text("\n".join(text_lines), encoding="utf-8")

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-vf",
                "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-movflags",
                "+faststart",
                str(output),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        return str(output)
    finally:
        db.close()
