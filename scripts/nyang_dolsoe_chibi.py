"""냥냥돌쇠 치비/SD 버전 10장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_nyang_dolsoe_chibi"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHAR = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes, facial mole, mole under eye"
NEG = "moles on body, mole on forehead, mole on nose"

JOBS = [
    {"prompt": f"{CHAR}, cat hood, paws up, sitting, cute, white background", "alias": "cb01_cathood", "style": "chibi_sketch"},
    {"prompt": f"{CHAR}, oversized hoodie, sleepy, holding pillow, white background", "alias": "cb02_sleepy", "style": "chibi_sketch"},
    {"prompt": f"{CHAR}, school uniform, bag, running late, toast in mouth, white background", "alias": "cb03_late", "style": "chibi_sketch"},
    {"prompt": f"{CHAR}, maid outfit, serving tea, smile, white background", "alias": "cb04_maid", "style": "chibi_sketch"},
    {"prompt": f"{CHAR}, winter coat, scarf, snow, cold, puffed cheeks, white background", "alias": "cb05_winter", "style": "chibi_sketch"},
    {"prompt": f"{CHAR}, pajamas, blanket cape, grumpy morning, white background", "alias": "cb06_grumpy", "style": "chibi_sketch"},
    {"prompt": f"{CHAR}, suit, tiny briefcase, serious face, cute, white background", "alias": "cb07_office", "style": "chibi_sketch"},
    {"prompt": f"{CHAR}, apron, cooking, frying pan, fire, panicking, white background", "alias": "cb08_cook", "style": "chibi_sketch"},
    {"prompt": f"{CHAR}, gym clothes, dumbbell, struggling, sweat, white background", "alias": "cb09_gym", "style": "chibi_sketch"},
    {"prompt": f"{CHAR}, detective coat, magnifying glass, smug, white background", "alias": "cb10_detect", "style": "chibi_sketch"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 1024,
        "height": 1024,
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
    print(f"냥냥돌쇠 치비 버전 {TOTAL}장", flush=True)
    print(f"프리셋: chibi_sketch", flush=True)
    print(f"해상도: 1024x1024 (정사각)", flush=True)
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
