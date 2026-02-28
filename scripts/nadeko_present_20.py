"""지금 나데코 (오프 시리즈) 배치 20장.

필명 "센고쿠 나데시코"로 연재 중인 만화가.
도쿄 혼자 독립, 꿈을 당당하게 추구하는 청년.
은둔형 X - 열심히 살아가는 프로 만화가 O.

외형:
- 매우 짧은 단발 (베리숏 / 직접 자른 short cut)
- 앞머리 없음, 눈 선명히 보임
- 홈웨어보다 캐주얼 작업복 계열
- 지쳐도 표정엔 의지, 성취감, 열정
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
    Path(__file__).parent.parent / "outputs" / f"{TODAY}_nadeko_present_20"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NEGATIVE_PROMPT = (
    "low quality, worst quality, blurry, out of focus, bad anatomy, deformed hands, "
    "extra fingers, missing fingers, fused fingers, bad hands, watermark, logo, text, "
    "school uniform, sailor collar, long hair, hair covering eyes, bangs over eyes, "
    "depressed, hollow, reclusive, withdrawn, sad, crying"
)

CHAR_BASE = (
    "sengoku nadeko, monogatari series, nademonogatari, nadeko draw, 1girl, "
    "orange hair, very short hair, pixie cut, short cut, no bangs, "
    "visible red eyes, determined expression, independent young woman, "
    "manga artist, pale skin, casual work clothes, apartment"
)

SCENES: list[str] = [
    "drawing at desk with focused determination, manuscript pages neatly arranged, desk lamp, upper body",
    "close-up portrait, confident direct gaze at viewer, short hair, slight proud smile, soft light",
    "holding finished manga page triumphantly, satisfied expression, warm room light",
    "leaning back in chair stretching arms, tired but accomplished, after long work session",
    "pinning storyboard panels on wall, planning next chapter, concentrated and engaged",
    "small apartment, morning light, making coffee before work, casual t-shirt, energetic",
    "phone call with editor, gesturing expressively, excited, window light behind her",
    "inking manga panel with steady hand, tongue slightly out in concentration, close-up",
    "sitting on floor surrounded by reference books, research mode, enthusiastic",
    "late night but still drawing with determination, desk lamp glow, focused not exhausted",
    "comparing two draft panels, critical eye, professional artist at work",
    "brief window break, gazing outside with quiet confidence, cup in hand, thoughtful",
    "celebrating finished chapter, small fist pump, genuine happy smile",
    "working on digital tablet alternatively, stylus in hand, modern setup, natural light",
    "reading rivals manga for research, analytical expression, cross-legged on floor",
    "messy hair from long work session but grinning, ink on cheek, proud mess",
    "side profile at window, holding pen, planning next scene in head, contemplative",
    "video call with another manga artist friend, laughing, casual and lively",
    "early morning, just woke up with idea, grabbing sketchbook immediately, excited",
    "looking at published tankobon (collected volume) of her work, quiet pride, warm smile",
]


class Job(TypedDict):
    alias: str
    prompt: str
    index: int


def build_jobs() -> list[Job]:
    return [
        {
            "alias": f"nadeko_present_{i + 1:02d}",
            "prompt": f"1girl, {CHAR_BASE}, {scene}, masterpiece, very aesthetic",
            "index": i + 1,
        }
        for i, scene in enumerate(SCENES)
    ]


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

    print("지금 나데코 | 만화가 센고쿠 나데시코 | NAI monogatari style", flush=True)
    print(f"총 {total}장 | 베리숏, 눈 선명, 꿈 향해 달리는 프로 만화가", flush=True)
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
