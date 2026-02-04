"""
전체 프리셋 랜덤 50장 배치
- SFW 프리셋만 사용
- 손가락 네거티브 강화
"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_random_batch"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PRESETS = [
    "cozy_gouache",
    "watercolor_sketch",
    "kyoto_animation",
    "ufotable",
    "shinkai",
    "ghibli",
    "trigger",
    "mappa",
    "shaft",
    "monogatari",
    "genshin",
    "blue_archive",
    "arknights",
    "fate",
    "cyberpunk",
    "pastel_soft",
    "inuyasha",
    "sepia_backlit",
    "mono_accent",
    "sketch_colorpop",
]

CHARACTERS = [
    {
        "tags": "1girl, reze, chainsaw man, purple hair, short hair, red eyes",
        "alias": "reze",
    },
    {
        "tags": "1girl, makima, chainsaw man, orange hair, braided ponytail, yellow eyes",
        "alias": "makima",
    },
    {
        "tags": "1girl, power, chainsaw man, blonde hair, red horns, red eyes",
        "alias": "power",
    },
    {
        "tags": "1girl, hiroi kikuri, bocchi the rock!, purple hair, long hair, red eyes, mature",
        "alias": "kikuri",
    },
    {
        "tags": "1girl, gotoh hitori, bocchi the rock!, pink hair, blue eyes, shy",
        "alias": "bocchi",
    },
    {
        "tags": "1girl, kita ikuyo, bocchi the rock!, red hair, green eyes",
        "alias": "kita",
    },
    {
        "tags": "1girl, senjougahara hitagi, bakemonogatari, purple hair, sharp eyes",
        "alias": "hitagi",
    },
    {
        "tags": "1girl, oshino shinobu, bakemonogatari, blonde hair, yellow eyes, vampire",
        "alias": "shinobu",
    },
    {
        "tags": "1girl, osaki nana, nana, black hair, short hair, punk",
        "alias": "nana_o",
    },
    {
        "tags": "1girl, komatsu nana, nana, brown hair, long hair, brown eyes, cute",
        "alias": "hachi",
    },
    {
        "tags": "1girl, hirasawa yui, k-on!, brown hair, short hair, hairpin",
        "alias": "yui",
    },
    {
        "tags": "1girl, akiyama mio, k-on!, black hair, long hair, grey eyes",
        "alias": "mio",
    },
    {
        "tags": "1girl, shinku, rozen maiden, blonde hair, twintails, red eyes, gothic lolita",
        "alias": "shinku",
    },
    {
        "tags": "1girl, frieren, sousou no frieren, white hair, elf ears, mage",
        "alias": "frieren",
    },
    {
        "tags": "1girl, ayanami rei, neon genesis evangelion, blue hair, short hair, red eyes",
        "alias": "rei",
    },
    {
        "tags": "1girl, souryuu asuka langley, neon genesis evangelion, red hair, blue eyes",
        "alias": "asuka",
    },
    {
        "tags": "1girl, tsukino usagi, sailor moon, blonde hair, twintails, blue eyes, tiara",
        "alias": "usagi",
    },
    {
        "tags": "1girl, tohsaka rin, fate stay night, black hair, twintails, aqua eyes",
        "alias": "rin",
    },
    {
        "tags": "1girl, saber, fate stay night, blonde hair, green eyes, ahoge, armor",
        "alias": "saber",
    },
    {
        "tags": "1girl, suzumiya haruhi, suzumiya haruhi no yuuutsu, brown hair, hair ribbon",
        "alias": "haruhi",
    },
    {
        "tags": "1girl, shana, shakugan no shana, red hair, long hair, red eyes, flame",
        "alias": "shana",
    },
    {
        "tags": "1girl, akemi homura, mahou shoujo madoka magica, black hair, purple eyes, hairband",
        "alias": "homura",
    },
    {
        "tags": "1girl, rem, re:zero, blue hair, blue eyes, maid, x hair ornament",
        "alias": "rem",
    },
    {
        "tags": "1girl, zero two, darling in the franxx, pink hair, green eyes, horns",
        "alias": "zero_two",
    },
    {
        "tags": "1girl, megumin, konosuba, brown hair, red eyes, witch hat, eyepatch",
        "alias": "megumin",
    },
    {
        "tags": "1girl, yor briar, spy x family, black hair, red eyes, earrings, elegant",
        "alias": "yor",
    },
    {
        "tags": "1girl, kitagawa marin, sono bisque doll, blonde hair, brown eyes, gyaru",
        "alias": "marin",
    },
    {
        "tags": "1girl, nishikigi chisato, lycoris recoil, blonde hair, red eyes, hair ribbon",
        "alias": "chisato",
    },
    {
        "tags": "1girl, hatsune miku, vocaloid, aqua hair, twintails, aqua eyes, headset",
        "alias": "miku",
    },
    {
        "tags": "1girl, furina, genshin impact, blue hair, blue eyes, hat, top hat",
        "alias": "furina",
    },
    {
        "tags": "1girl, raiden shogun, genshin impact, purple hair, purple eyes, braid",
        "alias": "raiden",
    },
]

SCENES = [
    {"tags": "cherry blossoms, petals, spring", "alias": "sakura"},
    {"tags": "rain, umbrella, melancholic", "alias": "rain"},
    {"tags": "cafe, coffee cup, sitting", "alias": "cafe"},
    {"tags": "sunset, golden hour, orange sky", "alias": "sunset"},
    {"tags": "night, stars, moon", "alias": "night"},
    {"tags": "snow, winter, scarf, breath", "alias": "snow"},
    {"tags": "autumn, falling leaves, red foliage", "alias": "autumn"},
    {"tags": "seaside, ocean, waves, beach", "alias": "seaside"},
    {"tags": "empty classroom, sunset, desk, memories", "alias": "classroom"},
    {"tags": "convenience store, night, glass door, warm glow", "alias": "konbini"},
    {"tags": "train, window seat, passing scenery, travel", "alias": "train"},
    {"tags": "kyoto, torii gate, shrine, traditional", "alias": "kyoto"},
    {"tags": "vending machine, night, glow, cicada", "alias": "vending"},
    {"tags": "old bookstore, dim light, dusty shelves", "alias": "bookstore"},
    {"tags": "laundromat, late night, fluorescent light", "alias": "laundromat"},
    {"tags": "park bench, autumn, alone, falling leaves", "alias": "park_bench"},
    {"tags": "bicycle, riverside, golden hour, wind", "alias": "bicycle"},
    {"tags": "fireworks, yukata, summer festival", "alias": "matsuri"},
    {"tags": "rooftop, wind, hair blowing", "alias": "rooftop"},
    {"tags": "bridge, river, reflection, dusk", "alias": "bridge"},
]

EXPRESSIONS = [
    {"tags": "gentle smile, soft expression", "alias": "gentle"},
    {"tags": "melancholic, wistful", "alias": "sad"},
    {"tags": "peaceful, serene", "alias": "peaceful"},
    {"tags": "contemplative, thoughtful", "alias": "think"},
    {"tags": "confident, cool", "alias": "cool"},
    {"tags": "nostalgic, bittersweet smile", "alias": "nostalgic"},
]

TOTAL = 50
NEGATIVE = "lowres, bad anatomy, bad hands, error, text, signature, extra fingers, fused fingers, deformed hands, poorly drawn hands"


async def generate(client, idx, preset, char, scene, expr):
    prompt = f"{char['tags']}, {expr['tags']}, {scene['tags']}, masterpiece, best quality, absurdres"
    filename = f"{preset}_{char['alias']}_{scene['alias']}"

    payload = {
        "prompt": prompt,
        "negative_prompt": NEGATIVE,
        "width": 832,
        "height": 1216,
        "style": preset,
        "model": "animagine-xl-4",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=300.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{filename}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(
                f"[{idx:02d}/{TOTAL}] OK [{preset}] {char['alias']}_{scene['alias']} (seed: {seed})"
            )
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL: {data.get('error', '?')}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR: {e}")
        return False


async def main():
    jobs = []
    for _ in range(TOTAL):
        jobs.append(
            (
                random.choice(PRESETS),
                random.choice(CHARACTERS),
                random.choice(SCENES),
                random.choice(EXPRESSIONS),
            )
        )
    random.shuffle(jobs)

    ok = fail = 0
    print(f"Animagine XL 4.0 랜덤 배치 {TOTAL}장")
    print(
        f"캐릭터 {len(CHARACTERS)}명 / 장면 {len(SCENES)}개 / 프리셋 {len(PRESETS)}개"
    )
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, (preset, char, scene, expr) in enumerate(jobs, 1):
            if await generate(client, i, preset, char, scene, expr):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
