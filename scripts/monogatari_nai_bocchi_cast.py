"""Bocchi the Rock cast batch using monogatari preset on NAI."""

import asyncio
from base64 import b64decode
from datetime import datetime
from pathlib import Path

import httpx

API_URL = "http://localhost:8002/api/generate"
TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_nai_bocchi_cast"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTERS = [
    {
        "alias": "bocchi",
        "tags": "1girl, gotoh hitori, bocchi the rock!, pink hair, blue eyes, shy, anxious, guitar",
    },
    {
        "alias": "nijika",
        "tags": "1girl, ijichi nijika, bocchi the rock!, blonde hair, ponytail, cheerful, drummer",
    },
    {
        "alias": "ryo",
        "tags": "1girl, yamada ryo, bocchi the rock!, blue hair, cool, stoic, bass guitar",
    },
    {
        "alias": "kita",
        "tags": "1girl, kita ikuyo, bocchi the rock!, red hair, bright smile, energetic, guitar",
    },
    {
        "alias": "kikuri",
        "tags": "1girl, hiroi kikuri, bocchi the rock!, purple hair, mature, drunk vibe, bass guitar",
    },
    {
        "alias": "pa_san",
        "tags": "1girl, pa-san, bocchi the rock!, black hair, green eyes, labret piercing, mature woman",
    },
    {
        "alias": "seika",
        "tags": "1girl, ijichi seika, bocchi the rock!, dark blue hair, tired eyes, manager, mature woman",
    },
    {
        "alias": "futari",
        "tags": "1girl, gotoh futari, bocchi the rock!, pink hair, playful, younger sister",
    },
]

SCENES = [
    "upper body, looking at viewer, cinematic lighting",
    "music studio, stage lights, dynamic angle",
]

NEGATIVE_PROMPT = "low quality, worst quality, bad anatomy, bad hands, extra fingers"


def build_jobs() -> list[dict]:
    jobs = []
    index = 1
    for character in CHARACTERS:
        for scene in SCENES:
            jobs.append(
                {
                    "index": index,
                    "alias": f"{character['alias']}_{index:02d}",
                    "prompt": f"{character['tags']}, {scene}, masterpiece, best quality",
                }
            )
            index += 1
    return jobs


async def generate_image(client: httpx.AsyncClient, job: dict, total: int) -> bool:
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEGATIVE_PROMPT,
        "width": 832,
        "height": 1216,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": "monogatari",
        "save_to_disk": False,
    }

    try:
        response = await client.post(API_URL, json=payload, timeout=180.0)
        data = response.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            output_path = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            output_path.write_bytes(b64decode(data["image_base64"]))
            print(f"[{job['index']:02d}/{total}] OK {job['alias']}")
            return True
        error = data.get("error", "unknown error")
        print(f"[{job['index']:02d}/{total}] FAIL {job['alias']}: {error}")
        return False
    except Exception as exc:
        print(f"[{job['index']:02d}/{total}] ERROR {job['alias']}: {exc}")
        return False


async def main() -> None:
    jobs = build_jobs()
    total = len(jobs)
    success_count = 0
    fail_count = 0

    print(f"monogatari + nai + bocchi cast batch ({total} images)")
    print(f"output: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for job in jobs:
            if await generate_image(client, job, total):
                success_count += 1
            else:
                fail_count += 1
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"done | success: {success_count}, fail: {fail_count}")


if __name__ == "__main__":
    asyncio.run(main())
