"""하네카와 3버전 일반 컨셉 150장"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_hanekawa_3ver_150"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 하네카와 3버전
HANEKAWA_VERSIONS = [
    ("hanekawa_base", "hanekawa tsubasa, monogatari, black hair, long hair, braids, glasses, gentle, class president"),
    ("black_hanekawa", "black hanekawa, monogatari, white hair, long hair, cat ears, golden eyes, seductive, tress"),
    ("hanekawa_short_mix", "hanekawa tsubasa, monogatari, short hair, bob cut, black and white mixed hair, tired eyes, traumatized, bandages"),
]

# 이쁜 프리셋
PRETTY_PRESETS = [
    "pale_aqua", "monogatari", "kyoto_animation", "pastel_soft",
    "waterful", "blue_archive", "pop_fanart", "watercolor_sketch",
    "cozy_gouache", "ghibli", "shinkai", "sepia_backlit",
]

# 다양한 상황 (50종)
SCENES = [
    # 학교/교실 (10)
    "classroom, sitting at desk, studying, focused, window light, upper body",
    "library, reading book, quiet, peaceful, surrounded by books, upper body",
    "school hallway, walking, after school, gentle smile, full body",
    "rooftop, sitting, looking at sky, wind, peaceful, upper body",
    "school uniform, standing, blackboard, teaching, upper body",
    "student council room, paperwork, serious, responsible, upper body",
    "exam, writing, focused, determined, upper body",
    "helping classmate, explaining, kind, patient, upper body",
    "school gate, leaving, sunset, nostalgic, upper body",
    "cafeteria, eating lunch, relaxed, casual, upper body",

    # 집/방 (8)
    "bedroom, lying on bed, reading, relaxed, cozy, full body",
    "desk, studying late night, tired, focused, upper body",
    "window, looking outside, thoughtful, rain, upper body",
    "living room, sitting on sofa, relaxed, home, upper body",
    "kitchen, making tea, gentle, domestic, upper body",
    "balcony, evening, city view, peaceful, upper body",
    "mirror, fixing hair, preparing, morning routine, upper body",
    "bed, waking up, sleepy, morning light, upper body",

    # 도시/거리 (8)
    "city street, walking, shopping bags, casual clothes, full body",
    "bookstore, browsing books, interested, intellectual, upper body",
    "cafe, sitting, drinking coffee, relaxed, warm lighting, upper body",
    "park, sitting on bench, reading, peaceful, nature, full body",
    "night city, neon lights, mysterious, urban, upper body",
    "convenience store, shopping, casual, night, upper body",
    "bus stop, waiting, evening, peaceful, upper body",
    "crosswalk, walking, city life, full body",

    # 도서관/독서 (6)
    "library, tall bookshelf, looking for book, reaching up, full body",
    "library desk, studying, notes, focused, upper body",
    "library corner, reading, absorbed, quiet, upper body",
    "bookshelf, organizing books, librarian, upper body",
    "reading nook, comfortable, book, peaceful, upper body",
    "library window, reading, natural light, serene, upper body",

    # 감정/표정 (10)
    "gentle smile, warm, kind, caring, upper body",
    "serious expression, focused, determined, upper body",
    "tired, exhausted, weary, sleepless, upper body",
    "worried, anxious, concerned, troubled, upper body",
    "thinking, hand on chin, pondering, intelligent, upper body",
    "surprised, eyes wide, shock, upper body",
    "embarrassed, blushing, flustered, shy, upper body",
    "sad, teary eyes, emotional, hurt, upper body",
    "relieved, peaceful smile, calm, upper body",
    "confident, proud, accomplished, upper body",

    # 특별한 순간 (8)
    "sunset, golden hour, wind, hair flowing, emotional, upper body",
    "rain, umbrella, wet, melancholic, upper body",
    "night, moonlight, mysterious, beautiful, upper body",
    "cherry blossoms, spring, petals falling, peaceful, upper body",
    "snow, winter, cold, scarf, gentle, upper body",
    "starry sky, looking up, dreamy, night, upper body",
    "sunrise, morning, hopeful, new beginning, upper body",
    "autumn leaves, falling, nostalgic, warm colors, upper body",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers"

JOBS = []

# 3버전 x 50장씩 = 150장
for char_idx, (alias, char_tags) in enumerate(HANEKAWA_VERSIONS):
    for variant_idx in range(50):
        preset = PRETTY_PRESETS[variant_idx % len(PRETTY_PRESETS)]
        scene = SCENES[variant_idx % len(SCENES)]

        job_idx = len(JOBS) + 1
        JOBS.append({
            "prompt": f"1girl, {char_tags}, {scene}",
            "style": preset,
            "name": f"hanekawa_{job_idx:03d}_{alias}_{variant_idx+1:02d}_{preset}",
        })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, idx: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece, best quality",
        "negative_prompt": NEGATIVE,
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=240.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:03d}/{TOTAL}] OK {job['name']}", flush=True)
            return True
        print(f"[{idx:03d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:50]}", flush=True)
        return False
    except Exception as e:
        print(f"[{idx:03d}/{TOTAL}] ERROR {job['name']}: {e}", flush=True)
        return False


async def main() -> None:
    ok = fail = 0
    print(f"📚 하네카와 3버전 일반 컨셉 {TOTAL}장! 📚", flush=True)
    print(f"기본 50 + 블랙하네카와 50 + 단발백발믹스 50", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)
    print("=" * 70, flush=True)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 70, flush=True)
    print(f"🎉 완료! 성공: {ok}, 실패: {fail} 🎉", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
