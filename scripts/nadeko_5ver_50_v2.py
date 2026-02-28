"""나데코 드로 5인 × 10장 = 50장 v2. 씬 전부 새로."""

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
    Path(__file__).parent.parent / "outputs" / f"{TODAY}_nadeko_5ver_50_v2"
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
            "morning routine, brushing short hair in mirror, casual shirt, soft daylight, upper body",
            "convenience store run, hoodie, bag under arm, evening city light, candid",
            "editor meeting cafe, leaning forward explaining idea, energetic, window seat",
            "stretching at desk mid-work, yawning but happy, lamp glow, cozy",
            "sketchbook in lap on train, drawing, focused, commute, natural window light",
            "phone showing debut announcement page, wide grin, bedroom, warm light",
            "inking at 3am, energy drink beside her, pushing through, intense focus",
            "laundry day, t-shirt and shorts, humming, casual home, relaxed",
            "video call on laptop, waving and laughing, lively expression, night",
            "reading own published volume in bookstore, small private smile, soft light",
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
        "neg_extra": "short hair, confident, bold, seductive, hair visible",
        "scenes": [
            "eating lunch alone on rooftop, gentle breeze, quiet contentment",
            "walking home alone, sunlight through trees, bag clutched, looking down",
            "rainy window, classroom empty, sitting quietly, melancholic",
            "sneaking glance sideways, slight blush, hands fidgeting, soft light",
            "reading book in corner of library, completely absorbed, calm",
            "tying shoe slowly, long bangs falling forward, low angle, afternoon",
            "waiting at bus stop, clutching strap, light rain, soft gaze ahead",
            "receiving note, surprised blush under bangs, classroom, backlit",
            "festival crowd, slightly overwhelmed, holding candy apple, night lanterns",
            "alone in gym storage room, sitting on mat, quiet introspection, dim light",
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
        "neg_extra": "shy, hair over eyes, school uniform, short hair, sad",
        "scenes": [
            "applying lip gloss in compact mirror, bedroom vanity, warm light, half-smile",
            "arms stretched above head, yawning theatrically, bare midriff, playful",
            "twirling hair clip in fingers, smirking, casual lean on wall, side light",
            "sitting across a table, chin resting on folded hands, eye contact, intimate",
            "standing in doorway, one hand on frame, backlit, silhouette and detail",
            "fixing hair in reflection of dark window at night, calm and confident",
            "eating ice cream, eyes closed in satisfaction, summer outdoor, carefree",
            "foot on chair seat, looking down at camera, low angle, dominant",
            "lying on side on couch, hand propping head, lazy smile, soft afternoon",
            "bare feet on cool floor, stretching, morning, golden hour light through window",
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
        "neg_extra": "shy, soft, gentle, long bangs, hair over eyes, cute, happy",
        "scenes": [
            "walking through crowd that parts around her, unsettling calm, wide angle",
            "sitting cross-legged on shrine floor, snakes pooling around her, moonlight",
            "close-up eyes only, sharp red iris, reflection of fire in pupils",
            "laughing softly to herself, sinister undertone, cherry blossoms falling",
            "finger trailing along wall, leaving faint snake-scale mark, dim corridor",
            "back against torii gate, arms crossed, daring gaze, stormy sky",
            "crouching at water's edge, staring at reflection, two selves visible",
            "striding forward, wind behind her, hair whipping, unstoppable energy",
            "head tilted, curious predatory expression, someone off-screen, night",
            "hands raised, small snakes between fingers, eerie playful smile",
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
        "neg_extra": "modern clothes, school uniform, short hair, mature, serious, sad",
        "scenes": [
            "spinning playfully on shrine grounds, petals everywhere, carefree divine child",
            "sitting with legs dangling off giant snake coil like a swing, happy",
            "pouting with crossed arms, tantrum energy but divine scale, dramatic clouds",
            "picking up small frog curiously, crouching, childlike wonder, soft glow",
            "braiding snakes into her hair absentmindedly, humming, serene",
            "sleeping on altar like a nap, snakes curled protectively, peaceful",
            "blowing on dandelion seeds, divine light scattering them like stars",
            "close-up, tilting head at viewer, innocent smile, golden pupils glowing",
            "waving both hands enthusiastically at someone below, high vantage point",
            "stacking shrine offering boxes like blocks, tongue out, concentrated, playful",
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
        neg = NEGATIVE_PROMPT + f", {char['neg_extra']}"
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

    print("나데코 드로 5인 × 10장 = 50장 v2 | NAI monogatari", flush=True)
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
