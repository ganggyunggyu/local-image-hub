"""걸밴크라이 새끼손가락 + NANA 레이라 - 프리셋 적용"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_gbc_styled"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 프리셋: cozy_gouache, waterful, pale_aqua, monogatari
STYLES = ["cozy_gouache", "waterful", "pale_aqua", "monogatari"]

# 캐릭터 + 포즈
CHARS = [
    {"prompt": "1girl, nina, girls band cry, short blonde hair, red eyes, pinky finger up, confident, upper body", "name": "nina"},
    {"prompt": "1girl, momoka, girls band cry, pink hair, twintails, pinky finger up, cheerful, upper body", "name": "momoka"},
    {"prompt": "1girl, subaru, girls band cry, green hair, pinky finger up, calm, cool, upper body", "name": "subaru"},
    {"prompt": "1girl, rupa, girls band cry, dark skin, white hair, pinky finger raised, cool, upper body", "name": "rupa"},
    {"prompt": "1girl, tomo, girls band cry, brown hair, small, pinky up, determined, upper body", "name": "tomo"},
    {"prompt": "1girl, serizawa reira, layla, nana (anime), blonde hair, elegant, singing, beautiful, upper body", "name": "layla"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, pinky finger up, confident, cool, upper body", "name": "dolsoe"},
]

# 조합 생성
JOBS = []
for char in CHARS:
    for style in STYLES:
        JOBS.append({
            "prompt": char["prompt"],
            "name": f"{char['name']}_{style}",
            "style": style,
        })

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{job['prompt']}, masterpiece",
        "negative_prompt": "low quality, worst quality, bad hands, extra fingers",
        "width": 832,
        "height": 1024,
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
    print(f"걸밴크라이 + 레이라 x 4스타일 = {TOTAL}장")
    print(f"스타일: {', '.join(STYLES)}")
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
