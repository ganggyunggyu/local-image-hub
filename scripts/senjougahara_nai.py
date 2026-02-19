"""센조가하라 히타기 장발/단발 100장 - NAI × monogatari 프리셋"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_senjougahara_nai"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LONG = "1girl, senjougahara hitagi, long purple hair, sharp eyes, cold beauty, slender"
SHORT = "1girl, senjougahara hitagi, short purple hair, sharp eyes, cold beauty, slender"

POSES = [
    "head tilt, looking at viewer, stapler in hand, threatening, upper body",
    "head tilt, mysterious smile, school uniform, wind",
    "arms crossed, tsundere, looking away, blushing slightly",
    "sitting on bench, legs crossed, elegant, reading",
    "school uniform, rooftop, sky, hair blowing",
    "casual clothes, relaxed, gentle rare smile, soft lighting",
    "profile view, moonlight, elegant, dramatic",
    "walking, back view, lonely atmosphere, autumn",
    "close up face, sharp gaze, beautiful, detailed eyes",
    "leaning on desk, bored, classroom, afternoon sun",
    "standing in rain, wet hair, emotional, dramatic",
    "white dress, summer, sunlight, peaceful smile",
    "night sky, stars, contemplative, beautiful",
    "cafe, drinking coffee, mature, elegant",
    "lying down, looking up, soft expression, intimate",
    "sitting on stairs, knees up, melancholic, golden hour",
    "running, dynamic, hair flowing, school bag",
    "standing under tree, dappled sunlight, serene",
    "holding phone, looking away, modern, casual outfit",
    "winter coat, scarf, cold breath, snowy street",
    "side glance, smirk, confident, close up",
    "stretching, morning, bedroom, sleepy, natural",
    "hands behind back, looking at sky, wistful",
    "leaning on railing, bridge, river, sunset",
    "reading book, library, quiet, focused",
]

JOBS = []
idx = 0

for hair_label, tags in [("long", LONG), ("short", SHORT)]:
    for pose in POSES:
        JOBS.append({
            "tags": tags,
            "pose": pose,
            "name": f"{idx:03d}_{hair_label}",
        })
        idx += 1
        for _ in range(1):
            JOBS.append({
                "tags": tags,
                "pose": pose,
                "name": f"{idx:03d}_{hair_label}",
            })
            idx += 1
            if idx >= 100:
                break
        if idx >= 100 and hair_label == "short":
            break
    if hair_label == "long" and idx >= 50:
        idx = 50

JOBS = JOBS[:100]
TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['tags']}, {job['pose']}, masterpiece, best quality",
        "negative_prompt": "low quality, worst quality, bad anatomy, bad hands",
        "width": 832,
        "height": 1216,
        "provider": "nai",
        "model": "nai-diffusion-4-curated-preview",
        "style": "monogatari",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=120.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{num:03d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{num:03d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:60]}")
            return False
    except Exception as e:
        print(f"[{num:03d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"센조가하라 히타기 × monogatari 프리셋 - NAI {TOTAL}장")
    print(f"  장발: 50장 / 단발: 50장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(1.0)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
