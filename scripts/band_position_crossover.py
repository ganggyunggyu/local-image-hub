"""밴드 포지션별 크로스오버 단체샷 - 수정본"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_band_crossover"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STYLES = ["pale_aqua", "monogatari", "waterful"]

# 정확한 포지션:
# 리드기타: 유이(케이온), 봇치(봇치더락), 모모카(걸밴크)
# 리듬기타: 아즈사(케이온), 키타(봇치더락), 니나(걸밴크-피날레)
# 베이스: 미오(케이온), 료(봇치더락), 루파(걸밴크)
# 드럼: 리츠(케이온), 니지카(봇치더락), 스바루(걸밴크)
# 키보드: 무기(케이온), 토모(걸밴크)
# 보컬: 유이(케이온), 키타(봇치더락), 니나(걸밴크)

JOBS = [
    # 리드기타리스트 모임
    {
        "prompt": "3girls, multiple series crossover, lead guitarists gathering, music studio, electric guitars, (hirasawa yui, k-on!, brown hair, gibson les paul), (gotoh hitori, bocchi the rock!, pink long hair, les paul custom), (kawaragi momoka, girls band cry, silver hair, jazzmaster), comparing techniques, masterpiece, best quality",
        "style": "waterful",
        "alias": "lead_guitar_waterful",
        "name": "리드기타 모임",
    },
    # 리듬기타리스트 모임
    {
        "prompt": "3girls, multiple series crossover, rhythm guitarists gathering, practice room, guitars, (nakano azusa, k-on!, black twintails, fender mustang), (kita ikuyo, bocchi the rock!, red hair, les paul junior), (iseri nina, girls band cry, purple twintails), jamming together, masterpiece, best quality",
        "style": "waterful",
        "alias": "rhythm_guitar_waterful",
        "name": "리듬기타 모임",
    },
    # 베이시스트 모임
    {
        "prompt": "3girls, multiple series crossover, bassists gathering, studio, bass guitars, (akiyama mio, k-on!, black long hair, fender jazz bass), (yamada ryo, bocchi the rock!, blue short hair, expressionless, precision bass), (rupa, girls band cry, dark skin, sg bass), cool vibes, masterpiece, best quality",
        "style": "waterful",
        "alias": "bass_waterful",
        "name": "베이시스트 모임",
    },
    # 드러머 모임
    {
        "prompt": "3girls, multiple series crossover, drummers gathering, drum room, drum kits, drumsticks, (tainaka ritsu, k-on!, light brown hair, headband, energetic), (ijichi nijika, bocchi the rock!, blonde ponytail, cheerful, leader), (awa subaru, girls band cry, green hair, quiet), rhythm session, masterpiece, best quality",
        "style": "waterful",
        "alias": "drums_waterful",
        "name": "드러머 모임",
    },
    # 키보디스트 모임
    {
        "prompt": "2girls, multiple series crossover, keyboardists gathering, piano room, keyboards, (kotobuki tsumugi, k-on!, blonde hair, thick eyebrows, elegant, synthesizer), (ebizuka tomo, girls band cry, ash brown hair, red eyes, nord keyboard), playing together, masterpiece, best quality",
        "style": "waterful",
        "alias": "keyboard_waterful",
        "name": "키보디스트 모임",
    },
    # 보컬 모임
    {
        "prompt": "3girls, multiple series crossover, vocalists gathering, karaoke room, microphones, singing, (hirasawa yui, k-on!, brown hair, cheerful, main vocal), (kita ikuyo, bocchi the rock!, red hair, energetic, idol-like), (iseri nina, girls band cry, purple twintails, passionate, emotional), having fun, masterpiece, best quality",
        "style": "waterful",
        "alias": "vocal_waterful",
        "name": "보컬 모임",
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
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['name']} - {job['style']}")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"포지션별 크로스오버 단체샷 {TOTAL}장 (수정본)")
    print("리드기타 / 리듬기타 / 베이스 / 드럼 / 키보드 / 보컬")
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
