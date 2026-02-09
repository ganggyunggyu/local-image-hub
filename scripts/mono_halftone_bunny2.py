"""mono_halftone 바니걸 추가 배치"""

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
        "prompt": "1girl, white hair, side ponytail, bunny ears, black bunny suit, sitting on bar stool, legs crossed, cocktail glass, smirk",
        "alias": "bunny2_bar_stool",
    },
    {
        "prompt": "1girl, green hair, short hair, bunny ears, black bunny suit, boxing pose, fists up, fierce expression, upper body",
        "alias": "bunny2_fighter",
    },
    {
        "prompt": "1girl, silver hair, braids, bunny ears, black bunny suit, reading book, glasses, intellectual, sitting",
        "alias": "bunny2_bookworm",
    },
    {
        "prompt": "1girl, orange hair, wavy hair, bunny ears, black bunny suit, blowing kiss, heart, wink, close-up face, flirty",
        "alias": "bunny2_kiss",
    },
    {
        "prompt": "1girl, dark blue hair, long hair, bunny ears, black bunny suit, leaning on railing, night city, wind, hair flowing, cool",
        "alias": "bunny2_night_city",
    },
    {
        "prompt": "1girl, white hair, twin tails, bunny ears, black bunny suit, tongue out, peace sign near eye, playful, upper body",
        "alias": "bunny2_twin_peace",
    },
    {
        "prompt": "1girl, ash blonde hair, messy bun, bunny ears, black bunny suit, cigarette, tired eyes, leaning on wall, noir",
        "alias": "bunny2_noir_smoke",
    },
    {
        "prompt": "1girl, lavender hair, long hair, bunny ears, white bunny suit, dancing pose, graceful, spotlight, stage",
        "alias": "bunny2_dancer",
    },
    {
        "prompt": "1girl, red hair, short bob, bunny ears, black bunny suit, finger to lips, shh pose, mischievous smile, close-up",
        "alias": "bunny2_shh",
    },
    {
        "prompt": "1girl, black hair, straight long hair, bunny ears, black bunny suit, katana, samurai pose, intense eyes, wind",
        "alias": "bunny2_samurai",
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
    print(f"mono_halftone 바니걸 추가 배치 {TOTAL}장")
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
