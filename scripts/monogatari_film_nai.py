"""모노가타리 시리즈 - 필름카메라 감성 NAI v4 full"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_film"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTERS = [
    {"label": "hitagi", "tags": "senjougahara hitagi, long purple hair, purple eyes, slender"},
    {"label": "sodachi_twin", "tags": "oikura sodachi, light brown hair, twin tails, green eyes"},
    {"label": "sodachi_short", "tags": "oikura sodachi, short light brown hair, green eyes, gentle"},
    {"label": "mayoi", "tags": "hachikuji mayoi, long black hair, twin tails, red eyes"},
    {"label": "suruga", "tags": "kanbaru suruga, short dark blue hair, brown eyes, athletic, tan skin"},
    {"label": "nadeko", "tags": "sengoku nadeko, long orange hair, bangs covering eyes, shy"},
    {"label": "tsubasa_long", "tags": "hanekawa tsubasa, long black hair, braids, calm expression"},
    {"label": "tsubasa_short", "tags": "hanekawa tsubasa, short white hair, golden eyes, cat ears"},
    {"label": "shinobu", "tags": "oshino shinobu, long blonde hair, golden eyes, vampire, pointy ears"},
    {"label": "karen", "tags": "araragi karen, long black hair, ponytail, tall, energetic"},
    {"label": "tsukihi", "tags": "araragi tsukihi, short black hair, calm"},
    {"label": "yotsugi", "tags": "ononoki yotsugi, teal hair, hat, expressionless, deadpan"},
    {"label": "ougi", "tags": "oshino ougi, short black hair, dark eyes, pale skin, mysterious"},
    {"label": "gaen", "tags": "gaen izuko, short grey hair, mature, confident"},
]

FILM_COMMON = "film grain, analog photo, 35mm film, soft focus, light leak, warm tones, vintage, nostalgic, natural lighting"

SCENES = [
    "sitting by window, afternoon sun, curtain blowing, golden hour, cafe, coffee cup",
    "walking down street, sunset, long shadows, power lines, residential area, summer evening",
    "lying on grass, looking up at sky, dappled sunlight, park, lazy afternoon",
    "standing at train platform, waiting, wind, hair blowing, cloudy day, melancholic",
    "leaning on bridge railing, river below, autumn leaves, overcast, contemplative",
    "sitting on school stairs, after school, orange sky through window, lonely",
    "reading book under tree, shade, summer, peaceful, gentle breeze",
    "standing in rain, no umbrella, wet hair, street lights, evening, emotional",
    "looking out bus window, rainy day, condensation on glass, reflection, pensive",
    "sitting on swing, empty playground, dusk, silhouette, bittersweet",
    "buying drink from vending machine, night, soft glow, quiet street, alone",
    "walking through torii gates, shrine, morning mist, peaceful, sacred",
    "eating ice cream, summer festival, yukata, lanterns, warm evening light",
    "lying on tatami, fan spinning above, lazy summer, indoor, relaxed",
    "standing at crosswalk, city, traffic lights, crowd, isolated feeling",
    "sitting on rooftop, legs dangling, city skyline, golden hour, wind",
    "bicycle, riding through rice fields, countryside, summer clouds, freedom",
    "phone booth, night, fluorescent light, rain outside, calling someone",
    "flower field, reaching out hand, backlit, lens flare, dreamy",
    "school hallway, empty, sunset light through windows, dust particles, still",
    "beach, barefoot, water touching feet, low angle, summer, serene",
    "convenience store parking lot, night, fluorescent light spill, eating onigiri",
    "old bookstore, dusty shelves, warm lamp light, browsing, cozy",
    "laundromat, waiting, watching clothes spin, late night, neon sign outside",
    "temple steps, morning, dew on leaves, quiet, spiritual",
    "holding sparkler, summer night, face lit by warm glow, close up",
    "sleeping on desk, classroom, afternoon light, peaceful face, quiet",
    "standing in doorway, backlit, silhouette, mysterious, entering room",
    "umbrella, cherry blossom petals falling, spring rain, gentle smile",
    "night market, crowd, colorful stalls, eating takoyaki, lively but intimate",
]

random.seed(2026)

JOBS = []

shuffled_scenes = list(SCENES)

for char in CHARACTERS:
    random.shuffle(shuffled_scenes)
    for i in range(5):
        scene = shuffled_scenes[i]
        JOBS.append({
            "prompt": f"1girl, {char['tags']}, {scene}, {FILM_COMMON}",
            "name": f"{char['label']}_{i:02d}",
        })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece, best quality",
        "negative_prompt": "low quality, worst quality, bad anatomy, blurry, digital art, clean lines, sharp, oversaturated, neon, vibrant, text, watermark",
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
    print(f"모노가타리 × 필름카메라 감성 - NAI full {TOTAL}장")
    print(f"  캐릭터: {len(CHARACTERS)}명 × 5장씩")
    print(f"  씬: {len(SCENES)}종")
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
