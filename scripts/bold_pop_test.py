"""bold_pop 스타일 테스트"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_bold_pop"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# bold_pop: 굵은 선, 진한 색감, 하이콘트라스트, 광택
JOBS = [
    # 히로이 키쿠리 (봇치더락) - 원본 이미지와 비슷한 캐릭터
    {
        "prompt": "1girl, hiroi kikuri, bocchi the rock!, magenta hair, braid, drunk, open mouth, laughing, camisole, sake bottle, upper body, masterpiece",
        "alias": "kikuri_bold",
        "name": "키쿠리",
    },
    # 냥냥돌쇠
    {
        "prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes, smirk, confident, upper body, masterpiece",
        "alias": "dolsoe_bold",
        "name": "냥냥돌쇠",
    },
    # 모모카 (걸밴크)
    {
        "prompt": "1girl, kawaragi momoka, girls band cry, silver hair, tomboyish, cool, guitar, confident pose, upper body, masterpiece",
        "alias": "momoka_bold",
        "name": "모모카",
    },
    # 료 (봇치더락)
    {
        "prompt": "1girl, yamada ryo, bocchi the rock!, blue short hair, expressionless, cool, bass guitar, stylish, upper body, masterpiece",
        "alias": "ryo_bold",
        "name": "료",
    },
    # 니나 (걸밴크)
    {
        "prompt": "1girl, iseri nina, girls band cry, purple hair, twintails, passionate, singing, microphone, energetic, upper body, masterpiece",
        "alias": "nina_bold",
        "name": "니나",
    },
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
    print(f"bold_pop 스타일 테스트 {TOTAL}장")
    print("굵은 선 + 진한 색감 + 하이콘트라스트")
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
