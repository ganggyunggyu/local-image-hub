"""하네카와 & 블랙 하네카와 테스트 (10장)
하네카와 5장 + 블랙 하네카와 5장
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_hanekawa_test"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 하네카와 츠바사 (일반)
TSUBASA = "hanekawa tsubasa, monogatari, black hair, long hair, glasses, purple eyes, school uniform"

# 블랙 하네카와 (츠바사 캣)
BLACK = "black hanekawa, monogatari, white hair, long hair, golden eyes, slit pupils, cat ears, pale skin"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    # 하네카와 5장
    {"prompt": f"1girl, {TSUBASA}, classroom, window, sunlight, sitting", "alias": "tsubasa_01", "style": "pale_aqua"},
    {"prompt": f"1girl, {TSUBASA}, library, books, reading, quiet", "alias": "tsubasa_02", "style": "pale_aqua"},
    {"prompt": f"1girl, {TSUBASA}, rooftop, sunset, wind, standing", "alias": "tsubasa_03", "style": "pale_aqua"},
    {"prompt": f"1girl, {TSUBASA}, night, street, walking, city lights", "alias": "tsubasa_04", "style": "pale_aqua"},
    {"prompt": f"1girl, {TSUBASA}, close up, portrait, looking at viewer, smile", "alias": "tsubasa_05", "style": "pale_aqua"},
    # 블랙 하네카와 5장
    {"prompt": f"1girl, {BLACK}, night, moonlight, rooftop, standing", "alias": "black_01", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, street, night, neon lights, walking", "alias": "black_02", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, close up, portrait, looking at viewer, smirk", "alias": "black_03", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, sitting, night, window, moon", "alias": "black_04", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, standing, alley, night, mysterious", "alias": "black_05", "style": "pale_aqua"},
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
    print("하네카와 & 블랙 하네카와 테스트 10장", flush=True)
    print("하네카와 5장 + 블랙 하네카와 5장", flush=True)
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
