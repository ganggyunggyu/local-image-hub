"""냥냥돌쇠 히힛 5장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_hihit"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, mischievous smile, smug, hand over mouth, giggling, looking at viewer, upper body", "style": "monogatari", "name": "hihit_mono"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, playful grin, teasing, wink, peace sign, upper body", "style": "pale_aqua", "name": "hihit_aqua"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, smug, confident smile, head tilt, sly, upper body", "style": "waterful", "name": "hihit_water"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, giggling, covering mouth, cute, mischievous, upper body", "style": "cozy_gouache", "name": "hihit_cozy"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, cheeky smile, tongue out slightly, playful, upper body", "style": "bold_pop", "name": "hihit_bold"},
]

TOTAL = len(JOBS)

async def generate(client, idx, job):
    payload = {
        "prompt": f"{job['prompt']}, masterpiece",
        "negative_prompt": "low quality, worst quality",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{idx}/{TOTAL}] FAIL: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx}/{TOTAL}] ERROR: {e}")
        return False

async def main():
    ok = 0
    print(f"냥냥돌쇠 히힛 {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 40)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            await asyncio.sleep(0.3)

    print("=" * 40)
    print(f"완료! 성공: {ok}/{TOTAL}")

if __name__ == "__main__":
    asyncio.run(main())
