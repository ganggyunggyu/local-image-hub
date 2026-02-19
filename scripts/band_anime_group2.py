"""밴드 애니 단체샷 추가 - 캐릭터 분리 개선"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_band_anime"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STYLES = ["pale_aqua", "monogatari", "waterful"]

# 캐릭터별 분리 프롬프트 (NAI 스타일)
JOBS = [
    # 케이온 - 라이브 (재시도)
    {
        "prompt": "5girls, k-on!, band, concert stage, instruments, spotlight, (hirasawa yui, brown hair, guitar), (akiyama mio, black long hair, bass), (tainaka ritsu, light brown hair, headband, drums), (kotobuki tsumugi, blonde hair, keyboard), (nakano azusa, black twintails, guitar), playing music, dynamic, masterpiece, best quality",
        "style": "monogatari",
        "alias": "keion_live",
        "name": "케이온 라이브",
    },
    # 봇치 - 라이브하우스
    {
        "prompt": "4girls, bocchi the rock!, kessoku band, livehouse, stage, (gotoh hitori, pink long hair, pink tracksuit, lead guitar), (ijichi nijika, blonde ponytail, drums), (yamada ryo, blue short hair, bass), (kita ikuyo, red hair, rhythm guitar), performing, energetic, masterpiece, best quality",
        "style": "waterful",
        "alias": "bocchi_live",
        "name": "봇치더락 라이브",
    },
    # GBC - 스트리트
    {
        "prompt": "5girls, girls band cry, togenashi togeari, street performance, urban, (iseri nina, purple twintails, vocalist), (kawaragi momoka, silver hair, guitar), (awa subaru, green hair), (rupa, dark skin), (ebizuka tomo, ash brown hair, red eyes, drums), passionate, masterpiece, best quality",
        "style": "pale_aqua",
        "alias": "gbc_street",
        "name": "걸밴크 스트리트",
    },
    # 크로스오버 - 기타리스트들
    {
        "prompt": "4girls, crossover, guitarists, music studio, (hirasawa yui, k-on!, brown hair, les paul guitar), (gotoh hitori, bocchi the rock!, pink hair, guitar), (iseri nina, girls band cry, purple twintails, guitar), (nakano azusa, k-on!, black twintails, mustang guitar), jamming together, masterpiece, best quality",
        "style": "pale_aqua",
        "alias": "crossover_guitar",
        "name": "크로스오버 기타",
    },
    # 크로스오버 - 드러머들
    {
        "prompt": "3girls, crossover, drummers, practice room, (tainaka ritsu, k-on!, light brown hair, headband, drum kit), (ijichi nijika, bocchi the rock!, blonde ponytail, energetic), (ebizuka tomo, girls band cry, ash brown hair, red eyes, intense), drumsticks, rhythm, masterpiece, best quality",
        "style": "monogatari",
        "alias": "crossover_drums",
        "name": "크로스오버 드럼",
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
    print(f"밴드 애니 단체샷 추가 {TOTAL}장")
    print("캐릭터 분리 개선 + 크로스오버")
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
