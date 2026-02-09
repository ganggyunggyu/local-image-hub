"""봇치더락 서브캐릭터 개인샷 (9장)
키쿠리 3장 / PA상 3장 / 세이카 3장
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_bocchi_side_solo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

KIKURI = "hiroi kikuri, pink hair, purple eyes, side braid"
PA = "pa-san, black hair, green eyes, labret piercing, ear piercing"
SEIKA = "ijichi seika, blonde hair, red eyes, ahoge"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    # 키쿠리 3장
    {
        "prompt": f"1girl, {KIKURI}, bass guitar, stage, spotlight, cool, playing",
        "alias": "kik01_stage",
        "style": "pale_aqua",
    },
    {
        "prompt": f"1girl, {KIKURI}, drunk, bar counter, beer, smiling, night",
        "alias": "kik02_bar",
        "style": "pale_aqua",
    },
    {
        "prompt": f"1girl, {KIKURI}, sukajan jacket, street, night, city lights, cool",
        "alias": "kik03_street",
        "style": "watercolor_sketch",
    },
    # PA상 3장
    {
        "prompt": f"1girl, {PA}, headphones, mixing console, studio, focused",
        "alias": "pa01_studio",
        "style": "pale_aqua",
    },
    {
        "prompt": f"1girl, {PA}, arms crossed, live house, backstage, cool",
        "alias": "pa02_backstage",
        "style": "pale_aqua",
    },
    {
        "prompt": f"1girl, {PA}, coffee, morning, cafe, reading, quiet",
        "alias": "pa03_cafe",
        "style": "watercolor_sketch",
    },
    # 세이카 3장
    {
        "prompt": f"1girl, {SEIKA}, microphone, announcing, stage, spotlight",
        "alias": "sei01_mc",
        "style": "pale_aqua",
    },
    {
        "prompt": f"1girl, {SEIKA}, office clothes, desk, working, serious",
        "alias": "sei02_office",
        "style": "pale_aqua",
    },
    {
        "prompt": f"1girl, {SEIKA}, casual clothes, rooftop, sunset, wind, smiling",
        "alias": "sei03_rooftop",
        "style": "watercolor_sketch",
    },
]

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
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} [{job['style']}] (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print("봇치더락 서브캐릭 개인샷 9장", flush=True)
    print("키쿠리 3장 / PA상 3장 / 세이카 3장", flush=True)
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
