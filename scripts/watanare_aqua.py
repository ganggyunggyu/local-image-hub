"""무리무리! (와타나레) 캐릭터 pale_aqua 10장
내가 연인이 될 수 있을 리 없잖아, 무리무리!
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_watanare_aqua"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === 캐릭터 정의 (작품명 + 캐릭터명 + 비주얼 태그) ===
SERIES = "watanare"
RENAKO = f"{SERIES}, amaori renako, pink hair, short hair, bob cut, purple eyes, x hair ornament, hairclip"
MAI = f"{SERIES}, oozuka mai, blonde hair, very long hair, blue eyes, sidelocks"
AJISAI = f"{SERIES}, sena ajisai, light brown hair, long hair, wavy hair, brown eyes"
SATSUKI = f"{SERIES}, koto satsuki, black hair, very long hair, red eyes, sidelocks"
KAHO = f"{SERIES}, koyanagi kaho, blue hair, long hair, yellow eyes, single hair bun, yellow ribbon"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    # 솔로 5장 (캐릭터당 1장)
    {
        "prompt": f"1girl, {RENAKO}, school uniform, blazer, looking at viewer, classroom, morning light, smile",
        "alias": "wt01_renako",
        "w": 832, "h": 1216,
    },
    {
        "prompt": f"1girl, {MAI}, white dress, model pose, elegant, wind, hair blowing, city background",
        "alias": "wt02_mai",
        "w": 832, "h": 1216,
    },
    {
        "prompt": f"1girl, {AJISAI}, cardigan, gentle smile, flower garden, hydrangea, soft light",
        "alias": "wt03_ajisai",
        "w": 832, "h": 1216,
    },
    {
        "prompt": f"1girl, {SATSUKI}, turtleneck, library, reading book, dim light, composed, cool beauty",
        "alias": "wt04_satsuki",
        "w": 832, "h": 1216,
    },
    {
        "prompt": f"1girl, {KAHO}, hoodie, peace sign, cheerful, convenience store, night, snacks",
        "alias": "wt05_kaho",
        "w": 832, "h": 1216,
    },
    # 투샷 3장
    {
        "prompt": f"2girls, multiple girls, girl on left {RENAKO} nervous, girl on right {MAI} smiling, holding hands, school corridor, afternoon",
        "alias": "wt06_renako_mai",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"2girls, multiple girls, girl on left {AJISAI} gentle smile, girl on right {SATSUKI} looking away, bench, cherry blossoms, spring",
        "alias": "wt07_ajisai_satsuki",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"2girls, multiple girls, girl on left {RENAKO} laughing, girl on right {KAHO} excited, selfie pose, phone, cafe",
        "alias": "wt08_renako_kaho",
        "w": 1024, "h": 1024,
    },
    # 그룹 2장
    {
        "prompt": f"3girls, multiple girls, {RENAKO}, {MAI}, {AJISAI}, school uniform, group photo, rooftop, blue sky, wind",
        "alias": "wt09_trio",
        "w": 1216, "h": 832,
    },
    {
        "prompt": f"5girls, multiple girls, {RENAKO}, {MAI}, {AJISAI}, {SATSUKI}, {KAHO}, casual clothes, picnic, park, blanket, food, laughing",
        "alias": "wt10_all5",
        "w": 1216, "h": 832,
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": job["w"],
        "height": job["h"],
        "model": "animagine-xl-4",
        "style": "pale_aqua",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print("무리무리! (와타나레) pale_aqua 10장", flush=True)
    print(f"레나코 / 마이 / 아지사이 / 사츠키 / 카호", flush=True)
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
