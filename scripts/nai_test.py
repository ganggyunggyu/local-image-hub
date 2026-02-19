"""NovelAI API 테스트"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_nai_test"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {
        "prompt": "1girl, white hair, bunny ears, black bunny suit, bow tie, arms up, smirk, upper body, looking at viewer, masterpiece, best quality",
        "alias": "nai_bunny",
        "model": "nai-v3",
    },
    {
        "prompt": "1girl, frieren, sousou no frieren, white hair, long hair, elf ears, green eyes, mage robe, flower meadow, wind, masterpiece, best quality",
        "alias": "nai_frieren",
        "model": "nai-v3",
    },
    {
        "prompt": "1boy, blue hair, short hair, blue eyes, hero armor, cape, confident smile, sky background, upper body, masterpiece, best quality",
        "alias": "nai_hero",
        "model": "nai-v3",
    },
    {
        "prompt": "1girl, silver hair, red eyes, maid outfit, holding tray, elegant, looking at viewer, indoor, masterpiece, best quality",
        "alias": "nai_maid",
        "model": "nai-v3",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality",
        "width": 832,
        "height": 1216,
        "steps": 28,
        "guidance_scale": 5.0,
        "provider": "nai",
        "model": job["model"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
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
    print(f"NovelAI API 테스트 {TOTAL}장")
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
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
