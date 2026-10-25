from __future__ import annotations

import re
from typing import Dict, List


def build_scene_breakdown(script: str, style: str) -> List[Dict[str, str | int | list[int]]]:
    clean = script.strip()
    if not clean:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", clean) if p.strip()]
    if not paragraphs:
        paragraphs = [clean]

    scenes: List[Dict[str, str | int | list[int]]] = []
    for idx, paragraph in enumerate(paragraphs, start=1):
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        narration = " ".join(s.strip() for s in sentences if s.strip())
        if not narration:
            continue
        scenes.append(
            {
                "title": f"Scene {idx}",
                "narration": narration[:180],
                "visual_description": f"{style}-style visual treatment for the story beat: {narration[:120]}",
                "prompt": f"{style} cinematic storyboard scene, script aligned, emotional visual storytelling, consistent characters, warm cinematic composition",
                "background": "location-based setting informed by the script",
                "camera": "tracked wide shot with subtle motion",
                "duration": max(6, min(18, len(narration.split()) // 4 + 6)),
                "subtitle_text": narration[:160],
                "character_ids": [],
                "status": "planned",
            }
        )
    return scenes


def format_scene_title(script_excerpt: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", script_excerpt)
    if not words:
        return "Untitled Scene"
    title = " ".join(words[:5])
    return title.title()
