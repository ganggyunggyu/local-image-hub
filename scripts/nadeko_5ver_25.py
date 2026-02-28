"""나데코 드로 5인 × 5장 = 25장.

애니/캐릭터명 명시 방식으로 각 버전 정확히 잡기.
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
    Path(__file__).parent.parent / "outputs" / f"{TODAY}_nadeko_5ver_25"
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
            "sengoku nadeko, monogatari series, nademonogatari, nadeko draw, 1girl, "
            "orange hair, very short hair, pixie cut, no bangs, visible red eyes, "
            "determined expression, manga artist, independent young woman, "
            "casual work clothes, small apartment, pale skin"
        ),
        "neg_extra": "long hair, hair over eyes, school uniform, depressed, hollow",
        "scenes": [
            "drawing manga at desk with focused determination, lamp light, upper body, confident",
            "holding finished manga page with proud smile, warm room light",
            "pinning storyboard panels on wall, planning next chapter, engaged and energetic",
            "close-up portrait, direct confident gaze, short hair, slight smile, soft cinematic light",
            "celebrating finished chapter with small fist pump, genuine happy expression",
        ],
    },
    {
        "alias": "quiet",
        "base": (
            "sengoku nadeko, monogatari series, bakemonogatari, 1girl, "
            "orange hair, long hair, hair covering eyes, bangs over eyes, "
            "red eyes barely visible, school uniform, sailor collar, "
            "shy expression, downcast gaze, soft blush, passive, introverted"
        ),
        "neg_extra": "short hair, confident, bold, seductive",
        "scenes": [
            "classroom window seat, afternoon light, hugging bag, upper body, soft shy look",
            "close-up portrait, half-hidden eyes through long bangs, cinematic warm light",
            "shrine steps, summer light, hands clasped, looking down, gentle bokeh",
            "park bench, knees together, soft smile barely visible, cherry blossom petals",
            "school hallway, standing alone, backlit, quiet and withdrawn",
        ],
    },
    {
        "alias": "seductive",
        "base": (
            "sengoku nadeko, monogatari series, nisemonogatari, 1girl, "
            "orange hair, medium hair, bangs pinned back, hair clip, hair up, "
            "red eyes, confident lidded eyes, seductive smile, "
            "sleeveless top, bare shoulders, mature look, flirtatious"
        ),
        "neg_extra": "shy, hair over eyes, school uniform, short hair",
        "scenes": [
            "upper body, chin tilt, confident gaze at viewer, dramatic cinematic lighting",
            "leaning forward close to camera, warm bedroom light, playful expression",
            "side glance over shoulder, low angle, moody cool light",
            "close-up portrait, lidded red eyes, soft lips, hair clip visible, cinematic",
            "sitting on windowsill, dusk light, one leg dangling, smirking",
        ],
    },
    {
        "alias": "reverse",
        "base": (
            "sengoku nadeko, monogatari series, otorimonogatari, 1girl, "
            "orange hair, medium hair, blunt short bangs, forehead fully exposed, "
            "sharp red eyes, intense expression, inner awakening, "
            "snake motif, dark atmosphere, intimidating aura"
        ),
        "neg_extra": "shy, soft, gentle, long bangs, hair over eyes, cute",
        "scenes": [
            "sharp forward stare directly at viewer, cold dramatic lighting, close-up",
            "shrine ruins at night, moonlight, snake coiling around arm, intense",
            "standing in rain, soaked, sharp eyes cutting through, side angle",
            "clenched fist, rage suppressed, dramatic shadow split across face",
            "glowing red aura, torii gate background, night, foreboding calm",
        ],
    },
    {
        "alias": "god",
        "base": (
            "sengoku nadeko, monogatari series, otorimonogatari, koimonogatari, 1girl, "
            "orange hair, long flowing hair, red eyes, "
            "miko outfit, shrine maiden, white and red hakama, "
            "snake hair ornament, childlike innocent expression, "
            "divine ethereal aura, goddess, snake deity"
        ),
        "neg_extra": "modern clothes, school uniform, short hair, mature, serious",
        "scenes": [
            "floating above shrine, petals swirling, divine golden light, ethereal",
            "seated on altar, giant snake spirit behind her, dramatic scale, awe",
            "childlike wide smile, arms spread open, glowing divine particles",
            "close-up portrait, innocent empty red eyes, golden rim light, sacred",
            "bare feet on stone floor, white hakama flowing, soft divine radiance, serene",
        ],
    },
]


class Job(TypedDict):
    alias: str
    prompt: str
    neg: str
    index: int


def build_jobs() -> list[Job]:
    jobs: list[Job] = []
    index = 1
    for char in CHARACTERS:
        neg = NEGATIVE_PROMPT + (f", {char['neg_extra']}" if char.get("neg_extra") else "")
        for scene in char["scenes"]:
            jobs.append(
                {
                    "alias": f"nadeko_{char['alias']}_{index:02d}",
                    "prompt": f"1girl, {char['base']}, {scene}, masterpiece, very aesthetic",
                    "neg": neg,
                    "index": index,
                }
            )
            index += 1
    return jobs


async def generate(client: httpx.AsyncClient, job: Job, total: int) -> bool:
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": job["neg"],
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

    print("나데코 드로 5인 × 5장 = 25장 | NAI monogatari", flush=True)
    print("present / quiet / seductive / reverse / god", flush=True)
    print(f"output: {OUTPUT_DIR}", flush=True)
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
