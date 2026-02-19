"""모노가타리 시리즈 바니걸 300장 대폭발!!!"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_bunny_300"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BUNNY_BASE = "bunny girl, playboy bunny, leotard, bow tie, rabbit ears, wrist cuffs, fishnet pantyhose"

# 모노가타리 전 캐릭터 (14명 - 아라라기 포함)
CHARACTERS = [
    ("hitagi", "senjougahara hitagi, monogatari, long purple hair, sharp eyes, tsundere"),
    ("hanekawa", "hanekawa tsubasa, monogatari, black hair, braids, glasses, gentle"),
    ("black_hanekawa", "black hanekawa, monogatari, white hair, cat ears, golden eyes, seductive"),
    ("shinobu", "oshino shinobu, monogatari, blonde hair, golden eyes, vampire, loli"),
    ("nadeko", "sengoku nadeko, monogatari, orange hair, bangs, shy, cute"),
    ("kanbaru", "kanbaru suruga, monogatari, short dark hair, athletic, tomboy"),
    ("hachikuji", "hachikuji mayoi, monogatari, twintails, backpack, ghost girl"),
    ("karen", "araragi karen, monogatari, long black hair, ponytail, tall, martial arts"),
    ("tsukihi", "araragi tsukihi, monogatari, short black hair, kimono style, cute, phoenix"),
    ("sodachi", "oikura sodachi, monogatari, light brown hair, twintails, sharp eyes, angry"),
    ("ougi", "oshino ougi, monogatari, short black hair, mysterious, dark, enigmatic"),
    ("gaen", "gaen izuko, monogatari, short hair, confident, mature, expert"),
    ("yotsugi", "ononoki yotsugi, monogatari, green hair, hat, expressionless, doll"),
    ("araragi", "1boy, araragi koyomi, monogatari, black hair, ahoge, male"),
]

# 프리셋 전부 (27종)
PRESETS = [
    "monogatari", "pale_aqua", "mono_halftone", "chibi_sketch",
    "cozy_gouache", "watercolor_sketch", "kyoto_animation", "ufotable",
    "shinkai", "ghibli", "trigger", "mappa", "shaft",
    "genshin", "blue_archive", "arknights", "fate", "cyberpunk",
    "pastel_soft", "inuyasha", "sepia_backlit", "mono_accent",
    "sketch_colorpop", "pop_fanart", "split_sketch", "waterful",
    "retro_glitch",
]

# 포즈/표정/상황 (풍부하게)
POSES = [
    "standing, looking at viewer, confident smile, hand on hip, upper body",
    "sitting on bar stool, crossed legs, seductive, elegant, upper body",
    "winking, peace sign, playful, cheerful, upper body",
    "serving drinks on tray, professional, smiling, upper body",
    "leaning forward, hand on chest, flirty, teasing, upper body",
    "back view, looking over shoulder, mysterious, elegant, upper body",
    "kneeling, bunny pose, hands up, cute, full body",
    "jumping, energetic, cheerful, dynamic, full body",
    "shy, blushing, embarrassed, covering face, upper body",
    "confident, smirking, arms crossed, cool, upper body",
    "sitting on floor, legs to side, relaxed, cute, full body",
    "stretching, arms up, yawning, casual, upper body",
    "hand on chin, thinking pose, curious, upper body",
    "adjusting bunny ears, fixing costume, preparing, upper body",
    "holding champagne glass, elegant, sophisticated, upper body",
    "blowing kiss, flirty, playful, romantic, upper body",
    "laughing, hands covering mouth, joyful, upper body",
    "serious expression, intense gaze, dramatic, upper body",
    "surprised, eyes wide, shock, cute, upper body",
    "sleepy, tired, lazy, relaxed, upper body",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, fused fingers"

JOBS = []

# 14 캐릭터 x 21-22장씩 = 약 300장
# 주연급(히타기, 하네카와, 시노부) 25장, 나머지 20장
for char_idx, (alias, char_tags) in enumerate(CHARACTERS):
    # 주연 3명은 25장
    if alias in ["hitagi", "hanekawa", "shinobu"]:
        num_variants = 25
    # 블랙하네카와, 나데코, 칸바루 22장
    elif alias in ["black_hanekawa", "nadeko", "kanbaru"]:
        num_variants = 22
    # 나머지 20장
    else:
        num_variants = 20

    for variant_idx in range(num_variants):
        preset = PRESETS[variant_idx % len(PRESETS)]
        pose = POSES[variant_idx % len(POSES)]

        # 1girl/1boy 처리
        prefix = "1girl" if "1boy" not in char_tags else ""
        clean_tags = char_tags.replace("1boy, ", "")

        job_idx = len(JOBS) + 1
        prompt = f"{prefix}, {clean_tags}, {BUNNY_BASE}, {pose}" if prefix else f"{clean_tags}, {BUNNY_BASE}, {pose}"

        JOBS.append({
            "prompt": prompt.strip(", "),
            "style": preset,
            "name": f"mono_bunny_{job_idx:03d}_{alias}_{variant_idx+1:02d}_{preset}",
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
    print(f"🎀 모노가타리 시리즈 바니걸 {TOTAL}장 대폭발!!! 🎀", flush=True)
    print(f"캐릭터 14명 x 프리셋 27종 x 포즈 20종", flush=True)
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
