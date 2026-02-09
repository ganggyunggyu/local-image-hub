"""봇치더락 서브캐릭터 3인조 테스트 (10장)
키쿠리 x PA상 x 세이카 (니지카 언니)
pale_aqua 5장 + watercolor_sketch 5장
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_bocchi_side_test"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# CLIP 77토큰 제한 대응: 이름 + 핵심 외형만 (작품명 생략)
KIKURI = "hiroi kikuri, pink hair, purple eyes, side braid"
PA = "pa-san, black hair, green eyes"
SEIKA = "ijichi seika, blonde hair, red eyes, ahoge"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

# 위치 태그로 캐릭터 분리
L = "girl on left"
C = "girl in center"
R = "girl on right"

JOBS = [
    # pale_aqua 5장
    {
        "prompt": f"3girls, {L} {KIKURI}, {C} {PA}, {R} {SEIKA}, bar counter, drinking, night",
        "alias": "side01_bar",
        "style": "pale_aqua",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"3girls, {L} {KIKURI} drunk, {C} {PA} annoyed, {R} {SEIKA} arms crossed, backstage",
        "alias": "side02_starry",
        "style": "pale_aqua",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"3girls, {L} {KIKURI} sleeping, {C} {PA} reading, {R} {SEIKA} coffee, cafe",
        "alias": "side03_morning",
        "style": "pale_aqua",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"3girls, {L} {KIKURI} bass guitar, {C} {PA} headphones, {R} {SEIKA} microphone, studio",
        "alias": "side04_studio",
        "style": "pale_aqua",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"3girls, {L} {KIKURI}, {C} {PA}, {R} {SEIKA}, walking, city night, neon",
        "alias": "side05_night",
        "style": "pale_aqua",
        "w": 1216, "h": 832,
    },
    # watercolor_sketch 5장
    {
        "prompt": f"3girls, {L} {KIKURI} laughing, {C} {PA} sighing, {R} {SEIKA} smiling, izakaya",
        "alias": "side06_izakaya",
        "style": "watercolor_sketch",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"3girls, {L} {KIKURI}, {C} {PA}, {R} {SEIKA}, rooftop, sunset, wind",
        "alias": "side07_rooftop",
        "style": "watercolor_sketch",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"3girls, {L} {KIKURI} umbrella, {C} {PA} hood, {R} {SEIKA} umbrella, rain",
        "alias": "side08_rain",
        "style": "watercolor_sketch",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"3girls, {L} {KIKURI}, {C} {PA}, {R} {SEIKA}, concert audience, stage",
        "alias": "side09_audience",
        "style": "watercolor_sketch",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"3girls, {L} {KIKURI} lying down, {C} {PA} sitting, {R} {SEIKA} leaning, park bench",
        "alias": "side10_park",
        "style": "watercolor_sketch",
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
    print("봇치더락 서브캐릭 3인조 테스트 10장", flush=True)
    print("키쿠리 x PA상 x 세이카(니지카 언니)", flush=True)
    print("pale_aqua 5장 + watercolor_sketch 5장", flush=True)
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
