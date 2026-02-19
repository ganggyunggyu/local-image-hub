"""모노가타리 프리셋 고정 + 바니걸 300장"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_preset_bunny_300"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BUNNY_BASE = "bunny girl, playboy bunny, leotard, bow tie, rabbit ears, wrist cuffs, fishnet pantyhose"
STYLE = "monogatari"  # 모노가타리 프리셋 고정!

# 모노가타리 전 캐릭터 (13명 - 아라라기 제외)
CHARACTERS = [
    ("hitagi", "senjougahara hitagi, monogatari, long purple hair, sharp eyes, tsundere"),
    ("hitagi_short", "senjougahara hitagi, monogatari, short purple hair, bob cut, sharp eyes, tsundere"),
    ("hanekawa", "hanekawa tsubasa, monogatari, black hair, braids, glasses, gentle"),
    ("black_hanekawa", "black hanekawa, monogatari, white hair, cat ears, golden eyes, seductive"),
    ("shinobu", "oshino shinobu, monogatari, blonde hair, golden eyes, vampire, loli"),
    ("nadeko", "sengoku nadeko, monogatari, orange hair, bangs, shy, cute"),
    ("kanbaru", "kanbaru suruga, monogatari, short dark hair, athletic, tomboy"),
    ("hachikuji", "hachikuji mayoi, monogatari, twintails, backpack, ghost girl"),
    ("karen", "araragi karen, monogatari, long black hair, ponytail, tall, martial arts"),
    ("tsukihi", "araragi tsukihi, monogatari, short black hair, kimono style, cute"),
    ("sodachi", "oikura sodachi, monogatari, light brown hair, twintails, sharp eyes, angry"),
    ("ougi", "oshino ougi, monogatari, short black hair, mysterious, dark, enigmatic"),
    ("gaen", "gaen izuko, monogatari, short hair, confident, mature"),
    ("yotsugi", "ononoki yotsugi, monogatari, green hair, hat, expressionless, doll"),
]

# 포즈/표정/상황 (엄청 다양하게 50종+)
POSES = [
    # 스탠딩 기본
    "standing, looking at viewer, confident smile, hand on hip, head tilt, upper body",
    "standing, arms crossed, smirking, cool, sharp gaze, upper body",
    "standing, peace sign, winking, playful, cheerful, upper body",
    "standing, hand on chest, flirty, seductive smile, upper body",
    "standing, finger to lips, mysterious, quiet gesture, upper body",
    "standing, arms behind back, innocent, shy smile, upper body",
    "standing, hand reaching out, inviting, welcoming gesture, upper body",
    "standing, victory pose, both hands v sign, energetic, upper body",
    "standing, salute pose, playful, military style, upper body",
    "standing, hand on hip, confident, proud, chest out, upper body",

    # 앉기 포즈
    "sitting on bar stool, crossed legs, seductive, elegant, looking at viewer, upper body",
    "sitting on floor, legs to side, relaxed, cute, gentle smile, full body",
    "sitting with legs crossed, composed, elegant, serious, upper body",
    "sitting backwards on chair, arms on backrest, cool, casual, upper body",
    "sitting on table edge, swinging legs, playful, cheerful, upper body",
    "sitting hugging knees, shy, vulnerable, looking down, full body",
    "kneeling, bunny pose, hands up, cute, cheerful, full body",
    "kneeling, sitting on heels, elegant, formal, upper body",

    # 동작 포즈
    "jumping, energetic, cheerful, dynamic, both arms up, full body",
    "twirling, spinning, dress flowing, graceful, dynamic, full body",
    "walking towards viewer, confident stride, cool, full body",
    "leaning forward, hand on table, flirty, teasing, upper body",
    "leaning against wall, casual, cool, relaxed, upper body",
    "back view, looking over shoulder, mysterious, elegant, upper body",
    "stretching, arms up, yawning, casual, lazy, upper body",
    "bending forward, adjusting stockings, sensual, elegant, full body",

    # 손 포즈
    "hand on chin, thinking pose, curious, intelligent, upper body",
    "adjusting bunny ears, fixing costume, cute, preparing, upper body",
    "holding champagne glass, elegant, sophisticated, toast, upper body",
    "serving drinks on tray, professional, smiling, waitress, upper body",
    "blowing kiss, flirty, playful, romantic, upper body",
    "covering mouth with hand, laughing, joyful, giggling, upper body",
    "touching bunny ear, cute, curious, playful, upper body",
    "hand behind head, relaxed, casual, cool, upper body",
    "hands on hips, confident, assertive, strong, upper body",
    "checking nails, nonchalant, cool, casual, upper body",
    "fixing bow tie, preparing, professional, adjusting, upper body",
    "hair flip, glamorous, confident, shiny hair, upper body",

    # 표정 중심
    "looking at viewer, gentle smile, warm, kind, soft lighting, upper body",
    "looking at viewer, mischievous smile, plotting, scheming, upper body",
    "looking at viewer, embarrassed, red face, blushing, flustered, upper body",
    "looking at viewer, surprised, eyes wide, shock, mouth open, upper body",
    "looking at viewer, sleepy, tired, lazy, half-closed eyes, upper body",
    "looking at viewer, serious, intense gaze, dramatic, sharp eyes, upper body",
    "looking at viewer, happy, bright smile, sparkling eyes, cheerful, upper body",
    "looking at viewer, sad, teary eyes, emotional, melancholic, upper body",
    "looking at viewer, angry, puffed cheeks, annoyed, frustrated, upper body",
    "looking at viewer, confident, proud, superior smile, upper body",
    "looking at viewer, shy, looking away, nervous, timid, upper body",

    # 특수 포즈
    "looking down, demure, shy, modest, upper body",
    "looking up, hopeful, dreamy, longing, upper body",
    "head tilt, cute, curious, questioning, upper body",
    "curtsy, elegant, formal, graceful, full body",
    "stretching one leg, flexible, graceful, ballet pose, full body",

    # 추가 바리에이션
    "winking, tongue out, playful, mischievous, upper body",
    "arms spread wide, welcoming, open, happy, upper body",
    "one hand on hip, other hand waving, greeting, friendly, upper body",
    "hugging self, shy, embarrassed, cute, upper body",
    "fidgeting with hands, nervous, anxious, cute, upper body",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, fused fingers"

JOBS = []

# 14 캐릭터 x 21-22장씩 = 약 300장
# 주연급(히타기, 히타기숏컷, 하네카와, 블랙하네카와, 시노부) 각 25장
# 나머지 각 20장
for char_idx, (alias, char_tags) in enumerate(CHARACTERS):
    if alias in ["hitagi", "hitagi_short", "hanekawa", "black_hanekawa", "shinobu"]:
        num_variants = 25
    else:
        num_variants = 20

    for variant_idx in range(num_variants):
        pose = POSES[variant_idx % len(POSES)]

        job_idx = len(JOBS) + 1
        JOBS.append({
            "prompt": f"1girl, {char_tags}, {BUNNY_BASE}, {pose}",
            "name": f"mono_preset_bunny_{job_idx:03d}_{alias}_{variant_idx+1:02d}",
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
        "style": STYLE,
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
    print(f"🎀 모노가타리 프리셋 고정 바니걸 {TOTAL}장! 🎀", flush=True)
    print(f"스타일: {STYLE} (고정)", flush=True)
    print(f"캐릭터 14명 x 다양한 포즈", flush=True)
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
