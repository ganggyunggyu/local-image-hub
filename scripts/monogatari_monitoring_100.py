"""모노가타리 3인 - 모니터링 피쉬아이 100장 NAI v4 full"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_monitoring_100v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SODACHI = "oikura sodachi, light brown hair, twin tails, sharp eyes, green eyes"
HITAGI = "senjougahara hitagi, long purple hair, sharp eyes, cold beauty, slender"
MAYOI = "hachikuji mayoi, long black hair, twin tails, red eyes"
TSUBASA_LONG = "hanekawa tsubasa, long black hair, braids, calm expression"
TSUBASA_SHORT = "hanekawa tsubasa, short white hair, golden eyes, cat ears, black hanekawa"

COMMON = "fisheye, wide-angle lens, looking at viewer, reaching toward viewer, spread fingers, foreshortening, perspective, pov"

POSES = [
    "from below, crop top, shorts, flip flops, night city background, smirk, confident",
    "from above, looking up, school uniform, classroom, hand up toward camera, desperate expression",
    "from below, casual hoodie, leaning forward, both hands toward camera, convenience store night",
    "from above, lying down, reaching up toward camera, hair spread out, indoor, soft lighting",
    "from below, jacket, standing, one hand on camera, angry expression, dramatic lighting, hallway",
    "from below, white blouse, skirt, one hand reaching camera, sharp gaze, night street",
    "from above, looking up at camera, cardigan, sitting on floor, hand raised, cold expression",
    "from below, long coat, leaning forward toward camera, mysterious smile, night, streetlight",
    "from above, lying on bed, reaching up, hair spread, white shirt, soft lighting",
    "from below, casual dress, both hands forward, playful smirk, alley night",
    "from below, sundress, both hands reaching camera, cheerful, playful smile, daytime street",
    "from above, hoodie, sitting on ground, curious expression, hand reaching up, park",
    "from below, t-shirt, skirt, jumping toward camera, joyful, energetic, shopping district",
    "from above, school uniform, crouching, looking up at camera, mischievous smile, alley",
    "from below, casual outfit, one hand on camera, winking, playful, evening street, lanterns",
    "from below, summer dress, rooftop, city skyline night, wind, hair flowing, reaching out",
    "from above, pajamas, bedroom, lying on back, one hand toward camera, sleepy, warm light",
    "from below, sports bra, gym shorts, gym, sweaty, determined, fist toward camera",
    "from above, kimono, tatami room, sitting seiza, looking up, elegant, paper lantern",
    "from below, raincoat, rain, umbrella in one hand, other hand toward camera, puddle reflections",
    "from above, oversized sweater, knees to chest, looking up, vulnerable, dim room",
    "from below, tank top, denim shorts, festival, fireworks background, sparklers, excited",
    "from above, apron, kitchen, flour on cheek, holding whisk, looking up, surprised",
    "from below, leather jacket, motorcycle, night highway, cool, confident, neon lights",
    "from above, bath towel, onsen, steam, looking up embarrassed, blush, hand covering",
    "from below, cheerleader outfit, pom poms, stadium, energetic, jumping, bright",
    "from above, reading glasses, book in hand, library, looking up from book, curious",
    "from below, winter coat, scarf, snowy street, breath visible, cold night, warm lights",
    "from above, swimsuit, pool, floating, looking up, summer, reflections, relaxed",
    "from below, waitress uniform, cafe, tray in hand, welcoming smile, cozy interior",
    "from below, detective coat, magnifying glass, dark alley, suspicious, dramatic shadow",
    "from above, cat ears headband, maid outfit, looking up, playful, paw pose",
    "from below, office shirt, tie loose, rooftop, sunset, wind, exhausted but smiling",
    "from above, painting canvas, art room, paint smudges on face, looking up, creative",
]

CHARS = [
    {"tags": SODACHI, "label": "sodachi"},
    {"tags": HITAGI, "label": "hitagi"},
    {"tags": MAYOI, "label": "mayoi"},
    {"tags": TSUBASA_LONG, "label": "tsubasa_long"},
    {"tags": TSUBASA_SHORT, "label": "tsubasa_short"},
]

random.seed(42)

JOBS = []

for char in CHARS:
    shuffled_poses = random.sample(POSES, len(POSES))
    for i in range(20):
        pose = shuffled_poses[i % len(POSES)]
        JOBS.append({
            "prompt": f"{COMMON}, {pose}, 1girl, {char['tags']}",
            "name": f"{char['label']}_{i:03d}",
        })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece, best quality, vibrant neon colors, detailed urban background, anime illustration",
        "negative_prompt": "low quality, worst quality, bad anatomy, bad hands, blurry, extra fingers, flat angle, normal perspective, straight-on, no distortion",
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
    counts = {}
    for j in JOBS:
        label = j["name"].rsplit("_", 1)[0]
        counts[label] = counts.get(label, 0) + 1

    print(f"모노가타리 모니터링 피쉬아이 - NAI full {TOTAL}장")
    for k, v in counts.items():
        print(f"  {k}: {v}장")
    print(f"포즈: {len(POSES)}종")
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
