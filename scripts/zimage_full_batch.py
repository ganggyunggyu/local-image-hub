"""
Z-Image 풀 모델 다양한 이미지 배치
한 장당 ~50분 소요, CPU offload + float32
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_zimage_full"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {
        "prompt": "portrait of a young woman in a cozy cafe, natural window light, warm tones, shallow depth of field, film photography",
        "alias": "cafe_portrait",
    },
    {
        "prompt": "white japanese spitz puppy playing in autumn leaves, golden hour backlight, bokeh, joyful expression",
        "alias": "spitz_autumn",
    },
    {
        "prompt": "aerial view of tokyo city at night, neon lights reflecting on wet streets, cyberpunk atmosphere, ultra detailed",
        "alias": "tokyo_night",
    },
    {
        "prompt": "fresh sushi platter on dark slate, close-up food photography, dramatic side lighting, water droplets on fish",
        "alias": "sushi_closeup",
    },
    {
        "prompt": "old european alley in morning fog, cobblestone street, vintage street lamps, cinematic mood, soft diffused light",
        "alias": "euro_alley",
    },
    {
        "prompt": "macro shot of a blue morpho butterfly on a flower, iridescent wings, dew drops, shallow focus, nature photography",
        "alias": "butterfly_macro",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{job['prompt']}, photorealistic, high quality, 8k",
        "negative_prompt": "cartoon, anime, ugly, blurry, deformed, watermark, text",
        "width": 1024,
        "height": 1024,
        "steps": 50,
        "guidance_scale": 4.0,
        "model": "z-image",
        "save_to_disk": False,
    }

    try:
        print(f"[{idx}/{TOTAL}] 생성 시작: {job['alias']}", flush=True)
        r = await client.post(API_URL, json=payload, timeout=3600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            img_bytes = b64decode(data["image_base64"])
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(img_bytes)
            fsize = len(img_bytes)
            print(f"[{idx}/{TOTAL}] OK {job['alias']} (seed: {seed}, {fsize:,} bytes)", flush=True)
            return True
        else:
            print(f"[{idx}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print(f"Z-Image 풀 모델 배치 {TOTAL}장 (한 장당 ~50분)", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)
    print("=" * 60, flush=True)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1

    print("=" * 60, flush=True)
    print(f"완료! 성공: {ok}, 실패: {fail}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
