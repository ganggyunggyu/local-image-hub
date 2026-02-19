"""NAI batch: top presets x various characters (200 images).

잘 뽑히는 프리셋 메모임냥
- monogatari
- blue_archive
- kyoto_animation
- chibi_sketch
- mono_halftone

구성임냥
- 40 캐릭터 x 5 프리셋 = 200장임냥
"""

import asyncio
from base64 import b64decode
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import httpx

API_URL = "http://localhost:8002/api/generate"
HEALTH_URL = "http://localhost:8002/health"

PROVIDER = "nai"
MODEL = "nai-v4.5-full"
STEPS = 28

REQUEST_TIMEOUT_SECONDS = 240.0
REQUEST_INTERVAL_SECONDS = 0.3

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_top_presets_various_chars_200"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TOP_STYLES: list[str] = [
    "monogatari",
    "blue_archive",
    "kyoto_animation",
    "chibi_sketch",
    "mono_halftone",
]

NEGATIVE_PROMPT = (
    "low quality, worst quality, blurry, out of focus, bad anatomy, deformed hands, "
    "extra fingers, missing fingers, fused fingers, bad hands, watermark, logo, text"
)

SCENES: list[str] = [
    "classroom, window light",
    "school rooftop, sunset",
    "music room, after school",
    "cafe table, tea time",
    "city street, rainy night",
    "library, quiet atmosphere",
    "shrine, torii",
    "park, cherry blossoms",
    "train station platform, evening",
    "bedroom, soft light",
    "stage, spotlight",
    "hallway, cinematic shadows",
]

POSES: list[str] = [
    "upper body, looking at viewer",
    "close-up portrait, head tilt",
    "full body, standing",
    "sitting pose, relaxed",
    "walking, candid moment",
    "low angle shot, dramatic composition",
    "dutch angle composition",
    "back view, looking over shoulder",
]

EXPRESSIONS: list[str] = [
    "gentle smile",
    "serious expression",
    "playful grin",
    "shy blush",
    "confident smirk",
    "surprised face",
    "calm expression",
    "focused expression",
]

CHARACTERS: list[tuple[str, str]] = [
    # Monogatari
    ("hitagi", "senjougahara hitagi, monogatari, purple hair, long hair, blue eyes"),
    ("hanekawa", "hanekawa tsubasa, monogatari, black hair, long hair, glasses, purple eyes"),
    ("black_hanekawa", "black hanekawa, monogatari, white hair, cat ears, yellow eyes"),
    ("shinobu", "oshino shinobu, monogatari, blonde hair, long hair, yellow eyes, pointy ears"),
    ("kanbaru", "kanbaru suruga, monogatari, dark blue short hair, brown eyes, athletic"),
    ("yotsugi", "ononoki yotsugi, monogatari, green hair, short hair, expressionless, hat"),
    ("ougi", "oshino ougi, monogatari, black short hair, mysterious, school uniform"),
    ("sodachi", "oikura sodachi, monogatari, blonde twintails, blue eyes, sharp eyes"),

    # K-ON!
    ("yui", "hirasawa yui, k-on!, brown short hair, brown eyes, hairclip, guitar"),
    ("mio", "akiyama mio, k-on!, black long hair, grey eyes, bass guitar"),
    ("ritsu", "tainaka ritsu, k-on!, brown short hair, headband, drumsticks"),
    ("mugi", "kotobuki tsumugi, k-on!, blonde long hair, blue eyes, thick eyebrows, keyboard"),
    ("azusa", "nakano azusa, k-on!, black twintails, red eyes, guitar"),

    # Bocchi the Rock!
    ("bocchi", "gotoh hitori, bocchi the rock!, pink long hair, blue eyes, guitar"),
    ("nijika", "ijichi nijika, bocchi the rock!, blonde short hair, blue eyes, side braid, drumsticks"),
    ("ryo", "yamada ryo, bocchi the rock!, blue long hair, red eyes, bass guitar"),
    ("kita", "kita ikuyo, bocchi the rock!, red long hair, green eyes, star hair ornament, guitar"),

    # Blue Archive
    ("shiroko", "shiroko, blue archive, white hair, blue eyes, halo, calm"),
    ("hoshino", "hoshino, blue archive, pink hair, halo, sleepy eyes"),
    ("hina", "hina, blue archive, purple hair, halo, serious"),
    ("arona", "arona, blue archive, blue hair, halo, cheerful"),
    ("shun", "shun, blue archive, purple hair, ponytail, halo, mature"),
    ("yuuka", "hayase yuuka, blue archive, black hair, glasses, halo"),
    ("mika", "mika, blue archive, blonde hair, halo, sweet smile"),
    ("ba_azusa", "shirasu azusa, blue archive, blonde hair, halo, serious"),

    # Genshin Impact
    ("raiden", "raiden shogun, genshin impact, purple hair, purple eyes, elegant"),
    ("keqing", "keqing, genshin impact, purple twintails, purple eyes, confident"),
    ("ganyu", "ganyu, genshin impact, blue hair, horns, gentle"),
    ("furina", "furina, genshin impact, two-tone hair, dramatic, noble"),
    ("nahida", "nahida, genshin impact, white hair, green eyes, small"),

    # Others
    ("violet", "violet evergarden, blonde hair, blue eyes, brooch, stoic"),
    ("chisato", "chisato nishikigi, lycoris recoil, blonde hair, red eyes, cheerful"),
    ("takina", "takina inoue, lycoris recoil, black hair, serious, cool"),
    ("rem", "rem, re:zero, blue hair, maid outfit, gentle smile"),
    ("emilia", "emilia, re:zero, silver hair, elf ears, purple eyes, kind"),
    ("asuka", "asuka langley, neon genesis evangelion, red hair, blue eyes, plugsuit"),
    ("rei", "rei ayanami, neon genesis evangelion, blue hair, red eyes, stoic"),
    ("makima", "makima, chainsaw man, red hair, yellow eyes, calm"),
    ("power", "power, chainsaw man, blonde hair, horns, wild grin"),
    ("yor", "yor forger, spy x family, black hair, red eyes, elegant"),
]


class Job(TypedDict):
    style: str
    prompt: str
    alias: str
    width: int
    height: int


def build_prompt(style: str, char_tags: str, char_index: int, style_index: int) -> str:
    scene = SCENES[(char_index + style_index * 2) % len(SCENES)]
    pose = POSES[(char_index * 3 + style_index) % len(POSES)]
    expression = EXPRESSIONS[(char_index + style_index * 5) % len(EXPRESSIONS)]

    if style == "chibi_sketch":
        scene = "simple background"
        pose = "full body, chibi pose"
        expression = "smile"

    if style == "mono_halftone":
        scene = "simple background"

    if style == "monogatari" and "head tilt" not in pose:
        pose = f"{pose}, head tilt"

    return f"1girl, {char_tags}, {scene}, {pose}, {expression}, masterpiece, very aesthetic"


def build_jobs() -> list[Job]:
    jobs: list[Job] = []

    width = 832
    height = 1024

    for style_index, style in enumerate(TOP_STYLES):
        for char_index, (char_alias, char_tags) in enumerate(CHARACTERS):
            prompt = build_prompt(style, char_tags, char_index, style_index)
            jobs.append(
                {
                    "style": style,
                    "prompt": prompt,
                    "alias": f"{char_alias}_{style}",
                    "width": width,
                    "height": height,
                }
            )

    return jobs


async def check_server(client: httpx.AsyncClient) -> bool:
    try:
        response = await client.get(HEALTH_URL, timeout=5.0)
        return response.status_code == 200
    except httpx.HTTPError:
        return False


async def generate(client: httpx.AsyncClient, index: int, total: int, job: Job) -> bool:
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEGATIVE_PROMPT,
        "width": job["width"],
        "height": job["height"],
        "steps": STEPS,
        "provider": PROVIDER,
        "model": MODEL,
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        response = await client.post(API_URL, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
    except (httpx.HTTPError, ValueError) as error:
        print(f"[{index:03d}/{total}] ERROR {job['alias']} [{job['style']}]: {error}", flush=True)
        return False

    image_base64 = data.get("image_base64")
    if data.get("success") and image_base64:
        seed = data.get("seed", 0)
        output_path = OUTPUT_DIR / f"{index:03d}_{job['alias']}_{seed}.webp"
        output_path.write_bytes(b64decode(image_base64))
        print(f"[{index:03d}/{total}] OK {job['alias']} [{job['style']}] (seed: {seed})", flush=True)
        return True

    error_message = data.get("error", "unknown error")
    print(f"[{index:03d}/{total}] FAIL {job['alias']} [{job['style']}]: {error_message}", flush=True)
    return False


async def main() -> None:
    jobs = build_jobs()
    total = len(jobs)

    ok = 0
    fail = 0

    print("top presets x various chars 200 (NAI)", flush=True)
    print(f"styles: {', '.join(TOP_STYLES)}", flush=True)
    print(f"chars: {len(CHARACTERS)}", flush=True)
    print(f"total: {total}", flush=True)
    print(f"output: {OUTPUT_DIR}", flush=True)
    print("=" * 70, flush=True)

    async with httpx.AsyncClient() as client:
        if not await check_server(client):
            print("server not reachable: http://localhost:8002", flush=True)
            print("run `make dev` first then retry", flush=True)
            return

        for index, job in enumerate(jobs, start=1):
            if await generate(client, index, total, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(REQUEST_INTERVAL_SECONDS)

    print("=" * 70, flush=True)
    print(f"done: success={ok}, fail={fail}", flush=True)
    print(f"output: {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
