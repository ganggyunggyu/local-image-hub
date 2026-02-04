"""
실사 모델 비교 테스트
- 같은 프롬프트를 여러 모델로 생성해서 비교
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_realistic_test"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODELS = [
    {"name": "sdxl", "steps": 30, "guidance": 7.0},
    {"name": "flux-schnell", "steps": 4, "guidance": 0.0},
    {"name": "flux-dev", "steps": 28, "guidance": 3.5},
]

PROMPTS = [
    {
        "prompt": "portrait of a young woman, natural light, cafe, bokeh background, film grain",
        "negative": "cartoon, anime, illustration, painting, ugly, deformed",
        "alias": "cafe_portrait",
    },
    {
        "prompt": "street photography, tokyo at night, neon signs, rain reflection, cinematic",
        "negative": "cartoon, anime, bright, overexposed",
        "alias": "tokyo_night",
    },
    {
        "prompt": "landscape, mountain lake, sunrise, fog, dramatic sky, wide angle",
        "negative": "people, text, watermark, cartoon",
        "alias": "mountain_lake",
    },
    {
        "prompt": "close-up portrait, elderly man, wrinkles, warm smile, golden hour, shallow depth of field",
        "negative": "cartoon, anime, young, smooth skin, painting",
        "alias": "elderly_portrait",
    },
    {
        "prompt": "food photography, ramen bowl, steam, chopsticks, overhead shot, warm lighting",
        "negative": "cartoon, anime, ugly, blurry",
        "alias": "ramen",
    },
    {
        "prompt": "architecture, modern building, glass facade, blue sky, geometric, minimalist",
        "negative": "people, cartoon, cluttered",
        "alias": "architecture",
    },
    {
        "prompt": "cat sitting on windowsill, afternoon sunlight, dust particles, cozy, shallow dof",
        "negative": "cartoon, anime, drawing, painting",
        "alias": "cat_window",
    },
    {
        "prompt": "fashion portrait, woman in black dress, studio lighting, high contrast, editorial",
        "negative": "cartoon, anime, casual, ugly",
        "alias": "fashion",
    },
]

SEED = 42


async def generate(client, idx, total, model_info, prompt_info):
    model = model_info["name"]
    payload = {
        "prompt": prompt_info["prompt"],
        "negative_prompt": prompt_info["negative"],
        "width": 1024,
        "height": 1024,
        "steps": model_info["steps"],
        "guidance_scale": model_info["guidance"],
        "seed": SEED,
        "model": model,
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{model}_{prompt_info['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{total}] OK [{model}] {prompt_info['alias']}")
            return True
        else:
            print(f"[{idx:02d}/{total}] FAIL [{model}] {prompt_info['alias']}: {data.get('error', '?')}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{total}] ERROR [{model}] {prompt_info['alias']}: {e}")
        return False


async def main():
    jobs = []
    for model_info in MODELS:
        for prompt_info in PROMPTS:
            jobs.append((model_info, prompt_info))

    total = len(jobs)
    ok = fail = 0

    print(f"실사 모델 비교 테스트 {total}장")
    print(f"모델 {len(MODELS)}개 x 프롬프트 {len(PROMPTS)}개")
    print(f"시드 고정: {SEED} (모델간 비교용)")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)
    for m in MODELS:
        print(f"  - {m['name']} (steps: {m['steps']}, guidance: {m['guidance']})")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, (model_info, prompt_info) in enumerate(jobs, 1):
            if await generate(client, i, total, model_info, prompt_info):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.5)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
