"""모노가타리 시리즈 캐릭터 배치 (100장)
다양한 캐릭터 + 다양한 씬
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_batch"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 캐릭터 정의
HITAGI = "senjougahara hitagi, monogatari, purple hair, long hair, blue eyes"
TSUBASA = "hanekawa tsubasa, monogatari, black hair, long hair, glasses, purple eyes"
SHINOBU = "oshino shinobu, monogatari, blonde hair, long hair, yellow eyes, pointy ears"
MAYOI = "hachikuji mayoi, monogatari, black hair, twintails, red eyes, backpack"
SURUGA = "kanbaru suruga, monogatari, short hair, dark blue hair, brown eyes"
NADEKO = "sengoku nadeko, monogatari, orange hair, long hair, red eyes, bangs"
TSUKIHI = "araragi tsukihi, monogatari, black hair, long hair, hair ornament"
KAREN = "araragi karen, monogatari, black hair, ponytail, tall"
YOTSUGI = "ononoki yotsugi, monogatari, green hair, short hair, expressionless, hat"
SODACHI = "oikura sodachi, monogatari, blonde hair, twintails, blue eyes"
KISSSHOT = "kiss-shot acerola-orion heart-under-blade, monogatari, blonde hair, very long hair, red eyes, vampire"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

STYLES = ["pale_aqua", "waterful"]

# 씬 정의
SCENES = [
    "standing, school uniform, classroom, window, sunlight",
    "sitting, cafe, coffee, reading, relaxed",
    "night, street, city lights, walking",
    "bedroom, casual clothes, relaxing",
    "rooftop, sunset, wind, hair flowing",
    "rain, umbrella, street, wet",
    "shrine, torii, traditional",
    "park, bench, spring, cherry blossoms",
    "library, books, quiet, studying",
    "summer, yukata, festival, night",
]

CHARACTERS = [
    ("hitagi", HITAGI),
    ("tsubasa", TSUBASA),
    ("shinobu", SHINOBU),
    ("mayoi", MAYOI),
    ("suruga", SURUGA),
    ("nadeko", NADEKO),
    ("tsukihi", TSUKIHI),
    ("karen", KAREN),
    ("yotsugi", YOTSUGI),
    ("sodachi", SODACHI),
]

JOBS = []
idx = 1

# 각 캐릭터당 10장씩 (10캐릭터 x 10장 = 100장)
for char_alias, char_tags in CHARACTERS:
    for i, scene in enumerate(SCENES):
        style = STYLES[i % 2]
        JOBS.append({
            "prompt": f"1girl, {char_tags}, {scene}",
            "alias": f"{char_alias}_{idx:03d}",
            "style": style,
        })
        idx += 1

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
    print("모노가타리 시리즈 캐릭터 배치 100장", flush=True)
    print("히타기/츠바사/시노부/마요이/스루가/나데코/츠키히/카렌/요츠기/소다치", flush=True)
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
