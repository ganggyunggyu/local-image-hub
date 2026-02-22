"""센조가하라 히타기 - 28스텝 vs 32스텝 비교 (동일 시드)"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_senjougahara_steps_compare"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHAR = "1girl, senjougahara hitagi, long purple hair, sharp eyes, cold beauty, slender, school uniform"

POSES = [
    "head tilt, looking at viewer, mysterious smile, upper body",
    "arms crossed, tsundere, looking away, blushing slightly",
    "profile view, moonlight, elegant, dramatic",
    "close up face, sharp gaze, beautiful, detailed eyes",
    "sitting on bench, legs crossed, elegant, reading",
    "standing in rain, wet hair, emotional, dramatic",
    "rooftop, sky, hair blowing, wind, contemplative",
    "cafe, drinking coffee, mature, elegant, afternoon",
    "night sky, stars, beautiful, atmospheric",
    "stapler in hand, threatening, smirk, playful, close up",
]

random.seed(2024)
SEEDS = [random.randint(1, 2**31) for _ in range(10)]

JOBS = []

for i, (pose, seed) in enumerate(zip(POSES, SEEDS)):
    JOBS.append({
        "pose": pose,
        "steps": 28,
        "seed": seed,
        "name": f"{i:02d}_28steps",
    })
    JOBS.append({
        "pose": pose,
        "steps": 32,
        "seed": seed,
        "name": f"{i:02d}_32steps",
    })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{CHAR}, {job['pose']}, masterpiece, best quality",
        "negative_prompt": "low quality, worst quality, bad anatomy, bad hands",
        "width": 832,
        "height": 1216,
        "steps": job["steps"],
        "seed": job["seed"],
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
            fp = OUTPUT_DIR / f"{job['name']}_seed{job['seed']}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{num:02d}/{TOTAL}] OK {job['name']} (seed: {job['seed']})")
            return True
        else:
            print(f"[{num:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:60]}")
            return False
    except Exception as e:
        print(f"[{num:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"센조가하라 28 vs 32 스텝 비교 - {TOTAL}장 (10포즈 × 2스텝)")
    print(f"동일 시드로 비교: 파일명 정렬하면 28/32 나란히 비교 가능")
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
