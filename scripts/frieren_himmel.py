"""프리렌 & 힘멜 투샷 3장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pale_aqua"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 프리렌: 은발, 긴머리, 엘프귀, 녹색눈, 지팡이
# 힘멜: 파란머리, 용사, 검, 잘생김

JOBS = [
    {
        "prompt": "1boy 1girl, frieren, white hair, long hair, elf ears, green eyes, himmel, blue hair, handsome, sousou no frieren, looking at each other, sunset, flowers, gentle, masterpiece",
        "alias": "frieren_himmel_01",
        "name": "프리렌x힘멜 석양",
    },
    {
        "prompt": "1boy 1girl, frieren, white hair, elf ears, himmel, blue hair, sousou no frieren, adventure, walking together, forest path, warm light, nostalgic, masterpiece",
        "alias": "frieren_himmel_02",
        "name": "프리렌x힘멜 모험",
    },
    {
        "prompt": "1boy 1girl, frieren, white hair, long hair, elf ears, himmel, blue hair, sousou no frieren, cafe, sitting together, tea, peaceful, window light, happy, masterpiece",
        "alias": "frieren_himmel_03",
        "name": "프리렌x힘멜 카페",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "",
        "width": 1024,
        "height": 832,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": "pale_aqua",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['name']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"프리렌 & 힘멜 투샷 {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.5)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
