"""나데코 드로 - 5인 나데코 배치 (50장 / 캐릭터당 10장).

나데모노가타리 나데코 드로 편 5인:
1. present  - 현재 나데코  (집에서 만화 그리는 은둔형)
2. quiet    - 얌전 나데코  (바케모노가타리: 앞머리 내린 수줍은 나데코)
3. seductive- 교태 나데코  (니세모노가타리: 앞머리 올린 유혹하는 나데코)
4. reverse  - 역 나데코    (오토리모노가타리: 앞머리 잘린 폭력성 각성)
5. god      - 신 나데코    (코이모노: 뱀신이 됐지만 유아퇴행)
"""

import asyncio
from base64 import b64decode
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import httpx

API_URL = "http://localhost:8002/api/generate"

PROVIDER = "nai"
MODEL = "nai-v4.5-full"
STYLE = "monogatari"
STEPS = 28
WIDTH = 832
HEIGHT = 1216

REQUEST_TIMEOUT_SECONDS = 240.0
REQUEST_INTERVAL_SECONDS = 0.3

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = (
    Path(__file__).parent.parent / "outputs" / f"{TODAY}_nadeko_draw_5ver_50"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NEGATIVE_PROMPT = (
    "low quality, worst quality, blurry, out of focus, bad anatomy, deformed hands, "
    "extra fingers, missing fingers, fused fingers, bad hands, watermark, logo, text"
)

CHARACTERS: list[dict] = [
    {
        "alias": "present",
        "base": (
            "sengoku nadeko, monogatari series, 1girl, "
            "orange hair, short hair, messy hair, red eyes, "
            "casual home clothes, hoodie, tired eyes, pale skin"
        ),
        "scenes": [
            "drawing manga at desk, cluttered room, lamp light, upper body",
            "sitting on floor, sketchbook, knee-up, soft indoor light",
            "looking out window, melancholic, night, curtain shadow",
            "close-up portrait, hollow gaze, gentle rim light",
            "lying on bed, staring ceiling, dim light",
            "holding pencil, side profile, concentrated expression",
            "stack of manga on shelf, reading, absorbed",
            "late night, mug of tea, quiet atmosphere",
            "withdrawn expression, doorway framing, interior",
            "hand covering face, shy, ambient light",
        ],
    },
    {
        "alias": "quiet",
        "base": (
            "sengoku nadeko, monogatari series, 1girl, "
            "orange hair, long hair, hair covering eyes, hair over eyes, "
            "red eyes barely visible, school uniform, sailor collar, "
            "soft shy expression, downcast gaze"
        ),
        "scenes": [
            "classroom, window seat, afternoon light, upper body",
            "school hallway, standing alone, backlit",
            "rooftop, light breeze, cherry blossom petals",
            "shrine steps, soft bokeh, summer light",
            "close-up portrait, half-hidden eyes through bangs, cinematic",
            "park bench, holding bag, knees together",
            "waiting, rain outside window, melancholic",
            "library, books, quiet atmosphere, seated",
            "soft smile, looking down, gentle warmth",
            "hands clasped in front, blushing, side angle",
        ],
    },
    {
        "alias": "seductive",
        "base": (
            "sengoku nadeko, monogatari series, 1girl, "
            "orange hair, medium hair, bangs pinned back, hair up, hair clip, "
            "red eyes, confident expression, seductive smile, "
            "sleeveless top, bare shoulders, mature look"
        ),
        "scenes": [
            "upper body, chin tilt, confident gaze at viewer, dramatic lighting",
            "leaning forward, close to camera, bedroom, warm light",
            "standing, arms crossed, smirking, sunset backdrop",
            "close-up portrait, lidded eyes, soft lips, cinematic",
            "side glance over shoulder, low angle, moody",
            "sitting on windowsill, one leg dangling, dusk light",
            "hand on hip, corridor, cool blue light",
            "reaching hand toward viewer, playful expression",
            "candle light, intimate atmosphere, table setting",
            "neck exposed, hair clip, looking away, blushing slightly",
        ],
    },
    {
        "alias": "reverse",
        "base": (
            "sengoku nadeko, monogatari series, 1girl, "
            "orange hair, medium hair, blunt bangs, short bangs, forehead exposed, "
            "sharp red eyes, intense expression, snake motif, "
            "dark outfit, inner awakening, intimidating aura"
        ),
        "scenes": [
            "sharp forward stare, close-up, cold lighting, dramatic",
            "shrine ruins, snake scales glow, moonlight",
            "snake wrapping arm, dark background, cinematic",
            "standing in rain, soaked, intense gaze, side angle",
            "dark forest path, eerie calm, low angle shot",
            "clenched fist, rage suppressed, dramatic shadow",
            "hair blown by wind, sharp eyes, stormy sky",
            "crouching, predatory pose, golden snake eyes",
            "split composition, before and after awakening",
            "glowing red aura, torii gate, night scene",
        ],
    },
    {
        "alias": "god",
        "base": (
            "sengoku nadeko, monogatari series, 1girl, "
            "orange hair, long flowing hair, red eyes, "
            "shrine maiden outfit, miko, white and red, "
            "snake hair ornament, childlike expression, divine aura, "
            "ethereal glow, innocent yet powerful"
        ),
        "scenes": [
            "floating above shrine, petals swirling, divine light",
            "seated on altar, snakes circling, ethereal",
            "childlike giggle, arms wide open, glowing particles",
            "close-up portrait, empty innocent eyes, golden rim light",
            "giant snake spirit behind her, dramatic scale",
            "shrine interior, candlelight, serene expression",
            "looking down at viewer from above, godlike",
            "soft smile, cherry blossom storm, dreamlike",
            "bare feet, stone floor, white miko skirt flowing",
            "eyes closed, prayer gesture, soft divine radiance",
        ],
    },
]


class Job(TypedDict):
    alias: str
    prompt: str
    index: int


def build_jobs() -> list[Job]:
    jobs: list[Job] = []
    index = 1

    for char in CHARACTERS:
        for scene in char["scenes"]:
            prompt = f"1girl, {char['base']}, {scene}, masterpiece, very aesthetic"
            jobs.append(
                {
                    "alias": f"nadeko_{char['alias']}_{index:02d}",
                    "prompt": prompt,
                    "index": index,
                }
            )
            index += 1

    return jobs


async def generate(client: httpx.AsyncClient, job: Job, total: int) -> bool:
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEGATIVE_PROMPT,
        "width": WIDTH,
        "height": HEIGHT,
        "steps": STEPS,
        "provider": PROVIDER,
        "model": MODEL,
        "style": STYLE,
        "save_to_disk": False,
    }

    try:
        response = await client.post(API_URL, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
    except (httpx.HTTPError, ValueError) as error:
        print(f"[{job['index']:02d}/{total}] ERROR {job['alias']}: {error}", flush=True)
        return False

    image_base64 = data.get("image_base64")
    if data.get("success") and image_base64:
        seed = data.get("seed", 0)
        output_path = OUTPUT_DIR / f"{job['index']:02d}_{job['alias']}_{seed}.webp"
        output_path.write_bytes(b64decode(image_base64))
        print(f"[{job['index']:02d}/{total}] OK   {job['alias']} (seed:{seed})", flush=True)
        return True

    error_message = data.get("error", "unknown error")
    print(f"[{job['index']:02d}/{total}] FAIL {job['alias']}: {error_message}", flush=True)
    return False


async def main() -> None:
    jobs = build_jobs()
    total = len(jobs)

    ok = 0
    fail = 0

    print("나데코 드로 5인 배치 | NAI monogatari style", flush=True)
    print(f"캐릭터: present / quiet / seductive / reverse / god  (각 10장)", flush=True)
    print(f"총 {total}장 | output: {OUTPUT_DIR}", flush=True)
    print("=" * 70, flush=True)

    async with httpx.AsyncClient() as client:
        for job in jobs:
            if await generate(client, job, total):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(REQUEST_INTERVAL_SECONDS)

    print("=" * 70, flush=True)
    print(f"완료 | success={ok}, fail={fail}", flush=True)
    print(f"output: {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
