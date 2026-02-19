"""바니걸 컨셉 100장 - 케이온 제외 버전"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_bunny_girl_no_keion"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BUNNY_BASE = "bunny girl, playboy bunny, leotard, bow tie, rabbit ears, wrist cuffs, fishnet pantyhose"

# 캐릭터 정의 (케이온 제외)
CHARACTERS = [
    # 모노가타리 시리즈 (13명)
    ("hitagi", "senjougahara hitagi, monogatari, long purple hair, sharp eyes"),
    ("hanekawa", "hanekawa tsubasa, monogatari, black hair, braids, glasses"),
    ("black_hanekawa", "black hanekawa, monogatari, white hair, cat ears, golden eyes"),
    ("shinobu", "oshino shinobu, monogatari, blonde hair, golden eyes, vampire"),
    ("nadeko", "sengoku nadeko, monogatari, orange hair, bangs, shy"),
    ("kanbaru", "kanbaru suruga, monogatari, short dark hair, athletic"),
    ("hachikuji", "hachikuji mayoi, monogatari, twintails, backpack"),
    ("karen", "araragi karen, monogatari, long black hair, ponytail, tall"),
    ("tsukihi", "araragi tsukihi, monogatari, short black hair, kimono style"),
    ("sodachi", "oikura sodachi, monogatari, light brown hair, twintails, sharp eyes"),
    ("ougi", "oshino ougi, monogatari, short black hair, mysterious"),
    ("gaen", "gaen izuko, monogatari, short hair, confident, mature"),
    ("yotsugi", "ononoki yotsugi, monogatari, green hair, hat, expressionless"),

    # 봇치더록 성인 3명
    ("seika", "ijichi seika, bocchi the rock, blue hair, short hair, older sister, mature"),
    ("pa_san", "pa-san, bocchi the rock, black hair, green eyes, labret piercing, mature woman, ponytail"),
    ("kikuri", "hiroi kikuri, bocchi the rock, red hair, drunk, mature, messy"),

    # 프리렌
    ("frieren", "frieren, sousou no frieren, white hair, elf ears, calm"),
    ("fern", "fern, sousou no frieren, purple hair, twintails, determined"),

    # 체인소맨
    ("power", "power, chainsaw man, blonde hair, horns, wild"),
    ("makima", "makima, chainsaw man, red hair, ringed eyes, calm"),
    ("reze", "reze, chainsaw man, dark hair, bob cut, gentle smile"),
    ("himeno", "himeno, chainsaw man, black hair, eyepatch, mature, cool"),

    # 스파이패밀리
    ("yor", "yor forger, spy x family, long black hair, red eyes, elegant"),

    # 원피스
    ("robin", "nico robin, one piece, black hair, elegant, mystery, mature"),
    ("nami", "nami, one piece, orange hair, confident, sexy"),

    # 최애의 아이
    ("ai", "hoshino ai, oshi no ko, purple hair, star eyes, idol"),
    ("ruby", "hoshino ruby, oshi no ko, blonde hair, star eyes, idol"),

    # 에반게리온
    ("asuka", "asuka langley, evangelion, red hair, blue eyes, tsundere"),
    ("rei", "rei ayanami, evangelion, blue hair, short hair, calm"),
    ("misato", "katsuragi misato, evangelion, black hair, mature, cool"),

    # 기타 인기 캐릭터
    ("violet", "violet evergarden, blonde hair, blue eyes, prosthetic hands, elegant"),
    ("rem", "rem, re:zero, blue hair, maid, devoted"),
    ("megumin", "megumin, konosuba, brown hair, red eyes, witch"),
    ("zerotwo", "zero two, darling in the franxx, pink hair, horns"),
    ("nezuko", "nezuko kamado, demon slayer, pink eyes, bamboo"),
    ("chika", "chika fujiwara, kaguya-sama, silver hair, ribbon, cheerful"),
    ("kaguya", "kaguya shinomiya, kaguya-sama, black hair, ribbon, elegant"),

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

# 37 캐릭터 x 2-3장씩 = 약 100장
# 모노가타리 주역(히타기, 하네카와, 시노부) 4장, 나머지 3장 or 2장
for char_idx, (alias, char_tags) in enumerate(CHARACTERS):
    # 모노가타리 주역 3명은 4장
    if alias in ["hitagi", "hanekawa", "shinobu"]:
        num_variants = 4
    # 모노가타리 나머지 + 봇치 성인 3명 = 3장
    elif char_idx < 16:
        num_variants = 3
    # 나머지는 2-3장
    else:
        num_variants = 3 if char_idx % 2 == 0 else 2

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
    print(f"바니걸 컨셉 {TOTAL}장 생성 (케이온 제외)", flush=True)
    print(f"모노가타리 13명 + 봇치 성인 3명 + 기타 21명", flush=True)
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
