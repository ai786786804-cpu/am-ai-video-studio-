from __future__ import annotations

import re
from typing import Dict, List


def build_scene_breakdown(script: str, style: str) -> List[Dict[str, str | int | list[int]]]:
    if not script or not script.strip():
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", script.strip()) if p.strip()]
    if not paragraphs:
        paragraphs = [script.strip()]

    scenes: List[Dict[str, str | int | list[int]]] = []
    for idx, paragraph in enumerate(paragraphs, start=1):
        clean_paragraph = " ".join(re.split(r"\s+", paragraph))
        narration = clean_paragraph[:220]
        scenes.append(
            {
                "title": f"Scene {idx}",
                "narration": narration,
                "visual_description": f"{style} scene set in a cinematic environment, matching the story beat and mood.",
                "prompt": f"{style} cinematic storyboard scene with consistent characters, script-aligned composition, warm lighting, and emotional storytelling.",
                "background": "Script-informed environment and historical or modern setting.",
                "camera": "wide establishing shot with subtle motion",
                "duration": max(6, min(18, len(clean_paragraph.split()) // 4 + 8)),
                "subtitle_text": narration[:160],
                "character_ids": [],
                "status": "planned",
            }
        )
    return scenes
