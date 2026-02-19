"""guidance_scale 비교 테스트"""
import asyncio
import httpx
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "guidance_compare"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_PROMPT = "1girl, frieren, sousou no frieren, white hair, elf ears, classroom, sitting at desk, sunset light through window, peaceful, masterpiece, gouache texture, traditional media, bold ink strokes, watercolor wash, paper texture"

SCALES = [3.0, 4.0, 5.0, 5.5, 6.0, 7.0]

async def generate(client, scale, seed):
    payload = {
        "prompt": BASE_PROMPT,
        "negative_prompt": "low quality, worst quality, digital, glossy",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "guidance_scale": scale,
        "seed": seed,  # 동일 시드로 비교
        "provider": "nai",
        "model": "nai-v4.5-full",
        "save_to_disk": False,
    }

    r = await client.post(API_URL, json=payload, timeout=180.0)
    data = r.json()
    if data.get("success") and data.get("image_base64"):
        fp = OUTPUT_DIR / f"cfg_{scale}_{seed}.webp"
        fp.write_bytes(b64decode(data["image_base64"]))
        print(f"OK cfg={scale}")
    else:
        print(f"FAIL cfg={scale}")

async def main():
    import random
    seed = random.randint(0, 2147483647)

    print(f"guidance_scale 비교 (동일 시드: {seed})")
    print(f"테스트: {SCALES}")
    print("=" * 40)

    async with httpx.AsyncClient() as client:
        for scale in SCALES:
            await generate(client, scale, seed)
            await asyncio.sleep(0.3)

    print("=" * 40)
    print(f"저장: {OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
