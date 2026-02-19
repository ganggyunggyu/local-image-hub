"""Animagine XL 4.0 전체 프리셋 200장"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_animagine_all_200"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTERS = [
    "1girl, long black hair, brown eyes, school uniform",
    "1girl, short pink hair, blue eyes, hoodie",
    "1girl, silver twin tails, red eyes, gothic dress",
    "1girl, blonde hair, green eyes, white dress, ribbon",
    "1girl, blue hair, golden eyes, kimono",
    "1boy, black hair, dark eyes, school uniform",
    "1boy, silver hair, golden eyes, red kimono, dog ears",
    "1girl, red hair, ponytail, sporty outfit",
    "1girl, purple hair, bob cut, mysterious, dark dress",
    "1girl, green hair, heterochromia, maid outfit",
]

POSES = [
    "gentle smile, looking at viewer, upper body",
    "sitting, peaceful, soft lighting",
    "wind in hair, looking at sky, melancholic",
    "laughing, energetic, dynamic pose",
    "blushing, shy, looking away",
    "cool expression, arms crossed, confident",
    "action pose, dramatic, intense eyes",
    "reading book, cozy, warm lighting",
    "running, hair flowing, joyful",
    "leaning on window, rainy day, contemplative",
    "standing in field, sunset, peaceful",
    "close up face, expressive eyes, detailed",
    "back view, looking over shoulder, elegant",
    "sitting on rooftop, night sky, stars",
    "dancing, graceful, flowing clothes",
    "holding umbrella, rain, atmospheric",
    "playing guitar, music, passionate",
    "drinking tea, cafe, relaxed",
    "stretching, morning light, sleepy",
    "walking, cherry blossoms, spring",
]

STYLES = [
    "pale_aqua", "mono_halftone", "chibi_sketch", "cozy_gouache",
    "watercolor_sketch", "kyoto_animation", "ufotable", "shinkai",
    "ghibli", "trigger", "mappa", "shaft", "monogatari",
    "genshin", "blue_archive", "arknights", "fate",
    "cyberpunk", "pastel_soft", "inuyasha",
    "sepia_backlit", "mono_accent", "sketch_colorpop", "pop_fanart",
    "split_sketch", "waterful", "bold_pop", "retro_glitch",
    "gyaru_peace", "double_peace", "heart_hands",
    "finger_gun", "cat_paw", "thumbs_up",
]

JOBS = []
random.seed(42)

for i in range(200):
    style = STYLES[i % len(STYLES)]
    char = random.choice(CHARACTERS)
    pose = random.choice(POSES)
    JOBS.append({
        "style": style,
        "char": char,
        "pose": pose,
        "name": f"{i:03d}_{style}",
    })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['char']}, {job['pose']}, masterpiece, best quality",
        "negative_prompt": "low quality, worst quality, bad anatomy, bad hands",
        "width": 832,
        "height": 1216,
        "steps": 28,
        "guidance_scale": 7.0,
        "provider": "local",
        "model": "animagine-xl-4",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=300.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{num:03d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{num:03d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:60]}")
            return False
    except Exception as e:
        print(f"[{num:03d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"Animagine XL 4.0 전체 프리셋 200장")
    print(f"스타일: {len(STYLES)}종 / 캐릭터: {len(CHARACTERS)}종 / 포즈: {len(POSES)}종")
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
