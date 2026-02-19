"""모노가타리 3대장 바니걸 200장 - 히타기 숏컷 포함!"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_top3_bunny_200"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BUNNY_BASE = "bunny girl, playboy bunny, leotard, bow tie, rabbit ears, wrist cuffs, fishnet pantyhose"

# 모노가타리 3대장 + 히타기 숏컷
CHARACTERS = [
    ("hitagi_long", "senjougahara hitagi, monogatari, long purple hair, sharp eyes, tsundere, stapler"),
    ("hitagi_short", "senjougahara hitagi, monogatari, short purple hair, bob cut, sharp eyes, tsundere"),
    ("hanekawa", "hanekawa tsubasa, monogatari, black hair, braids, glasses, gentle, class president"),
    ("black_hanekawa", "black hanekawa, monogatari, white hair, cat ears, golden eyes, seductive, tress"),
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

# 포즈/표정/상황 (50종 - 엄청 다양하게!)
POSES = [
    # 기본 포즈
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

    # 앉은 포즈
    "sitting on floor, legs to side, relaxed, cute, full body",
    "sitting with legs crossed, elegant, composed, upper body",
    "sitting backwards on chair, arms on backrest, cool, upper body",
    "sitting on table edge, swinging legs, playful, upper body",
    "sitting hugging knees, shy, vulnerable, full body",

    # 손 포즈
    "stretching, arms up, yawning, casual, upper body",
    "hand on chin, thinking pose, curious, upper body",
    "adjusting bunny ears, fixing costume, preparing, upper body",
    "holding champagne glass, elegant, sophisticated, upper body",
    "blowing kiss, flirty, playful, romantic, upper body",
    "covering mouth with hand, laughing, joyful, upper body",
    "finger to lips, shh gesture, mysterious, upper body",
    "arms behind back, innocent, cute, upper body",
    "hand reaching out, inviting, welcoming, upper body",
    "touching bunny ear, cute, curious, upper body",

    # 표정 중심
    "serious expression, intense gaze, dramatic, upper body",
    "surprised, eyes wide, shock, cute, upper body",
    "sleepy, tired, lazy, relaxed, upper body",
    "happy, bright smile, sparkling eyes, upper body",
    "sad, teary eyes, emotional, upper body",
    "angry, puffed cheeks, annoyed, cute, upper body",
    "embarrassed, red face, flustered, upper body",
    "confident, proud, chest out, upper body",
    "mischievous, plotting, scheming smile, upper body",
    "gentle smile, warm, kind, upper body",

    # 동작
    "twirling, spinning, dress flowing, dynamic, full body",
    "walking towards viewer, confident stride, full body",
    "leaning against wall, casual, cool, upper body",
    "looking down, shy, demure, upper body",
    "looking up, hopeful, dreamy, upper body",
    "head tilt, cute, curious, upper body",
    "hair flip, glamorous, confident, upper body",
    "adjusting stockings, sensual, elegant, full body",
    "checking nails, nonchalant, cool, upper body",
    "fixing bow tie, preparing, professional, upper body",

    # 특수 포즈
    "victory pose, v sign with both hands, cheerful, upper body",
    "salute pose, playful, energetic, upper body",
    "curtsy, elegant, formal, full body",
    "stretching one leg, flexible, graceful, full body",
    "hand behind head, relaxed, casual, upper body",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, fused fingers"

JOBS = []

# 4명 x 50장씩 = 200장
for char_idx, (alias, char_tags) in enumerate(CHARACTERS):
    for variant_idx in range(50):
        preset = PRESETS[variant_idx % len(PRESETS)]
        pose = POSES[variant_idx % len(POSES)]

        job_idx = len(JOBS) + 1
        JOBS.append({
            "prompt": f"1girl, {char_tags}, {BUNNY_BASE}, {pose}",
            "style": preset,
            "name": f"top3_bunny_{job_idx:03d}_{alias}_{variant_idx+1:02d}_{preset}",
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
    print(f"💜 모노가타리 3대장 바니걸 {TOTAL}장! 💜", flush=True)
    print(f"히타기(롱) 50 + 히타기(숏컷) 50 + 하네카와 50 + 블랙하네카와 50", flush=True)
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
