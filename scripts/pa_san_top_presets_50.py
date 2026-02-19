"""봇치더락 PA상 50장 - NAI 잘 뽑히는 프리셋 5종"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pa_san_top_presets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PA = "pa-san, bocchi the rock!, black hair, green eyes, labret piercing, ear piercing, mature woman, ponytail"

# 잘 뽑히는 프리셋 5종
TOP_PRESETS = ["monogatari", "blue_archive", "kyoto_animation", "chibi_sketch", "mono_halftone"]

# 다양한 상황/포즈 (10종 x 5프리셋 = 50장)
SCENES = [
    "mixing console, live house, focused expression, professional, upper body",
    "backstage, preparing equipment, serious, cool, upper body",
    "soundcheck, stage empty, testing microphone, concentrated, full body",
    "ticket booth, night, smiling at customer, friendly, upper body",
    "staff room, break time, relaxed, sitting, casual clothes",
    "rooftop, sunset, looking at city, peaceful, wind, upper body",
    "corridor, walking with clipboard, busy, professional, full body",
    "storage room, organizing equipment, focused, cool lighting",
    "office desk, paperwork, tired but determined, upper body",
    "stage wings, watching band perform, proud smile, emotional, upper body",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy"

JOBS = []
for preset_idx, preset in enumerate(TOP_PRESETS):
    for scene_idx, scene in enumerate(SCENES):
        job_idx = preset_idx * len(SCENES) + scene_idx + 1
        JOBS.append({
            "prompt": f"1girl, {PA}, {scene}",
            "style": preset,
            "name": f"pa_{job_idx:02d}_{preset}_{scene_idx+1}",
        })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, idx: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece",
        "negative_prompt": NEGATIVE,
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=240.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['name']} ({job['style']})", flush=True)
            return True
        print(f"[{idx:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:50]}", flush=True)
        return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['name']}: {e}", flush=True)
        return False


async def main() -> None:
    ok = fail = 0
    print(f"PA상 {TOTAL}장 생성 - NAI 잘 뽑히는 프리셋 5종", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)
    print("=" * 60, flush=True)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60, flush=True)
    print(f"완료! 성공: {ok}, 실패: {fail}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
