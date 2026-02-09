"""봇치더락 캐릭터명 인식 테스트 (10장)
작품명 + 캐릭터명 + 비주얼 태그 조합 테스트
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_bocchi_name_test"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SERIES = "bocchi the rock!"
BOCCHI = f"{SERIES}, gotoh hitori, pink long hair, blue eyes, pink track jacket"
NIJIKA = f"{SERIES}, ijichi nijika, blonde short hair, blue eyes, side braid"
RYO = f"{SERIES}, yamada ryo, blue long hair, red eyes"
KITA = f"{SERIES}, kita ikuyo, red long hair, green eyes, star hair ornament"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    # 솔로 4장
    {
        "prompt": f"1girl, {BOCCHI}, nervous, school uniform, classroom, hiding behind desk",
        "alias": "bt01_bocchi",
        "w": 832, "h": 1216,
    },
    {
        "prompt": f"1girl, {NIJIKA}, smile, drumsticks, music studio, energetic",
        "alias": "bt02_nijika",
        "w": 832, "h": 1216,
    },
    {
        "prompt": f"1girl, {RYO}, cool, bass guitar, standing, white background",
        "alias": "bt03_ryo",
        "w": 832, "h": 1216,
    },
    {
        "prompt": f"1girl, {KITA}, cheerful, guitar, peace sign, school rooftop",
        "alias": "bt04_kita",
        "w": 832, "h": 1216,
    },
    # 투샷 3장
    {
        "prompt": f"2girls, multiple girls, girl on left {BOCCHI} nervous, girl on right {KITA} hugging, school, comedy",
        "alias": "bt05_bocchi_kita",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"2girls, multiple girls, girl on left {RYO} cool, girl on right {NIJIKA} laughing, cafe, sitting",
        "alias": "bt06_ryo_nijika",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"2girls, multiple girls, girl on left {BOCCHI} shy, girl on right {RYO} deadpan, bench, park, quiet",
        "alias": "bt07_bocchi_ryo",
        "w": 1216, "h": 832,
    },
    # 그룹 3장
    {
        "prompt": f"4girls, multiple girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, band, stage, concert, spotlight, instruments",
        "alias": "bt08_kessoku_live",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"4girls, multiple girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, casual clothes, group photo, cherry blossoms, spring",
        "alias": "bt09_kessoku_photo",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"4girls, multiple girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, school uniform, classroom, after school, relaxing",
        "alias": "bt10_kessoku_school",
        "w": 1216, "h": 832,
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": job["w"],
        "height": job["h"],
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
    print("봇치더락 캐릭터명 인식 테스트 10장", flush=True)
    print("작품명 + 캐릭터명 + 비주얼 태그 조합", flush=True)
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
