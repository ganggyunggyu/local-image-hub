"""모노가타리 시리즈 캐릭터 배치 (100장)
요츠기 40장 + 나머지 캐릭터 60장
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_yotsugi"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 캐릭터 정의
YOTSUGI = "ononoki yotsugi, monogatari, green hair, short hair, expressionless, orange hat, orange eyes"
HITAGI = "senjougahara hitagi, monogatari, purple hair, long hair, blue eyes"
TSUBASA = "hanekawa tsubasa, monogatari, black hair, long hair, glasses, purple eyes"
SHINOBU = "oshino shinobu, monogatari, blonde hair, long hair, yellow eyes, pointy ears"
MAYOI = "hachikuji mayoi, monogatari, black hair, twintails, red eyes, backpack"
SURUGA = "kanbaru suruga, monogatari, short hair, dark blue hair, brown eyes"
NADEKO = "sengoku nadeko, monogatari, orange hair, long hair, red eyes, bangs"
TSUKIHI = "araragi tsukihi, monogatari, black hair, long hair, hair ornament"
KAREN = "araragi karen, monogatari, black hair, ponytail, tall"
SODACHI = "oikura sodachi, monogatari, blonde hair, twintails, blue eyes"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

STYLES = ["pale_aqua", "waterful"]

# 요츠기 전용 씬 (40장)
YOTSUGI_SCENES = [
    "standing, expressionless, peace sign, white background",
    "sitting, reading, library, quiet",
    "night, street, moonlight, standing",
    "pointing finger, serious, close up",
    "arms crossed, expressionless, white background",
    "lying down, floor, relaxed, bored",
    "walking, street, daytime, casual",
    "rooftop, sunset, wind, hair flowing",
    "cafe, tea, sitting, expressionless",
    "shrine, torii, standing, traditional",
    "bedroom, sitting on bed, casual clothes",
    "rain, umbrella, street, standing",
    "park, bench, sitting, autumn leaves",
    "school uniform, classroom, standing",
    "spring, cherry blossoms, wind, petals",
    "winter, snow, coat, cold",
    "summer, sundress, bright, sunny",
    "night sky, stars, looking up",
    "bookstore, browsing, shelves",
    "convenience store, night, fluorescent light",
    "train station, platform, waiting",
    "bridge, river, sunset, leaning",
    "forest, trees, mysterious, standing",
    "beach, ocean, summer, wind",
    "festival, yukata, night, lanterns",
    "apartment, window, looking outside",
    "kitchen, cooking, apron, expressionless",
    "bath, onsen, steam, relaxed",
    "halloween, costume, pumpkin, night",
    "christmas, santa hat, winter, snow",
    "new year, shrine, kimono, traditional",
    "valentine, chocolate, heart, giving",
    "white day, candy, receiving, expressionless",
    "graduation, school uniform, cherry blossoms",
    "birthday, cake, candles, celebration",
    "sleepy, yawning, morning, pajamas",
    "angry, pouting, cute, close up",
    "curious, tilting head, questioning",
    "happy, slight smile, rare, precious",
    "cool, confident, stylish, pose",
]

# 다른 캐릭터 씬 (각 6장씩 = 60장)
OTHER_SCENES = [
    "standing, school uniform, classroom, window, sunlight",
    "sitting, cafe, coffee, reading, relaxed",
    "night, street, city lights, walking",
    "rooftop, sunset, wind, hair flowing",
    "rain, umbrella, street, wet",
    "summer, yukata, festival, night",
]

OTHER_CHARS = [
    ("hitagi", HITAGI),
    ("tsubasa", TSUBASA),
    ("shinobu", SHINOBU),
    ("mayoi", MAYOI),
    ("suruga", SURUGA),
    ("nadeko", NADEKO),
    ("tsukihi", TSUKIHI),
    ("karen", KAREN),
    ("sodachi", SODACHI),
    ("hitagi2", HITAGI),  # 히타기 추가 6장
]

JOBS = []
idx = 1

# 요츠기 40장
for i, scene in enumerate(YOTSUGI_SCENES):
    style = STYLES[i % 2]
    JOBS.append({
        "prompt": f"1girl, {YOTSUGI}, {scene}",
        "alias": f"yotsugi_{idx:03d}",
        "style": style,
    })
    idx += 1

# 다른 캐릭터 60장 (10캐릭터 x 6장)
for char_alias, char_tags in OTHER_CHARS:
    for i, scene in enumerate(OTHER_SCENES):
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
    print("요츠기 40장 + 나머지 캐릭터 60장", flush=True)
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
