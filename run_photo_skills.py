#!/usr/bin/env python3
"""Orchestrate 7 photo-space skills on a single source image using local gpt_image_2.py."""
import os
import subprocess
import sys
from pathlib import Path

SRC_IMG = Path("C:/Users/ilost/Desktop/照片/list/20230705203743.jpg")
RESULTS = Path("C:/Users/ilost/Desktop/照片/list/results")
PROMPTS = RESULTS / "prompts"
GPT_IMG = Path("C:/Users/ilost/.workbuddy/scripts/gpt_image_2.py")
PYTHON = Path("C:/Users/ilost/.workbuddy/binaries/python/versions/3.13.12/python.exe")

SKILLS = [
    {
        "id": "01_photo-abstract-editorial",
        "name": "photo-abstract-editorial",
        "github": "ZzzLc0405/photo-abstract-editorial",
        "mode": "gen",
        "size": "1024x1536",
        "prompt": (
            "An ivory-cream editorial abstract panel inspired by the spatial rhythm of a modern glass tower plaza. "
            "Minimalist geometric composition, soft cobalt-blue glass reflections fragmented into translucent rectangular blocks, "
            "subtle terracotta vertical accents, pale warm background, architectural abstraction, high-end magazine print aesthetic, "
            "clean negative space, calm sophisticated mood."
        ),
    },
    {
        "id": "02_compose-photo-memory-archive",
        "name": "Compose Photo Memory Archive",
        "github": "sbj61188-lab/compose-photo-memory-archive",
        "mode": "edit",
        "size": "1024x1536",
        "prompt": (
            "Transform the reference city-plaza photo into a dreamy watercolor memory field. "
            "The cobalt glass towers dissolve into fluid blue washes, rust-orange structural beams become soft ochre streaks, "
            "green tree canopy at the bottom bleeds upward into the architecture, nostalgic atmosphere, wet-on-wet technique, "
            "muted palette with occasional bright accents, no text, no realistic detail, pure painterly memory."
        ),
    },
    {
        "id": "03_scene-distillation-zine",
        "name": "Scene Distillation Zine v1.3",
        "github": "Zeejay0/gathered-scenes-zine-skill",
        "mode": "gen",
        "size": "1024x1536",
        "prompt": (
            "A distilled risograph-style zine illustration of a contemporary urban plaza. "
            "Tall glass tower rendered as bold flat color blocks of sky blue and terracotta, minimal green tree silhouettes at the base, "
            "zine print texture, graphic poster composition, clean vector-like lines, contemporary Chinese city mood, "
            "limited palette, no photographic realism."
        ),
    },
    {
        "id": "04_gathered-scenes-zine",
        "name": "Gathered Scenes Zine v1.3",
        "github": "Zeejay0/gathered-scenes-zine-skill",
        "mode": "gen",
        "size": "1024x1536",
        "prompt": (
            "A torn-paper collage illustration of a modern city plaza scene. "
            "Layered matte paper cutouts of blue glass curtain wall and red structural tower, rough deckled edges, "
            "muted editorial palette of powder blue, rust, and cream, zine art, tactile paper texture, "
            "fragmented architectural view, handcrafted feel, no text."
        ),
    },
    {
        "id": "05_gc-minimal-zine-poster",
        "name": "gc-minimal-zine-poster",
        "github": "LiamGvchi/gc-minimal-zine-poster",
        "mode": "gen",
        "size": "1024x1536",
        "prompt": (
            "A minimal zine poster abstracting a modern tower plaza. "
            "Large bold geometric shapes in powder blue, rust orange, and off-white, clean Swiss typography layout with empty headline space, "
            "contemporary minimal zine aesthetic, poetic and airy, no realistic rendering, graphic composition, print-ready."
        ),
    },
    {
        "id": "06_8bit-pixel-fusion",
        "name": "8bit-pixel-fusion",
        "github": "TwentyfiveBTea/8bit-pixel-art",
        "mode": "gen",
        "size": "1024x1536",
        "prompt": (
            "A sparse 8-bit pixel art abstraction of a modern glass tower complex. "
            "Limited 8-color palette, blocky blue glass facade, red tower accent, tiny green tree sprites at the bottom, "
            "retro game aesthetic, clean pixel grid, minimalist editorial composition, no text, no dithering."
        ),
    },
    {
        "id": "07_photo-ink-echo",
        "name": "Photo Ink Echo",
        "github": "zhouaria28-cloud/photo-ink-echo",
        "mode": "gen",
        "size": "1024x1536",
        "prompt": (
            "A Chinese ink-wash watercolor memory motif panel inspired by a modern office plaza. "
            "Flowing blue ink gradations form tower silhouettes, warm orange ink accents suggest structural lines, "
            "misty green foliage at the bottom, rice-paper texture, poetic Chinese brush painting mood, "
            "serene and atmospheric, no text, no photorealism."
        ),
    },
]


def run_skill(skill: dict) -> dict:
    out_path = RESULTS / f"{skill['id']}.png"
    prompt_path = PROMPTS / f"{skill['id']}.txt"
    prompt_path.write_text(skill["prompt"], encoding="utf-8")

    cmd = [str(PYTHON), str(GPT_IMG), skill["mode"], skill["prompt"], "-s", skill["size"], "-o", str(out_path)]
    if skill["mode"] == "edit":
        cmd += ["-i", str(SRC_IMG)]

    print(f"\n>>> [{skill['id']}] {skill['name']}")
    print(" ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    success = proc.returncode == 0 and out_path.exists() and out_path.stat().st_size > 1000
    return {
        "id": skill["id"],
        "name": skill["name"],
        "success": success,
        "out": str(out_path),
        "returncode": proc.returncode,
        "stderr_tail": stderr[-500:] if stderr else "",
    }


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    PROMPTS.mkdir(parents=True, exist_ok=True)

    if not SRC_IMG.exists():
        print(f"Source image not found: {SRC_IMG}", file=sys.stderr)
        sys.exit(1)

    report = []
    for skill in SKILLS:
        report.append(run_skill(skill))

    print("\n\n=== GENERATION REPORT ===")
    for r in report:
        status = "OK" if r["success"] else "FAIL"
        print(f"{status}  {r['id']}  {r['name']}")
        if not r["success"]:
            print(f"       rc={r['returncode']}  {r['stderr_tail']}")

    failures = [r for r in report if not r["success"]]
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
