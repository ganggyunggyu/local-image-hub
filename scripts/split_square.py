"""스플릿 스케치 정사각형 테스트 (5장)
1024x1024 정사각형 포맷
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_split_square"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    {"prompt": "1girl, purple hair, large eyes, close up face, cute", "alias": "sq_01"},
    {"prompt": "1girl, pink hair, twintails, large eyes, close up face, smile", "alias": "sq_02"},
    {"prompt": "1girl, black hair, long hair, large eyes, close up face, mysterious", "alias": "sq_03"},
    {"prompt": "1girl, blonde hair, blue eyes, close up face, gentle", "alias": "sq_04"},
    {"prompt": "1girl, silver hair, red eyes, close up face, cool", "alias": "sq_05"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 1024,
        "height": 1024,
        "model": "animagine-xl-4",
        "style": "split_sketch",
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
    print("스플릿 스케치 정사각형 테스트 5장 (1024x1024)", flush=True)
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
