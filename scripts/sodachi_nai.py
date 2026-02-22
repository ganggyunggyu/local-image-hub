"""오이쿠라 소다치 - 양갈래/단발 100장 - NAI × monogatari 프리셋"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_sodachi_nai"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TWIN = "1girl, oikura sodachi, light brown hair, twin tails, sharp eyes, angry expression, school uniform, owarimonogatari"
SHORT = "1girl, oikura sodachi, short hair, light brown hair, sad expression, gentle, casual clothes, sodachi lost"

POSES = [
    "head tilt, looking at viewer, sharp gaze, upper body",
    "head tilt, arms crossed, angry, confrontational",
    "close up face, tears, emotional, crying, beautiful",
    "shouting, pointing, angry, dramatic, intense",
    "looking away, melancholic, window light, lonely",
    "sitting alone, classroom, empty desks, after school",
    "standing in hallway, school, dramatic shadow",
    "profile view, wind, hair blowing, contemplative",
    "hands clenched, frustrated, trembling, emotional",
    "gentle smile, rare, soft lighting, peaceful",
    "reading book, focused, library, quiet",
    "leaning on desk, bored, classroom, afternoon sun",
    "running, corridor, hair flowing, dynamic",
    "back view, walking away, lonely, rain",
    "standing at door, hesitant, looking down, shy",
    "sitting on stairs, hugging knees, vulnerable",
    "looking up at sky, rooftop, clouds, wistful",
    "close up eyes, detailed iris, tears welling up",
    "hand reaching out, desperate, emotional, dramatic light",
    "standing in rain, wet hair, no umbrella, sad",
    "fist on chest, determined, serious expression",
    "laughing, genuine, surprised by own laughter",
    "writing on blackboard, math equations, chalk, focused",
    "holding phone, looking at screen, conflicted",
    "night, street light, standing alone, atmospheric",
    "scarf, winter, cold breath, snowy, melancholic",
    "sitting by window, cafe, rain outside, thoughtful",
    "confronting someone, pointing finger, fierce eyes",
    "lying on bed, staring at ceiling, empty expression",
    "sunrise, rooftop, new beginning, hopeful, wind",
    "eating alone, lunchbox, bench, peaceful moment",
    "umbrella, walking, puddles, reflections, moody",
    "close up hands, clenched, trembling, emotion",
    "leaning on railing, bridge, river below, sunset",
    "piano, playing, eyes closed, serene, music room",
    "standing at crosswalk, city, traffic lights, thinking",
    "jacket over shoulders, casual, walking home, dusk",
    "sitting in park, autumn leaves, bench, quiet",
    "hair clip adjusting, mirror, getting ready, morning",
    "watching sunset, silhouette, beautiful sky, peaceful",
    "crouching, hugging self, dark room, vulnerable",
    "looking at old photo, nostalgic, bittersweet smile",
    "standing in doorway, backlit, dramatic, mysterious",
    "chin on hand, desk, daydreaming, soft light",
    "standing in snow, white world, peaceful, breath visible",
    "arguing, expressive, hand gestures, passionate",
    "apologetic, looking down, hands together, sorry",
    "surprised, wide eyes, blush, caught off guard",
    "sleeping at desk, peaceful face, afternoon sun",
    "determined walk, forward, strong posture, confident",
]

JOBS = []
random.seed(314)

for i in range(100):
    if i % 2 == 0:
        tags = TWIN
        label = "twin"
    else:
        tags = SHORT
        label = "short"
    pose = POSES[i % len(POSES)]
    JOBS.append({
        "tags": tags,
        "pose": pose,
        "name": f"{i:03d}_{label}",
    })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['tags']}, {job['pose']}, masterpiece, best quality",
        "negative_prompt": "low quality, worst quality, bad anatomy, bad hands",
        "width": 832,
        "height": 1216,
        "provider": "nai",
        "model": "nai-diffusion-4-curated-preview",
        "style": "monogatari",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=120.0)
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
    twin_count = sum(1 for j in JOBS if "twin" in j["name"])
    short_count = sum(1 for j in JOBS if "short" in j["name"])

    print(f"오이쿠라 소다치 × monogatari 프리셋 - NAI {TOTAL}장")
    print(f"  양갈래: {twin_count}장 / 단발: {short_count}장")
    print(f"  포즈: {len(POSES)}종")
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
