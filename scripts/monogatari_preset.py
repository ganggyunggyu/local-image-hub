"""모노가타리 시리즈 프리셋별 배치 (100장)
pale_aqua 34장 + waterful 33장 + watercolor_sketch 33장
캐릭터 골고루 분배
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_preset"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 캐릭터 정의
CHARS = {
    "yotsugi": "ononoki yotsugi, monogatari, green hair, short hair, expressionless, orange hat, orange eyes",
    "hitagi": "senjougahara hitagi, monogatari, purple hair, long hair, blue eyes",
    "tsubasa": "hanekawa tsubasa, monogatari, black hair, long hair, glasses, purple eyes",
    "shinobu": "oshino shinobu, monogatari, blonde hair, long hair, yellow eyes, pointy ears",
    "mayoi": "hachikuji mayoi, monogatari, black hair, twintails, red eyes, backpack",
    "suruga": "kanbaru suruga, monogatari, short hair, dark blue hair, brown eyes",
    "nadeko": "sengoku nadeko, monogatari, orange hair, long hair, red eyes, bangs",
    "tsukihi": "araragi tsukihi, monogatari, black hair, long hair, hair ornament",
    "karen": "araragi karen, monogatari, black hair, ponytail, tall",
    "sodachi": "oikura sodachi, monogatari, blonde hair, twintails, blue eyes",
}

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

# 씬 정의
SCENES = [
    "standing, school uniform, classroom, window, sunlight",
    "sitting, cafe, coffee, reading, relaxed",
    "night, street, city lights, walking",
    "rooftop, sunset, wind, hair flowing",
    "rain, umbrella, street, wet",
    "summer, yukata, festival, night",
    "spring, cherry blossoms, wind, petals",
    "winter, snow, coat, scarf",
    "bedroom, casual clothes, relaxing",
    "library, books, quiet, studying",
    "shrine, torii, traditional",
    "beach, ocean, summer, swimsuit",
    "park, bench, autumn leaves",
    "train station, platform, waiting",
    "night sky, stars, looking up",
    "close up, portrait, looking at viewer",
    "full body, standing, white background",
]

PRESETS = ["pale_aqua", "waterful", "watercolor_sketch"]
CHAR_NAMES = list(CHARS.keys())

JOBS = []

# 프리셋별로 정리 (각 프리셋당 33-34장)
for preset_idx, preset in enumerate(PRESETS):
    count = 34 if preset_idx == 0 else 33
    for i in range(count):
        char_name = CHAR_NAMES[i % len(CHAR_NAMES)]
        scene = SCENES[i % len(SCENES)]
        job_idx = len(JOBS) + 1
        JOBS.append({
            "prompt": f"1girl, {CHARS[char_name]}, {scene}",
            "alias": f"{preset}_{char_name}_{job_idx:03d}",
            "style": preset,
        })

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 832,
        "height": 1216,
        "model": "animagine-xl-4",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:03d}/{TOTAL}] OK {job['alias']} [{job['style']}] (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:03d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:03d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print("모노가타리 시리즈 프리셋별 배치 100장", flush=True)
    print("pale_aqua 34장 + waterful 33장 + watercolor_sketch 33장", flush=True)
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
    print(f"저장: {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
