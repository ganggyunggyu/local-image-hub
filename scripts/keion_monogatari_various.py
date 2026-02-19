"""Generate diverse K-ON! characters using the monogatari style preset."""

import asyncio
from base64 import b64decode
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import httpx

API_URL = "http://localhost:8002/api/generate"
REQUEST_TIMEOUT_SECONDS = 240.0
REQUEST_INTERVAL_SECONDS = 0.3

STYLE = "monogatari"
MODEL = "nai-v4.5-full"
PROVIDER = "nai"
STEPS = 28

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_keion_monogatari_various"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NEGATIVE_PROMPT = (
    "low quality, worst quality, blurry, out of focus, extra fingers, missing fingers, "
    "fused fingers, deformed hands, bad hands, bad anatomy, watermark, logo, text"
)


class Job(TypedDict):
    prompt: str
    alias: str
    width: int
    height: int


KEION_CHARACTERS: list[tuple[str, str]] = [
    ("yui", "hirasawa yui, k-on!, brown short hair, brown eyes, cheerful, guitar"),
    ("mio", "akiyama mio, k-on!, black long hair, grey eyes, shy, bass guitar"),
    ("ritsu", "tainaka ritsu, k-on!, brown short hair, headband, energetic, drumsticks"),
    ("mugi", "kotobuki tsumugi, k-on!, blonde long hair, blue eyes, elegant, keyboard"),
    ("azusa", "nakano azusa, k-on!, black twintails, red eyes, serious, guitar"),
    ("ui", "hirasawa ui, k-on!, brown medium hair, kind smile, apron"),
    ("nodoka", "manabe nodoka, k-on!, dark blue long hair, glasses, calm, student council"),
    ("sawako", "yamanaka sawako, k-on!, brown long hair, teacher, mature, stylish"),
    ("jun", "suzuki jun, k-on!, short brown hair, playful, bass guitar"),
]

CHARACTER_MAP: dict[str, str] = dict(KEION_CHARACTERS)
SOLO_VARIANTS_PER_CHARACTER = 5

OUTFIT_TAGS = [
    "school uniform, blazer",
    "casual clothes, cardigan",
    "live stage outfit, frilled costume",
    "summer uniform",
    "winter coat, scarf",
    "yukata, summer festival",
]

SCENE_TAGS = [
    "music room, after school",
    "classroom, sunset light",
    "school rooftop, golden hour",
    "live house stage, spotlight",
    "empty hallway, cinematic shadows",
    "cafe table, tea and cake",
    "city street, rainy night",
    "park, cherry blossoms",
    "library, quiet atmosphere",
    "train station platform, evening",
]

POSE_TAGS = [
    "upper body, looking at viewer",
    "full body, dynamic stance",
    "close-up portrait, head tilt",
    "sitting pose, crossed legs",
    "leaning on wall, relaxed",
    "walking pose, motion blur",
    "low angle shot, dramatic",
    "dutch angle composition",
]

EXPRESSION_TAGS = [
    "bright smile",
    "focused expression",
    "gentle smile",
    "playful grin",
    "serious eyes",
    "surprised face",
    "shy blush",
    "confident smirk",
]

DUO_SETUPS: list[tuple[str, str, str, str]] = [
    ("yui", "azusa", "practice together, senpai and kouhai energy", "music room, guitar duet"),
    ("mio", "ritsu", "childhood friends, teasing, playful", "classroom, after school"),
    ("mugi", "ritsu", "tea time and jokes, bright mood", "club room table, tea set"),
    ("yui", "ui", "sisters, warm and cozy", "kitchen, home atmosphere"),
    ("azusa", "jun", "bass and guitar jam session", "live stage rehearsal"),
    ("nodoka", "yui", "study help, relaxed", "library table, notebooks"),
    ("sawako", "mio", "teacher and student, stylish contrast", "music room, evening light"),
    ("mio", "azusa", "guitar technique talk, serious", "practice studio, focused"),
    ("yui", "mugi", "snack break, cheerful", "cafe corner, desserts"),
    ("ritsu", "jun", "rhythm section duo, energetic", "stage backstage"),
    ("nodoka", "ui", "calm conversation, friendly", "school courtyard"),
    ("mugi", "sawako", "fashion check, elegant", "dressing room mirror"),
]

GROUP_PROMPTS: list[tuple[str, str]] = [
    (
        "htt_stage",
        "5girls, hirasawa yui, akiyama mio, tainaka ritsu, kotobuki tsumugi, nakano azusa, "
        "k-on!, live concert, full band, dramatic spotlight, crowd glow",
    ),
    (
        "htt_tea_time",
        "5girls, hirasawa yui, akiyama mio, tainaka ritsu, kotobuki tsumugi, nakano azusa, "
        "k-on!, tea time, cakes, club room, warm daylight",
    ),
    (
        "htt_rooftop",
        "5girls, hirasawa yui, akiyama mio, tainaka ritsu, kotobuki tsumugi, nakano azusa, "
        "k-on!, school rooftop, sunset wind, nostalgic",
    ),
    (
        "extended_cast",
        "8girls, hirasawa yui, akiyama mio, tainaka ritsu, kotobuki tsumugi, nakano azusa, "
        "hirasawa ui, manabe nodoka, suzuki jun, k-on!, group photo, cheerful",
    ),
    (
        "festival_yukata",
        "6girls, hirasawa yui, akiyama mio, tainaka ritsu, kotobuki tsumugi, nakano azusa, hirasawa ui, "
        "k-on!, summer festival, yukata, lantern lights",
    ),
    (
        "graduation",
        "6girls, hirasawa yui, akiyama mio, tainaka ritsu, kotobuki tsumugi, nakano azusa, manabe nodoka, "
        "k-on!, graduation day, cherry blossoms, emotional",
    ),
    (
        "winter_walk",
        "6girls, hirasawa yui, akiyama mio, tainaka ritsu, kotobuki tsumugi, nakano azusa, suzuki jun, "
        "k-on!, winter city walk, coats and scarves, evening lights",
    ),
    (
        "teacher_group",
        "4girls, yamanaka sawako, hirasawa yui, akiyama mio, tainaka ritsu, "
        "k-on!, preparation for school festival, costume fitting",
    ),
]


def build_solo_jobs() -> list[Job]:
    jobs: list[Job] = []

    for char_index, (alias, tags) in enumerate(KEION_CHARACTERS):
        for variant_index in range(SOLO_VARIANTS_PER_CHARACTER):
            outfit = OUTFIT_TAGS[(char_index + variant_index) % len(OUTFIT_TAGS)]
            scene = SCENE_TAGS[(char_index * 2 + variant_index) % len(SCENE_TAGS)]
            pose = POSE_TAGS[(char_index + variant_index * 2) % len(POSE_TAGS)]
            expression = EXPRESSION_TAGS[(char_index * 3 + variant_index) % len(EXPRESSION_TAGS)]
            prompt = (
                f"1girl, {tags}, {outfit}, {scene}, {pose}, {expression}, "
                "cinematic framing, masterpiece"
            )
            jobs.append(
                {
                    "prompt": prompt,
                    "alias": f"solo_{alias}_{variant_index + 1:02d}",
                    "width": 832,
                    "height": 1024,
                }
            )

    return jobs


def build_duo_jobs() -> list[Job]:
    jobs: list[Job] = []

    for index, (left_alias, right_alias, mood, scene) in enumerate(DUO_SETUPS, start=1):
        left_tags = CHARACTER_MAP[left_alias]
        right_tags = CHARACTER_MAP[right_alias]
        prompt = (
            f"2girls, multiple girls, {left_tags}, {right_tags}, {scene}, {mood}, "
            "upper body, dynamic composition, masterpiece"
        )
        jobs.append(
            {
                "prompt": prompt,
                "alias": f"duo_{left_alias}_{right_alias}_{index:02d}",
                "width": 1024,
                "height": 832,
            }
        )

    return jobs


def build_group_jobs() -> list[Job]:
    jobs: list[Job] = []

    for alias, group_prompt in GROUP_PROMPTS:
        jobs.append(
            {
                "prompt": f"{group_prompt}, masterpiece",
                "alias": f"group_{alias}",
                "width": 1024,
                "height": 832,
            }
        )

    return jobs


def build_jobs() -> tuple[list[Job], int, int, int]:
    solo_jobs = build_solo_jobs()
    duo_jobs = build_duo_jobs()
    group_jobs = build_group_jobs()

    jobs = [*solo_jobs, *duo_jobs, *group_jobs]
    return jobs, len(solo_jobs), len(duo_jobs), len(group_jobs)


async def generate(client: httpx.AsyncClient, index: int, total: int, job: Job) -> bool:
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEGATIVE_PROMPT,
        "width": job["width"],
        "height": job["height"],
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
        print(f"[{index:03d}/{total}] ERROR {job['alias']}: {error}", flush=True)
        return False

    image_base64 = data.get("image_base64")
    if data.get("success") and image_base64:
        seed = data.get("seed", 0)
        output_path = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
        output_path.write_bytes(b64decode(image_base64))
        print(f"[{index:03d}/{total}] OK {job['alias']} (seed: {seed})", flush=True)
        return True

    error_message = data.get("error", "unknown error")
    print(f"[{index:03d}/{total}] FAIL {job['alias']}: {error_message}", flush=True)
    return False


async def main() -> None:
    jobs, solo_count, duo_count, group_count = build_jobs()
    total_jobs = len(jobs)

    ok_count = 0
    fail_count = 0

    print("K-ON! monogatari preset batch", flush=True)
    print(
        f"total: {total_jobs} (solo: {solo_count}, duo: {duo_count}, group: {group_count})",
        flush=True,
    )
    print(f"output: {OUTPUT_DIR}", flush=True)
    print("=" * 70, flush=True)

    async with httpx.AsyncClient() as client:
        for index, job in enumerate(jobs, start=1):
            if await generate(client, index, total_jobs, job):
                ok_count += 1
            else:
                fail_count += 1
            await asyncio.sleep(REQUEST_INTERVAL_SECONDS)

    print("=" * 70, flush=True)
    print(f"done: success={ok_count}, fail={fail_count}", flush=True)
    print(f"output: {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
