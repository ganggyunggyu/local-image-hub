"""mono_halftone 바니걸 특화 배치"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_mono_halftone"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {
        "prompt": "1girl, white hair, bunny ears, black bunny suit, bow tie, arms up, smirk, upper body, looking at viewer, wink",
        "alias": "bunny_wink",
    },
    {
        "prompt": "1girl, blonde hair, bunny ears, black bunny suit, fishnet stockings, leaning forward, playful smile, close-up face",
        "alias": "bunny_blonde_lean",
    },
    {
        "prompt": "1girl, black hair, ponytail, bunny ears, white bunny suit, sitting cross legged, chin on hand, bored expression",
        "alias": "bunny_white_bored",
    },
    {
        "prompt": "1girl, silver hair, long hair, bunny ears, black bunny suit, holding tray with drinks, elegant pose, looking at viewer",
        "alias": "bunny_tray_elegant",
    },
    {
        "prompt": "1girl, red hair, twin tails, bunny ears, black bunny suit, peace sign, cheerful, upper body, energetic",
        "alias": "bunny_red_peace",
    },
    {
        "prompt": "1girl, pink hair, short hair, bunny ears, black bunny suit, arms behind back, shy smile, looking away, cute",
        "alias": "bunny_pink_shy",
    },
    {
        "prompt": "1girl, purple hair, long hair, bunny ears, black bunny suit, lying on side, propping head up, seductive, looking at viewer",
        "alias": "bunny_purple_lying",
    },
    {
        "prompt": "1girl, white hair, bunny ears, black bunny suit, back view, looking over shoulder, hair flowing, dramatic lighting",
        "alias": "bunny_back_view",
    },
    {
        "prompt": "1girl, blue hair, messy hair, bunny ears, black bunny suit, stretching arms above head, yawning, sleepy, cute",
        "alias": "bunny_blue_sleepy",
    },
    {
        "prompt": "1girl, black hair, hime cut, bunny ears, black bunny suit, fan covering mouth, mysterious, elegant, japanese style",
        "alias": "bunny_hime_fan",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "",
        "width": 832,
        "height": 1216,
        "model": "animagine-xl-4",
        "style": "mono_halftone",
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
    print(f"mono_halftone 바니걸 배치 {TOTAL}장")
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
