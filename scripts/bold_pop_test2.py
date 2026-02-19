"""bold_pop 스타일 추가 테스트 10장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_bold_pop"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    # 봇치더락
    {"prompt": "1girl, gotoh hitori, bocchi the rock!, pink long hair, blue eyes, anxious, guitar, upper body, masterpiece", "alias": "bocchi_bold", "name": "봇치"},
    {"prompt": "1girl, kita ikuyo, bocchi the rock!, red hair, yellow eyes, energetic, smile, wink, upper body, masterpiece", "alias": "kita_bold", "name": "키타"},
    {"prompt": "1girl, ijichi nijika, bocchi the rock!, blonde ponytail, cheerful, drumsticks, upper body, masterpiece", "alias": "nijika_bold", "name": "니지카"},
    # 걸밴크
    {"prompt": "1girl, ebizuka tomo, girls band cry, ash brown hair, red eyes, small, intense, keyboard, upper body, masterpiece", "alias": "tomo_bold", "name": "토모"},
    {"prompt": "1girl, awa subaru, girls band cry, green hair, quiet, drums, upper body, masterpiece", "alias": "subaru_bold", "name": "스바루"},
    # 케이온
    {"prompt": "1girl, akiyama mio, k-on!, black long hair, shy, bass guitar, cool, upper body, masterpiece", "alias": "mio_bold", "name": "미오"},
    {"prompt": "1girl, tainaka ritsu, k-on!, light brown hair, headband, energetic, drumsticks, upper body, masterpiece", "alias": "ritsu_bold", "name": "리츠"},
    # 하네카와
    {"prompt": "1girl, black hanekawa, monogatari, white long hair, cat ears, yellow eyes, smirk, upper body, masterpiece", "alias": "black_hanekawa_bold", "name": "블랙하네카와"},
    # 프리렌
    {"prompt": "1girl, frieren, sousou no frieren, white hair, elf ears, green eyes, staff, confident, upper body, masterpiece", "alias": "frieren_bold", "name": "프리렌"},
    # 돌쇠 다른 포즈
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, yandere, crazy smile, upper body, masterpiece", "alias": "dolsoe_yandere_bold", "name": "냥냥돌쇠 얀데레"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "low quality, worst quality, bad anatomy",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "guidance_scale": 6.0,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": "bold_pop",
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
    print(f"bold_pop 추가 테스트 {TOTAL}장")
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
