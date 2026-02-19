"""봇치더락 PA상 배치 50장

PA상(=pa-san) 솔로 위주로 50장 생성함냥
pale_aqua 25장 + watercolor_sketch 25장 구성임냥
"""

import asyncio
from base64 import b64decode
from datetime import datetime
from pathlib import Path

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_bocchi_pa_san_50"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PA = "pa-san, bocchi the rock!, black hair, green eyes, labret piercing, ear piercing"
NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

SCENES: list[str] = [
    "headphones, mixing console, studio, focused",
    "arms crossed, live house, backstage, cool",
    "coffee, cafe, reading, quiet",
    "goth fashion, black dress, choker, standing",
    "night, street, city lights, cool expression",
    "headphones around neck, smiling, casual",
    "sitting, bench, park, relaxed",
    "looking at viewer, close up, portrait",
    "side profile, wind, hair flowing",
    "night club, neon lights, cool",
    "holding phone, texting, train station",
    "leaning on wall, alley, night",
    "listening to music, eyes closed, peaceful",
    "black cardigan, grey dress, standing",
    "rooftop, sunset, looking away",
    "bar counter, drink, relaxed",
    "concert hall, spotlight, stage",
    "rainy day, umbrella, street",
    "record store, browsing, vinyl",
    "studio booth, microphone, working",
    "soundcheck, venue stage, cables, focused",
    "venue entrance, ticket booth, night",
    "laptop, audio editing, dim light",
    "carrying equipment cases, backstage corridor",
    "quiet break, sitting on stairs, moody",
]

STYLES: list[str] = ["pale_aqua", "watercolor_sketch"]

JOBS: list[dict] = []
idx = 1
for style in STYLES:
    for scene in SCENES:
        JOBS.append(
            {
                "prompt": f"1girl, {PA}, {scene}",
                "alias": f"pa{idx:03d}",
                "style": style,
            }
        )
        idx += 1

TOTAL = len(JOBS)


async def generate(client, job_idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 832,
        "height": 1216,
        "model": "animagine-xl-4",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{job['style']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(
                f"[{job_idx:02d}/{TOTAL}] OK {job['alias']} [{job['style']}] (seed: {seed})",
                flush=True,
            )
            return True

        print(
            f"[{job_idx:02d}/{TOTAL}] FAIL {job['alias']} [{job['style']}]: {data.get('error', '?')}",
            flush=True,
        )
        return False
    except Exception as e:
        print(
            f"[{job_idx:02d}/{TOTAL}] ERROR {job['alias']} [{job['style']}]: {e}",
            flush=True,
        )
        return False


async def main():
    ok = fail = 0
    print("봇치더락 PA상 배치 50장", flush=True)
    print("pale_aqua 25장 + watercolor_sketch 25장", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)
    print("=" * 60, flush=True)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60, flush=True)
    print(f"완료! 성공: {ok}, 실패: {fail}", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
