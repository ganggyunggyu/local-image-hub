"""냥냥돌쇠 + 모노가타리 시리즈 캐릭터 200장 - 다양한 프리셋"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_monogatari_200"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTERS = {
    "dolsoe": {
        "tags": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes, facial mole, multiple moles, mole under eye, mole on neck",
        "neg": "moles on body, mole on forehead, mole on nose",
    },
    "senjougahara": {
        "tags": "1girl, senjougahara hitagi, long purple hair, sharp eyes, cold expression, school uniform",
        "neg": "",
    },
    "hanekawa": {
        "tags": "1girl, hanekawa tsubasa, long black hair, glasses, gentle expression, school uniform",
        "neg": "",
    },
    "shinobu": {
        "tags": "1girl, oshino shinobu, blonde hair, long hair, golden eyes, white dress, vampire",
        "neg": "",
    },
    "nadeko": {
        "tags": "1girl, sengoku nadeko, short orange hair, bangs covering eyes, shy, school uniform",
        "neg": "",
    },
    "kanbaru": {
        "tags": "1girl, kanbaru suruga, short dark hair, sporty, athletic, energetic, tomboyish",
        "neg": "",
    },
    "hachikuji": {
        "tags": "1girl, hachikuji mayoi, twin tails, brown hair, backpack, cheerful, young girl",
        "neg": "",
    },
    "kaiki": {
        "tags": "1man, kaiki deishuu, black suit, dark hair, stubble, tired expression, middle aged",
        "neg": "",
    },
    "araragi": {
        "tags": "1boy, araragi koyomi, short black hair, school uniform, messy hair, casual",
        "neg": "",
    },
    "yotsugi": {
        "tags": "1girl, ononoki yotsugi, short green hair, orange hat, expressionless, peace sign, flat chest",
        "neg": "",
    },
    "sodachi": {
        "tags": "1girl, oikura sodachi, long light brown hair, hair over one eye, sad expression, school uniform",
        "neg": "",
    },
    "gaen": {
        "tags": "1woman, gaen izuko, short dark hair, confident smile, business suit, mature",
        "neg": "",
    },
    "black_hanekawa": {
        "tags": "1girl, black hanekawa, long white hair, cat ears, golden eyes, seductive, playful",
        "neg": "",
    },
    "kiss_shot": {
        "tags": "1girl, kiss-shot acerola-orion heart-under-blade, very long blonde hair, red eyes, regal, elegant dress, vampire queen",
        "neg": "",
    },
}

STYLES = [
    "monogatari", "shaft", "pale_aqua", "mono_halftone",
    "watercolor_sketch", "pastel_soft", "sepia_backlit", "mono_accent",
    "sketch_colorpop", "pop_fanart", "cozy_gouache", "split_sketch",
    "waterful", "retro_glitch", "kyoto_animation", "inuyasha",
    "cyberpunk", "chibi_sketch", "mappa", "ufotable",
    "ghibli", "trigger", "genshin", "fate",
]

POSES = [
    "head tilt, looking at viewer, mysterious smile, upper body",
    "head tilt, side glance, enigmatic, close up face",
    "gentle smile, soft lighting, upper body",
    "arms crossed, cool expression, confident",
    "blushing, looking away, shy",
    "laughing, hand near mouth, joyful",
    "melancholic, wind in hair, looking at distance",
    "reading book, sitting, cozy, warm lighting",
    "walking, cherry blossoms, spring, peaceful",
    "sitting on bench, park, autumn leaves",
    "standing in rain, umbrella, moody atmosphere",
    "rooftop, sunset sky, dramatic clouds",
    "leaning on railing, night city, lights",
    "drinking tea, cafe, relaxed, afternoon",
    "back view, looking over shoulder, elegant",
    "close up eyes, detailed iris, beautiful",
    "action pose, dynamic, speed lines",
    "sleeping, peaceful, soft blanket, warm",
    "standing under sakura, petals, dreamy",
    "staircase, dramatic lighting, geometric shadow",
]

JOBS = []
random.seed(42)

char_keys = list(CHARACTERS.keys())

for i in range(200):
    char_key = char_keys[i % len(char_keys)]
    char = CHARACTERS[char_key]
    style = random.choice(STYLES)
    pose = random.choice(POSES)
    JOBS.append({
        "char_key": char_key,
        "tags": char["tags"],
        "neg": char["neg"],
        "style": style,
        "pose": pose,
        "name": f"{i:03d}_{char_key}_{style}",
    })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    neg_parts = ["low quality, worst quality, bad anatomy, bad hands"]
    if job["neg"]:
        neg_parts.append(job["neg"])

    payload = {
        "prompt": f"{job['tags']}, {job['pose']}, masterpiece, best quality",
        "negative_prompt": ", ".join(neg_parts),
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

    char_count = {}
    style_count = {}
    for j in JOBS:
        char_count[j["char_key"]] = char_count.get(j["char_key"], 0) + 1
        style_count[j["style"]] = style_count.get(j["style"], 0) + 1

    print(f"냥냥돌쇠 + 모노가타리 시리즈 200장")
    print(f"\n캐릭터 ({len(char_count)}명):")
    for c, n in sorted(char_count.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}장")
    print(f"\n스타일 ({len(style_count)}종):")
    for s, n in sorted(style_count.items(), key=lambda x: -x[1]):
        print(f"  {s}: {n}장")
    print(f"\n저장: {OUTPUT_DIR}")
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
