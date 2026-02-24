"""마요이 × 필름카메라 감성 - animagine-xl-4 로컬 10장"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_mayoi_film_animagine"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAYOI = "1girl, hachikuji mayoi, long black hair, twin tails, red eyes"
FILM = "film grain, analog photo, 35mm film, soft focus, light leak, warm tones, vintage, nostalgic, natural lighting"

SCENES = [
    "sitting by window, afternoon sun, curtain blowing, golden hour, cafe, coffee cup",
    "walking down street, sunset, long shadows, power lines, residential area, summer evening",
    "standing at train platform, waiting, wind, hair blowing, cloudy day, melancholic",
    "reading book under tree, shade, summer, peaceful, gentle breeze",
    "looking out bus window, rainy day, condensation on glass, reflection, pensive",
    "buying drink from vending machine, night, soft glow, quiet street, alone",
    "eating ice cream, summer festival, yukata, lanterns, warm evening light",
    "holding sparkler, summer night, face lit by warm glow, close up",
    "umbrella, cherry blossom petals falling, spring rain, gentle smile",
    "bicycle, riding through rice fields, countryside, summer clouds, freedom",
]

random.seed(777)

JOBS = []
for i, scene in enumerate(SCENES):
    JOBS.append({
        "prompt": f"{MAYOI}, {scene}, {FILM}",
        "name": f"mayoi_{i:02d}",
    })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece, best quality",
        "negative_prompt": "low quality, worst quality, bad anatomy, blurry, oversaturated, neon, vibrant, text, watermark, digital art",
        "width": 832,
        "height": 1216,
        "provider": "local",
        "model": "animagine-xl-4",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=300.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{num:02d}/{TOTAL}] OK {job['name']} (seed: {seed})")
            return True
        else:
            print(f"[{num:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:80]}")
            return False
    except Exception as e:
        print(f"[{num:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"마요이 × 필름카메라 감성 - animagine-xl-4 {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.5)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
