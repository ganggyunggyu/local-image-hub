"""cozy_gouache 테스트"""
import asyncio
import httpx
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "cozy_test"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    payload = {
        "prompt": "1girl, frieren, sousou no frieren, white hair, elf ears, classroom, sitting at desk, sunset light through window, peaceful, masterpiece",
        "negative_prompt": "low quality, worst quality",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": "cozy_gouache",
        "save_to_disk": False,
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"frieren_classroom_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"OK! {fp}")
        else:
            print(f"FAIL: {data.get('error')}")

if __name__ == "__main__":
    asyncio.run(main())
