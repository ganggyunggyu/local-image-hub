"""PA상 피어싱 배치 (100장)"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pa_batch_100"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PA = "pa-san, black hair, green eyes, labret piercing, ear piercing"
NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

SCENES = [
    "headphones, mixing console, studio, focused",
    "arms crossed, live house, backstage, cool",
    "coffee, cafe, reading, quiet",
    "goth fashion, black dress, choker, standing",
    "night, street, city lights, cool expression",
    "headphones around neck, smiling, casual",
    "sitting, bench, park, relaxed",
    "looking at viewer, close up, portrait",
    "side profile, wind, hair flowing",
    "night club, neon lights, cool",
    "holding phone, texting, train station",
    "leaning on wall, alley, night",
    "listening to music, eyes closed, peaceful",
    "black cardigan, grey dress, standing",
    "rooftop, sunset, looking away",
    "bar counter, drink, relaxed",
    "concert hall, spotlight, stage",
    "rainy day, umbrella, street",
    "record store, browsing, vinyl",
    "studio booth, microphone, working",
]

STYLES = ["pale_aqua", "watercolor_sketch"]

JOBS = []
idx = 1
for style in STYLES:
    for scene in SCENES:
        for _ in range(5 if style == "pale_aqua" else 5):
            if idx > 100:
                break
            JOBS.append({
                "prompt": f"1girl, {PA}, {scene}",
                "alias": f"pa{idx:03d}",
                "style": style,
            })
            idx += 1
        if idx > 100:
            break
    if idx > 100:
        break

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
    print("PA상 피어싱 배치 100장", flush=True)
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
