"""
센죠가하라 히타기 - 다양한 프리셋 테스트
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_hitagi_presets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTER = "1girl, senjougahara hitagi, purple hair, sharp eyes"

JOBS = [
    {"style": "monogatari", "scene": "head tilt, school uniform", "alias": "monogatari_classroom"},
    {"style": "monogatari", "scene": "sitting, night sky", "alias": "monogatari_night"},
    {"style": "shaft", "scene": "school uniform, dramatic pose", "alias": "shaft_dramatic"},
    {"style": "shaft", "scene": "head tilt, smirk", "alias": "shaft_headtilt"},
    {"style": "kyoto_animation", "scene": "cafe, coffee cup", "alias": "kyoani_cafe"},
    {"style": "kyoto_animation", "scene": "cherry blossoms, wind", "alias": "kyoani_sakura"},
    {"style": "shinkai", "scene": "sunset, rooftop", "alias": "shinkai_sunset"},
    {"style": "shinkai", "scene": "rain, umbrella", "alias": "shinkai_rain"},
    {"style": "watercolor_sketch", "scene": "standing, looking away", "alias": "watercolor_melancholy"},
    {"style": "watercolor_sketch", "scene": "sitting by window", "alias": "watercolor_window"},
    {"style": "cozy_gouache", "scene": "reading book", "alias": "gouache_reading"},
    {"style": "sepia_backlit", "scene": "backlit, hair flowing", "alias": "sepia_backlit"},
    {"style": "mono_accent", "scene": "sharp gaze, close-up", "alias": "mono_intense"},
    {"style": "sketch_colorpop", "scene": "walking, school bag", "alias": "sketch_walking"},
    {"style": "pastel_soft", "scene": "smile, flower field", "alias": "pastel_flower"},
    {"style": "cyberpunk", "scene": "neon lights, night", "alias": "cyberpunk_neon"},
    {"style": "mappa", "scene": "wind, intense expression", "alias": "mappa_dramatic"},
    {"style": "ufotable", "scene": "dynamic pose, glowing", "alias": "ufotable_action"},
    {"style": "ghibli", "scene": "walking in forest", "alias": "ghibli_forest"},
    {"style": "inuyasha", "scene": "moonlight, kimono", "alias": "inuyasha_moon"},
    {"style": "gyaru_peace", "scene": "v sign, peace sign, wink", "alias": "gyaru_peace"},
    {"style": "heart_hands", "scene": "heart hands, finger heart", "alias": "heart_hands"},
    {"style": "finger_gun", "scene": "finger gun, smirk", "alias": "finger_gun"},
    {"style": "cat_paw", "scene": "cat paw pose, playful", "alias": "cat_paw"},
]

NEGATIVE = "lowres, bad anatomy, error, text, extra fingers, fused fingers, bad hands"

TOTAL = len(JOBS)


async def generate(client, idx, job):
    prompt = f"{CHARACTER}, {job['scene']}"

    payload = {
        "prompt": prompt,
        "negative_prompt": NEGATIVE,
        "width": 832,
        "height": 1216,
        "style": job["style"],
        "model": "animagine-xl-4",
        "lora": "ClearHandsXL-v2.safetensors",
        "lora_scale": 2.0,
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=300.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"hitagi_{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK [{job['style']}] {job['alias']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL [{job['style']}]: {data.get('error', '?')}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR [{job['style']}]: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"센죠가하라 히타기 프리셋 테스트 {TOTAL}장")
    print(f"스타일 프리셋 + ClearHandsXL LoRA (scale: 2.0)")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)
    for job in JOBS:
        print(f"  - [{job['style']}] {job['alias']}")
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
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
