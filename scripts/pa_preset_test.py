"""PA상 프리셋 테스트 (10장)
waterful 5장 + pale_aqua 5장
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pa_preset_test"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PA = "pa-san, black hair, green eyes, labret piercing, ear piercing"
NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    # waterful 5장
    {"prompt": f"1girl, {PA}, headphones, mixing console, studio, focused", "alias": "pa01_waterful", "style": "waterful"},
    {"prompt": f"1girl, {PA}, goth fashion, black dress, choker, standing", "alias": "pa02_waterful", "style": "waterful"},
    {"prompt": f"1girl, {PA}, looking at viewer, close up, portrait", "alias": "pa03_waterful", "style": "waterful"},
    {"prompt": f"1girl, {PA}, night, street, city lights, cool expression", "alias": "pa04_waterful", "style": "waterful"},
    {"prompt": f"1girl, {PA}, coffee, cafe, reading, quiet", "alias": "pa05_waterful", "style": "waterful"},
    # pale_aqua 5장
    {"prompt": f"1girl, {PA}, headphones, mixing console, studio, focused", "alias": "pa06_aqua", "style": "pale_aqua"},
    {"prompt": f"1girl, {PA}, goth fashion, black dress, choker, standing", "alias": "pa07_aqua", "style": "pale_aqua"},
    {"prompt": f"1girl, {PA}, looking at viewer, close up, portrait", "alias": "pa08_aqua", "style": "pale_aqua"},
    {"prompt": f"1girl, {PA}, night, street, city lights, cool expression", "alias": "pa09_aqua", "style": "pale_aqua"},
    {"prompt": f"1girl, {PA}, coffee, cafe, reading, quiet", "alias": "pa10_aqua", "style": "pale_aqua"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 832,
        "height": 1216,
        "model": "animagine-xl-4",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} [{job['style']}] (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print("PA상 프리셋 테스트 10장", flush=True)
    print("waterful 5장 + pale_aqua 5장", flush=True)
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
