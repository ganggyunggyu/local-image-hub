"""밴드 포지션별 크로스오버 - 프롬프트 최적화"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_band_crossover"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# NAI V4.5 최적화: 75토큰 이하, 10-30태그, 중요컨셉 앞에
JOBS = [
    # 리드기타 (유이, 봇치, 모모카)
    {
        "prompt": "3girls, guitarists, studio, hirasawa yui, brown hair, gotoh hitori, pink hair, kawaragi momoka, silver hair, electric guitars, sitting, masterpiece",
        "alias": "lead_guitar_v2",
        "name": "리드기타",
    },
    # 리듬기타 (아즈사, 키타, 니나)
    {
        "prompt": "3girls, guitarists, practice room, nakano azusa, black twintails, kita ikuyo, red hair, iseri nina, purple twintails, guitars, standing, masterpiece",
        "alias": "rhythm_guitar_v2",
        "name": "리듬기타",
    },
    # 베이스 (미오, 료, 루파)
    {
        "prompt": "3girls, bassists, studio, akiyama mio, black long hair, yamada ryo, blue short hair, rupa, dark skin, bass guitars, cool, masterpiece",
        "alias": "bass_v2",
        "name": "베이스",
    },
    # 드럼 (리츠, 니지카, 스바루)
    {
        "prompt": "3girls, drummers, drum room, tainaka ritsu, light brown hair, headband, ijichi nijika, blonde ponytail, awa subaru, green hair, drumsticks, masterpiece",
        "alias": "drums_v2",
        "name": "드럼",
    },
    # 키보드 (무기, 토모)
    {
        "prompt": "2girls, keyboardists, piano room, kotobuki tsumugi, blonde hair, thick eyebrows, ebizuka tomo, ash brown hair, red eyes, keyboards, elegant, masterpiece",
        "alias": "keyboard_v2",
        "name": "키보드",
    },
    # 보컬 (유이, 키타, 니나)
    {
        "prompt": "3girls, vocalists, karaoke, hirasawa yui, brown hair, kita ikuyo, red hair, iseri nina, purple twintails, microphones, singing, happy, masterpiece",
        "alias": "vocal_v2",
        "name": "보컬",
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
        "style": "waterful",
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
    print(f"포지션별 크로스오버 (프롬프트 최적화) {TOTAL}장")
    print("스타일: waterful 고정")
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
