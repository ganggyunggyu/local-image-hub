"""프리렌 & 힘멜 투샷 - NAI V4.5 최적화"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pale_aqua"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# NAI V4.5 최적화 프롬프트
# 순서: 인물수 → 캐릭터 → 품질 → 구도 → 배경 → 외형 → 자세
JOBS = [
    # 석양 - 서로 바라보기 (mutual 상호작용)
    {
        "prompt": "1boy 1girl, frieren, himmel, sousou no frieren, masterpiece, very aesthetic, upper body, 1.3::sunset, flower field::, white long hair, elf ears, green eyes, blue hair, handsome, mutual#looking at another, gentle smile",
        "alias": "frieren_himmel_v2_01",
        "name": "석양 (최적화)",
    },
    # 모험 - 함께 걷기
    {
        "prompt": "1boy 1girl, frieren, himmel, sousou no frieren, masterpiece, very aesthetic, full body, forest path, 1.2::warm light, nostalgic::, white long hair, elf ears, blue hair, walking together, from behind",
        "alias": "frieren_himmel_v2_02",
        "name": "모험 (최적화)",
    },
    # 카페 - 마주 앉기
    {
        "prompt": "1boy 1girl, frieren, himmel, sousou no frieren, masterpiece, very aesthetic, upper body, cafe, window light, white long hair, elf ears, blue hair, sitting, 1.2::tea, peaceful::, happy",
        "alias": "frieren_himmel_v2_03",
        "name": "카페 (최적화)",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "low quality, worst quality, bad anatomy, deformed hands, blurry",
        "width": 1024,
        "height": 832,
        "steps": 28,
        "guidance_scale": 5.5,  # V4.5 권장값
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": "pale_aqua",
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
    print(f"프리렌 & 힘멜 (NAI V4.5 최적화) {TOTAL}장")
    print("Guidance: 5.5, 네거티브 추가, 가중치 문법 적용")
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
