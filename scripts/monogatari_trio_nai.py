"""모노가타리 시리즈 - 모니터링 밈 (극한 클로즈업 + 사이키델릭) NAI"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_monitoring_v3"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTERS = [
    {"label": "hitagi", "tags": "senjougahara hitagi, long purple hair, purple eyes"},
    {"label": "sodachi", "tags": "oikura sodachi, light brown hair, green eyes"},
    {"label": "mayoi", "tags": "hachikuji mayoi, black hair, red eyes"},
    {"label": "suruga", "tags": "kanbaru suruga, short dark blue hair, brown eyes"},
    {"label": "nadeko", "tags": "sengoku nadeko, orange hair, bangs"},
    {"label": "tsubasa", "tags": "hanekawa tsubasa, black hair, braids"},
    {"label": "tsubasa_short", "tags": "hanekawa tsubasa, short white hair, golden eyes, cat ears, black hanekawa"},
    {"label": "shinobu", "tags": "oshino shinobu, blonde hair, golden eyes, vampire"},
    {"label": "karen", "tags": "araragi karen, black hair, ponytail"},
    {"label": "yotsugi", "tags": "ononoki yotsugi, teal hair, hat, expressionless"},
    {"label": "ougi", "tags": "oshino ougi, short black hair, dark eyes, pale skin"},
]

STYLES = [
    # A: 전신 피쉬아이 — 레제 짤 스타일 (카메라 향해 손 뻗기 + 네온 시티)
    "fisheye, from below, full body, looking at viewer, reaching toward viewer, spread fingers, foreshortening, casual clothes, neon city night, vibrant colors, dynamic perspective, detailed background",
    # B: 상반신 클로즈업 — 얼굴+상체 보이면서 사이키델릭 배경
    "upper body, close-up, looking at viewer, one hand reaching toward viewer, head tilt, psychedelic background, neon pink, neon blue, hearts, stars, sparkles, glowing, pop art, dark background",
    # C: 얼굴 클로즈업 — 모니터링 밈 (큰 눈 + 네온 글로우)
    "close-up face, both eyes visible, large detailed eyes, looking at viewer, glowing iris, psychedelic, abstract background, neon accents, sparkles, stars, split color pink blue, lens flare, intense",
]

JOBS = []

for char in CHARACTERS:
    for i, style in enumerate(STYLES):
        JOBS.append({
            "prompt": f"1girl, {char['tags']}, {style}",
            "name": f"{char['label']}_{i:02d}_{['fisheye', 'upper', 'face'][i]}",
        })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece, best quality, detailed iris, glowing effects, neon lighting",
        "negative_prompt": "low quality, worst quality, blurry, realistic, photorealistic, full body, wide shot, simple background, white background, plain, boring, text",
        "width": 1216,
        "height": 832,
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
            print(f"[{num:02d}/{TOTAL}] OK {job['name']} (seed: {seed})")
            return True
        else:
            print(f"[{num:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:60]}")
            return False
    except Exception as e:
        print(f"[{num:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"모노가타리 3인 × 5포즈 - NAI {TOTAL}장")
    print(f"  소다치: 5장 / 히타기: 5장 / 마요이: 5장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(1.0)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
