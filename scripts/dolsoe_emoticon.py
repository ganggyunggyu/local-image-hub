"""냥냥돌쇠 이모티콘/스티커 세트 (10개)
다양한 표정과 감정
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_emoticon"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 냥냥돌쇠 캐릭터 (chibi 태그는 프리셋에서 추가됨)
CHAR = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, mole under eye"
NEG = "realistic, detailed background, mature, multiple views, grid"

JOBS = [
    # 기본 감정
    {"prompt": f"{CHAR}, happy, smile, sparkle eyes", "alias": "emo_happy"},
    {"prompt": f"{CHAR}, sad, crying, tears", "alias": "emo_sad"},
    {"prompt": f"{CHAR}, angry, puffed cheeks, pouting", "alias": "emo_angry"},
    {"prompt": f"{CHAR}, surprised, wide eyes, open mouth", "alias": "emo_surprise"},
    {"prompt": f"{CHAR}, sleepy, half closed eyes, zzz", "alias": "emo_sleepy"},
    # 특수 감정
    {"prompt": f"{CHAR}, heart eyes, blushing, hearts", "alias": "emo_love"},
    {"prompt": f"{CHAR}, shy, blushing, looking away", "alias": "emo_shy"},
    {"prompt": f"{CHAR}, confused, question mark, tilted head", "alias": "emo_confused"},
    {"prompt": f"{CHAR}, thumbs up, wink", "alias": "emo_thumbsup"},
    {"prompt": f"{CHAR}, cat paw pose, playful", "alias": "emo_nya"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 768,
        "height": 768,
        "model": "animagine-xl-4",
        "style": "chibi_sketch",
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
    print("냥냥돌쇠 이모티콘 세트 10개", flush=True)
    print("기쁨/슬픔/화남/놀람/졸림/사랑/수줍/의문/엄지척/냥포즈", flush=True)
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
