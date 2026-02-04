"""
Z-Image Turbo - 다양한 강아지 품종 + 포즈 테스트
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_zimage_dogs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {"prompt": "dachshund puppy running in a park, action shot, sunny day", "alias": "dachshund_run"},
    {"prompt": "dachshund sleeping on a blanket, cozy, warm light, close-up", "alias": "dachshund_sleep"},
    {"prompt": "golden retriever puppy playing fetch, beach, golden hour", "alias": "golden_fetch"},
    {"prompt": "golden retriever sitting in autumn leaves, portrait, bokeh", "alias": "golden_autumn"},
    {"prompt": "shiba inu tilting head, curious expression, studio lighting", "alias": "shiba_tilt"},
    {"prompt": "shiba inu in snow, winter, playful, action shot", "alias": "shiba_snow"},
    {"prompt": "corgi puppy running toward camera, grass field, low angle", "alias": "corgi_run"},
    {"prompt": "corgi lying on back, belly up, cute, indoor, wooden floor", "alias": "corgi_belly"},
    {"prompt": "pomeranian with bow tie, portrait, studio, fluffy", "alias": "pom_portrait"},
    {"prompt": "pomeranian jumping, park, joyful, motion blur background", "alias": "pom_jump"},
    {"prompt": "french bulldog in cafe, sitting on chair, urban, warm light", "alias": "frenchie_cafe"},
    {"prompt": "french bulldog yawning, close-up, funny expression, cozy", "alias": "frenchie_yawn"},
    {"prompt": "husky howling, snow mountain, dramatic sky, cinematic", "alias": "husky_howl"},
    {"prompt": "husky puppy with blue eyes, portrait, soft lighting", "alias": "husky_portrait"},
    {"prompt": "beagle sniffing flowers, garden, spring, colorful", "alias": "beagle_flowers"},
    {"prompt": "samoyed smiling, fluffy white fur, outdoor, bright day", "alias": "samoyed_smile"},
    {"prompt": "border collie catching frisbee, action, blue sky", "alias": "collie_frisbee"},
    {"prompt": "poodle with stylish haircut, elegant pose, studio", "alias": "poodle_elegant"},
    {"prompt": "labrador puppy in rain puddle, splashing, playful", "alias": "lab_puddle"},
    {"prompt": "chihuahua in sweater, sitting on pillow, cute, indoor", "alias": "chihuahua_cozy"},
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
    print(f"Z-Image Turbo 강아지 배치 {TOTAL}장")
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
