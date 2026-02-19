"""냥냥돌쇠 히힛 한장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_hihit"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPT = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, mischievous smile, smug, playful grin, hand over mouth, giggling, teasing, looking at viewer, upper body, masterpiece"

async def main():
    payload = {
        "prompt": PROMPT,
        "negative_prompt": "low quality, worst quality",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": "monogatari",
        "save_to_disk": False,
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"dolsoe_hihit_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"OK! seed: {seed}")
            print(f"저장: {fp}")
        else:
            print(f"FAIL: {data.get('error', '?')}")

if __name__ == "__main__":
    asyncio.run(main())
