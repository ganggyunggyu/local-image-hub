"""
Z-Image Turbo - 스피츠(Japanese Spitz) 다양한 포즈
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_zimage_spitz"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {"prompt": "japanese spitz puppy running on grass, sunny, action shot", "alias": "spitz_run"},
    {"prompt": "japanese spitz sitting, fluffy white fur, studio portrait", "alias": "spitz_portrait"},
    {"prompt": "japanese spitz playing in snow, winter, joyful", "alias": "spitz_snow"},
    {"prompt": "japanese spitz sleeping curled up, cozy blanket, warm light", "alias": "spitz_sleep"},
    {"prompt": "japanese spitz tilting head, curious expression, close-up", "alias": "spitz_tilt"},
    {"prompt": "japanese spitz with tongue out, smiling, park, bright day", "alias": "spitz_smile"},
    {"prompt": "japanese spitz puppy with ball, playful, garden", "alias": "spitz_ball"},
    {"prompt": "japanese spitz on beach, waves, golden hour", "alias": "spitz_beach"},
    {"prompt": "japanese spitz looking out window, rain outside, moody", "alias": "spitz_window"},
    {"prompt": "japanese spitz jumping, low angle, blue sky, dynamic", "alias": "spitz_jump"},
    {"prompt": "japanese spitz in autumn leaves, warm colors, bokeh", "alias": "spitz_autumn"},
    {"prompt": "japanese spitz puppy and flower, spring, soft light", "alias": "spitz_flower"},
    {"prompt": "two japanese spitz puppies playing together, indoor, cute", "alias": "spitz_duo"},
    {"prompt": "japanese spitz walking on forest trail, morning mist", "alias": "spitz_forest"},
    {"prompt": "japanese spitz close-up face, big dark eyes, fluffy, adorable", "alias": "spitz_face"},
    {"prompt": "japanese spitz in cafe, sitting on chair, urban, cozy", "alias": "spitz_cafe"},
    {"prompt": "japanese spitz shaking off water, splash, backlit, fun", "alias": "spitz_shake"},
    {"prompt": "japanese spitz puppy being held, hands, heartwarming", "alias": "spitz_held"},
    {"prompt": "japanese spitz yawning, close-up, funny, cozy indoor", "alias": "spitz_yawn"},
    {"prompt": "japanese spitz standing proud, wind blowing fur, majestic", "alias": "spitz_majestic"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{job['prompt']}, photorealistic, high quality",
        "negative_prompt": "cartoon, anime, ugly, blurry, deformed",
        "width": 1024,
        "height": 1024,
        "steps": 8,
        "guidance_scale": 0.0,
        "model": "z-image-turbo",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"Z-Image Turbo 스피츠 배치 {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
