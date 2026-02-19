"""NANA 캐릭터 테스트 - 담배 + 단체샷"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_nana"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    # 오사키 나나 (BLAST 보컬)
    {"prompt": "1girl, oosaki nana, nana (anime), short black hair, punk style, cigarette, smoking, leather jacket, choker, cool, upper body", "name": "nana_smoke1"},
    {"prompt": "1girl, oosaki nana, nana (anime), short black hair, singing, microphone, stage, dramatic lighting", "name": "nana_sing"},
    {"prompt": "1girl, oosaki nana, nana (anime), short black hair, cigarette in mouth, looking away, melancholic, night", "name": "nana_smoke2"},
    {"prompt": "1girl, oosaki nana, nana (anime), short black hair, leather outfit, confident, punk, standing", "name": "nana_punk"},

    # 코마츠 나나 (하치)
    {"prompt": "1girl, komatsu nana, hachi, nana (anime), long brown hair, innocent, cute, pink clothes, upper body", "name": "hachi_cute"},
    {"prompt": "1girl, komatsu nana, hachi, nana (anime), long brown hair, cheerful, smile, strawberry motif", "name": "hachi_smile"},
    {"prompt": "1girl, komatsu nana, hachi, nana (anime), long brown hair, crying, emotional, vulnerable", "name": "hachi_cry"},
    {"prompt": "1girl, komatsu nana, hachi, nana (anime), long brown hair, happy, casual clothes, warm", "name": "hachi_happy"},

    # 혼조 렌 (TRAPNEST)
    {"prompt": "1boy, honjo ren, nana (anime), blonde hair, long hair, handsome, cigarette, cool, leather jacket, upper body", "name": "ren_smoke"},
    {"prompt": "1boy, honjo ren, nana (anime), blonde hair, guitar, performing, stage, dramatic", "name": "ren_guitar"},

    # 타쿠미 (TRAPNEST 베이스)
    {"prompt": "1boy, ichinose takumi, nana (anime), black hair, handsome, suit, cigarette, businessman, upper body", "name": "takumi_smoke"},
    {"prompt": "1boy, ichinose takumi, nana (anime), black hair, bass guitar, performing, cool", "name": "takumi_bass"},

    # 신 (BLAST 베이스)
    {"prompt": "1boy, terashima shinichi, shin, nana (anime), blonde short hair, punk, cigarette, bass guitar, upper body", "name": "shin_smoke"},
    {"prompt": "1boy, terashima shinichi, shin, nana (anime), blonde short hair, energetic, punk style", "name": "shin_punk"},

    # 야스 (BLAST 드럼)
    {"prompt": "1boy, takagi yasushi, yasu, nana (anime), bald, sunglasses, mature, cigarette, cool, calm, upper body", "name": "yasu_smoke"},
    {"prompt": "1boy, takagi yasushi, yasu, nana (anime), bald, sunglasses, drums, performing", "name": "yasu_drums"},

    # 노부 (BLAST 기타)
    {"prompt": "1boy, nobu, nana (anime), messy hair, guitar, punk, cigarette, casual, upper body", "name": "nobu_smoke"},

    # 두 나나
    {"prompt": "2girls, oosaki nana, komatsu nana, nana (anime), short black hair, long brown hair, together, contrast, punk and cute, friendship, upper body", "name": "two_nana"},
    {"prompt": "2girls, oosaki nana, komatsu nana, nana (anime), hugging, emotional, best friends, apartment", "name": "two_nana_hug"},

    # BLAST 단체
    {"prompt": "4people, band, nana (anime), blast band, punk rock, stage, performing, dramatic lighting, concert", "name": "blast_band"},
    {"prompt": "group, nana (anime), blast members, smoking together, night, rooftop, casual, relaxed", "name": "blast_smoke"},

    # TRAPNEST 단체
    {"prompt": "4people, band, nana (anime), trapnest band, glamorous, stage, performing, professional", "name": "trapnest_band"},

    # 분위기샷
    {"prompt": "1girl, oosaki nana, nana (anime), short black hair, cigarette, window, rain, melancholic, thinking, atmospheric", "name": "nana_rain"},
    {"prompt": "2girls, oosaki nana, komatsu nana, nana (anime), apartment 707, living together, cozy, domestic", "name": "apartment_707"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{job['prompt']}, masterpiece, 2000s anime style",
        "negative_prompt": "low quality, worst quality, child, underage",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{idx:02d}_{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"NANA 캐릭터 테스트 {TOTAL}장")
    print(f"담배 + 단체샷 포함")
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


if __name__ == "__main__":
    asyncio.run(main())
