"""페른 (장송의 프리렌) 아쿠아 5장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_fern_aqua"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 페른: 보라색 긴 머리, 트윈테일, 보라색 눈, 마법사 로브
FERN = "fern, sousou no frieren, purple hair, long hair, twintails, purple eyes, mage robe"
NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    {"prompt": f"1girl, {FERN}, staff, magic, casting spell, forest, mystical", "alias": "fern_01"},
    {"prompt": f"1girl, {FERN}, reading book, library, quiet, focused", "alias": "fern_02"},
    {"prompt": f"1girl, {FERN}, concerned expression, worried, upper body, portrait", "alias": "fern_03"},
    {"prompt": f"1girl, {FERN}, sunset, meadow, wind, hair flowing, peaceful", "alias": "fern_04"},
    {"prompt": f"1girl, {FERN}, slight smile, rare smile, happy, gentle, portrait", "alias": "fern_05"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 1024,
        "height": 1024,
        "model": "animagine-xl-4",
        "style": "pale_aqua",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print("페른 (장송의 프리렌) 아쿠아 5장 (1024x1024)", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)
    print("=" * 60, flush=True)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60, flush=True)
    print(f"완료! 성공: {ok}, 실패: {fail}", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
