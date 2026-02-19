"""V4.5 Curated vs V4.5 Full 비교 - 전체 프리셋"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")

CHAR_BASE = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes"

JOBS = [
    {"style": "pale_aqua", "pose": "smile, looking at viewer, upper body"},
    {"style": "mono_halftone", "pose": "smirk, looking at viewer, upper body"},
    {"style": "chibi_sketch", "pose": "happy, full body, jumping"},
    {"style": "cozy_gouache", "pose": "reading book, sitting, cozy"},
    {"style": "watercolor_sketch", "pose": "gentle smile, wind, hair flowing"},
    {"style": "kyoto_animation", "pose": "school uniform, classroom, window"},
    {"style": "ufotable", "pose": "action pose, dramatic, magic"},
    {"style": "shinkai", "pose": "looking at sky, sunset, wind"},
    {"style": "ghibli", "pose": "nature, peaceful, walking"},
    {"style": "trigger", "pose": "dynamic pose, energetic, action"},
    {"style": "mappa", "pose": "intense, dramatic lighting, cool"},
    {"style": "shaft", "pose": "head tilt, mysterious, artistic"},
    {"style": "monogatari", "pose": "head tilt, elegant, looking at viewer"},
    {"style": "genshin", "pose": "fantasy outfit, magic, glowing"},
    {"style": "blue_archive", "pose": "school uniform, halo, cheerful"},
    {"style": "arknights", "pose": "tactical, cool, industrial"},
    {"style": "fate", "pose": "elegant dress, noble, dramatic"},
    {"style": "cyberpunk", "pose": "neon, night city, futuristic"},
    {"style": "pastel_soft", "pose": "gentle, dreamy, flowers"},
    {"style": "inuyasha", "pose": "feudal japan, wind, nostalgic"},
    {"style": "sepia_backlit", "pose": "backlit, sunset, dreamy"},
    {"style": "mono_accent", "pose": "stylish, cool, limited color"},
    {"style": "sketch_colorpop", "pose": "sketch, color accent, artistic"},
    {"style": "pop_fanart", "pose": "cute, blush, looking at viewer"},
    {"style": "gyaru_peace", "pose": "gyaru peace, v sign, wink, cheerful"},
    {"style": "double_peace", "pose": "double peace sign, both hands, energetic"},
    {"style": "ura_peace", "pose": "peace sign, back of hand showing, cool"},
    {"style": "face_peace", "pose": "peace sign near face, cute"},
    {"style": "cheek_peace", "pose": "peace sign on cheek, adorable"},
    {"style": "heart_hands", "pose": "heart hands, finger heart, lovely"},
    {"style": "cheek_heart", "pose": "heart on cheek, cute pose"},
    {"style": "finger_gun", "pose": "finger gun, pointing, confident"},
    {"style": "cat_paw", "pose": "cat pose, paw hands, playful, nya"},
    {"style": "thumbs_up", "pose": "thumbs up, encouraging, bright"},
    {"style": "hand_wave", "pose": "waving hand, greeting, friendly"},
    {"style": "split_sketch", "pose": "close up face, expressive eyes"},
    {"style": "waterful", "pose": "serene, flowers, soft lighting"},
    {"style": "bold_pop", "pose": "confident, stylish, bold expression"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job, model, output_dir, seed):
    style = job["style"]
    pose = job["pose"]
    payload = {
        "prompt": f"{CHAR_BASE}, {pose}, masterpiece",
        "negative_prompt": "low quality, worst quality",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "seed": seed,
        "provider": "nai",
        "model": model,
        "style": style,
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            actual_seed = data.get("seed", seed)
            fp = output_dir / f"{idx:02d}_{style}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            return True, actual_seed
        else:
            print(f"[{idx:02d}] FAIL {style}: {data.get('error', '?')[:40]}")
            return False, seed
    except Exception as e:
        print(f"[{idx:02d}] ERROR {style}: {e}")
        return False, seed


async def main():
    import random

    # 동일 시드로 비교
    base_seed = random.randint(0, 2147483647)

    curated_dir = Path(__file__).parent.parent / "outputs" / f"{TODAY}_v45_curated"
    full_dir = Path(__file__).parent.parent / "outputs" / f"{TODAY}_v45_full"
    curated_dir.mkdir(parents=True, exist_ok=True)
    full_dir.mkdir(parents=True, exist_ok=True)

    print(f"V4.5 Curated vs Full 비교 (각 {TOTAL}장)")
    print(f"동일 시드: {base_seed}")
    print(f"Curated: {curated_dir}")
    print(f"Full: {full_dir}")
    print("=" * 60)

    curated_ok = curated_fail = 0
    full_ok = full_fail = 0

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            seed = base_seed + i

            # Curated
            success, _ = await generate(client, i, job, "nai-v4.5", curated_dir, seed)
            if success:
                curated_ok += 1
            else:
                curated_fail += 1

            # Full
            success, _ = await generate(client, i, job, "nai-v4.5-full", full_dir, seed)
            if success:
                full_ok += 1
            else:
                full_fail += 1

            print(f"[{i:02d}/{TOTAL}] {job['style']} done")
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"Curated: 성공 {curated_ok}, 실패 {curated_fail}")
    print(f"Full: 성공 {full_ok}, 실패 {full_fail}")


if __name__ == "__main__":
    asyncio.run(main())
