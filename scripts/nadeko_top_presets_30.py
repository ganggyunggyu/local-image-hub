"""NAI batch: Nadeko x top presets (30 images).

NAI 기준 잘 뽑히는 프리셋 메모임냥
- monogatari
- blue_archive
- kyoto_animation
- chibi_sketch
- mono_halftone
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
STEPS = 28

REQUEST_TIMEOUT_SECONDS = 240.0
REQUEST_INTERVAL_SECONDS = 0.3

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_nadeko_top_presets_30"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TOP_STYLES: list[str] = [
    "monogatari",
    "blue_archive",
    "kyoto_animation",
    "chibi_sketch",
    "mono_halftone",
]

CHAR = "sengoku nadeko, monogatari, orange hair, long hair, red eyes, bangs"

NEGATIVE_PROMPT = (
    "low quality, worst quality, blurry, out of focus, bad anatomy, deformed hands, "
    "extra fingers, missing fingers, fused fingers, bad hands, watermark, logo, text"
)

SCENES: list[str] = [
    "classroom, window light, after school",
    "shrine, torii, summer air",
    "cafe table, tea and cake",
    "bedroom, soft light, cozy",
    "rainy street, night, reflections",
    "park, cherry blossoms, petals",
    "library, quiet atmosphere, books",
    "train station platform, evening",
    "school rooftop, sunset wind",
    "festival, lantern lights, night",
]

POSES: list[str] = [
    "upper body, head tilt, looking at viewer",
    "close-up portrait, soft gaze",
    "full body, standing pose",
    "sitting, knees together, shy",
    "walking, candid moment",
    "low angle shot, dramatic composition",
    "dutch angle composition, shaft-like framing",
]

EXPRESSIONS: list[str] = [
    "shy blush",
    "gentle smile",
    "serious eyes",
    "surprised face",
    "playful grin",
    "melancholic",
]

OUTFITS: list[str] = [
    "school uniform, sailor collar",
    "casual clothes, cardigan",
    "yukata",
    "summer dress",
    "hoodie, casual",
    "winter coat, scarf",
]


class Job(TypedDict):
    style: str
    prompt: str
    alias: str
    width: int
    height: int


def build_jobs() -> list[Job]:
    jobs: list[Job] = []

    per_style = 6
    width = 832
    height = 1024

    for style_index, style in enumerate(TOP_STYLES):
        for i in range(per_style):
            scene = SCENES[(style_index * 2 + i) % len(SCENES)]
            pose = POSES[(style_index + i) % len(POSES)]
            expression = EXPRESSIONS[(style_index * 3 + i) % len(EXPRESSIONS)]
            outfit = OUTFITS[(style_index + i * 2) % len(OUTFITS)]

            extra = ""
            if style == "chibi_sketch":
                extra = ", full body"

            prompt = (
                f"1girl, {CHAR}, {outfit}, {scene}, {pose}, {expression}{extra}, "
                "masterpiece, very aesthetic"
            )

            jobs.append(
                {
                    "style": style,
                    "prompt": prompt,
                    "alias": f"nadeko_{style}_{i + 1:02d}",
                    "width": width,
                    "height": height,
                }
            )

    return jobs


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
        output_path = OUTPUT_DIR / f"{index:02d}_{job['alias']}_{seed}.webp"
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

    print("nadeko top presets 30 (NAI)", flush=True)
    print(f"styles: {', '.join(TOP_STYLES)}", flush=True)
    print(f"output: {OUTPUT_DIR}", flush=True)
    print("=" * 70, flush=True)

    async with httpx.AsyncClient() as client:
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
