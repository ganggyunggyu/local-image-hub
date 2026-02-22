"""모노가타리 시리즈 전 캐릭터 - 화이트보드 교실 스케치 스타일 NAI"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_labcoat"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPT_SUFFIX = "lab coat, writing on whiteboard, classroom, thinking face, clean lines, digital sketch"
NEGATIVE = "smile, blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, logo, dated, signature, multiple views, gigantic breasts"

CHARACTERS = [
    {"name": "hitagi", "tags": "1girl, senjougahara hitagi, long purple hair, sharp eyes, slender"},
    {"name": "mayoi", "tags": "1girl, hachikuji mayoi, long black hair, twin tails, red eyes"},
    {"name": "sodachi", "tags": "1girl, oikura sodachi, light brown hair, twin tails, sharp eyes, green eyes"},
    {"name": "suruga", "tags": "1girl, kanbaru suruga, short dark blue hair, tan skin, athletic"},
    {"name": "nadeko", "tags": "1girl, sengoku nadeko, long orange hair, bangs covering eyes, shy"},
    {"name": "tsubasa", "tags": "1girl, hanekawa tsubasa, long black hair, braids, calm expression"},
    {"name": "shinobu", "tags": "1girl, oshino shinobu, long blonde hair, golden eyes, vampire, pointy ears"},
    {"name": "karen", "tags": "1girl, araragi karen, long black hair, ponytail, tall, energetic"},
    {"name": "tsukihi", "tags": "1girl, araragi tsukihi, short black hair, kimono style, calm"},
    {"name": "yotsugi", "tags": "1girl, ononoki yotsugi, teal hair, hat, expressionless, deadpan"},
    {"name": "ougi", "tags": "1girl, oshino ougi, short black hair, dark eyes, mysterious, pale skin"},
    {"name": "gaen", "tags": "1girl, gaen izuko, short grey hair, mature, confident, smirk"},
    {"name": "koyomi", "tags": "1boy, araragi koyomi, short black hair, ahoge, school uniform"},
    {"name": "meme", "tags": "1boy, oshino meme, messy blonde hair, hawaiian shirt, stubble, relaxed"},
    {"name": "kaiki", "tags": "1boy, kaiki deishuu, black suit, dark hair, tired eyes, con man"},
]

JOBS = []

for char in CHARACTERS:
    JOBS.append({
        "prompt": f"{char['tags']}, {PROMPT_SUFFIX}",
        "name": char["name"],
    })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece, best quality",
        "negative_prompt": NEGATIVE,
        "width": 832,
        "height": 1216,
        "provider": "nai",
        "model": "nai-diffusion-4-full",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=120.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{num:02d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{num:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:60]}")
            return False
    except Exception as e:
        print(f"[{num:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"모노가타리 시리즈 × 화이트보드 교실 - NAI full {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(1.5)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
