"""바니걸 컨셉 100장 - 다양한 캐릭터 x 프리셋"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_bunny_girl_100"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BUNNY_BASE = "bunny girl, playboy bunny, leotard, bow tie, rabbit ears, wrist cuffs, fishnet pantyhose"

# 캐릭터 정의 (다양한 작품)
CHARACTERS = [
    # 모노가타리
    ("hitagi", "senjougahara hitagi, monogatari, long purple hair, sharp eyes"),
    ("hanekawa", "hanekawa tsubasa, monogatari, black hair, braids, glasses"),
    ("shinobu", "oshino shinobu, monogatari, blonde hair, golden eyes, vampire"),
    ("nadeko", "sengoku nadeko, monogatari, orange hair, bangs, shy"),
    ("kanbaru", "kanbaru suruga, monogatari, short dark hair, athletic"),

    # 케이온
    ("yui", "hirasawa yui, k-on!, brown short hair, brown eyes, cheerful"),
    ("mio", "akiyama mio, k-on!, black long hair, grey eyes, shy"),
    ("ritsu", "tainaka ritsu, k-on!, brown short hair, headband, energetic"),
    ("mugi", "kotobuki tsumugi, k-on!, blonde long hair, blue eyes, elegant"),
    ("azusa", "nakano azusa, k-on!, black twintails, red eyes"),

    # 프리렌
    ("frieren", "frieren, sousou no frieren, white hair, elf ears, calm"),
    ("fern", "fern, sousou no frieren, purple hair, twintails, determined"),

    # 체인소맨
    ("power", "power, chainsaw man, blonde hair, horns, wild"),
    ("makima", "makima, chainsaw man, red hair, ringed eyes, calm"),
    ("reze", "reze, chainsaw man, dark hair, bob cut, gentle smile"),

    # 보치더록
    ("bocchi", "gotou hitori, bocchi the rock, pink hair, shy, nervous"),
    ("nijika", "ijichi nijika, bocchi the rock, blonde hair, cheerful"),
    ("ryo", "yamada ryo, bocchi the rock, blue hair, cool, composed"),
    ("kita", "kita ikuyo, bocchi the rock, red hair, sparkling, happy"),

    # 스파이패밀리
    ("yor", "yor forger, spy x family, long black hair, red eyes, elegant"),

    # 기타 인기 캐릭터
    ("violet", "violet evergarden, blonde hair, blue eyes, prosthetic hands"),
    ("rem", "rem, re:zero, blue hair, maid"),
    ("megumin", "megumin, konosuba, brown hair, red eyes, witch"),
    ("asuka", "asuka langley, evangelion, red hair, blue eyes, tsundere"),
    ("rei", "rei ayanami, evangelion, blue hair, short hair, calm"),
    ("zerotwo", "zero two, darling in the franxx, pink hair, horns"),
    ("nezuko", "nezuko kamado, demon slayer, pink eyes, bamboo"),
    ("ai", "hoshino ai, oshi no ko, purple hair, star eyes, idol"),
    ("ruby", "hoshino ruby, oshi no ko, blonde hair, star eyes, idol"),

    # 냥냥돌쇠
    ("dolsoe", "cat ears, cat tail, dark blue hair, bob cut, amber eyes"),
]

# 프리셋 (잘 뽑히는 순)
PRESETS = [
    "monogatari", "blue_archive", "kyoto_animation", "pale_aqua",
    "mono_halftone", "pop_fanart", "trigger", "pastel_soft",
    "watercolor_sketch", "ghibli", "shinkai", "mappa",
    "fate", "cyberpunk", "ufotable", "shaft",
]

# 포즈/상황
POSES = [
    "standing, looking at viewer, confident smile, upper body",
    "sitting on bar stool, crossed legs, seductive, upper body",
    "winking, peace sign, playful, upper body",
    "serving drinks, tray, professional, upper body",
    "leaning forward, hand on hip, flirty, upper body",
    "back view, looking over shoulder, elegant, upper body",
    "kneeling, bunny pose, cute, full body",
    "jumping, energetic, cheerful, full body",
    "shy, blushing, embarrassed, upper body",
    "confident, smirking, hand on chest, upper body",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy, bad hands"

JOBS = []

# 30 캐릭터 x 3-4장씩 = 약 100장
for char_idx, (alias, char_tags) in enumerate(CHARACTERS):
    # 각 캐릭터당 3-4개 조합
    num_variants = 4 if char_idx < 5 else 3  # 모노가타리 주역들은 4장, 나머지 3장

    for variant_idx in range(num_variants):
        preset = PRESETS[(char_idx + variant_idx) % len(PRESETS)]
        pose = POSES[(char_idx * 2 + variant_idx) % len(POSES)]

        job_idx = len(JOBS) + 1
        JOBS.append({
            "prompt": f"1girl, {char_tags}, {BUNNY_BASE}, {pose}",
            "style": preset,
            "name": f"bunny_{job_idx:03d}_{alias}_{preset}",
        })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, idx: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece",
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
    print(f"바니걸 컨셉 {TOTAL}장 생성", flush=True)
    print(f"캐릭터 {len(CHARACTERS)}명 x 다양한 프리셋/포즈", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)
    print("=" * 60, flush=True)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60, flush=True)
    print(f"완료! 성공: {ok}, 실패: {fail}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
