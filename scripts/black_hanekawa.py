"""블랙 하네카와 배치 (20장)
과감한 의상 버전
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_black_hanekawa"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 블랙 하네카와 (원작 특징: 속옷/노출 의상)
BLACK = "black hanekawa, monogatari, white hair, long hair, golden eyes, slit pupils, cat ears, pale skin"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    {"prompt": f"1girl, {BLACK}, white lingerie, night, rooftop, moonlight, standing", "alias": "bh01", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, black bra, night, alley, mysterious, looking at viewer", "alias": "bh02", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, white underwear, bedroom, sitting on bed, night", "alias": "bh03", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, camisole, night, window, moon, standing", "alias": "bh04", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, nightgown, transparent, night, moonlight", "alias": "bh05", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, off shoulder, bare shoulders, night, street", "alias": "bh06", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, white slip dress, night, rooftop, wind", "alias": "bh07", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, tank top, shorts, night, casual, relaxed", "alias": "bh08", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, backless dress, night, elegant, looking back", "alias": "bh09", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, halter top, night, city lights, cool", "alias": "bh10", "style": "pale_aqua"},
    {"prompt": f"1girl, {BLACK}, white lingerie, close up, portrait, smirk", "alias": "bh11", "style": "waterful"},
    {"prompt": f"1girl, {BLACK}, black negligee, lying down, bed, night", "alias": "bh12", "style": "waterful"},
    {"prompt": f"1girl, {BLACK}, crop top, midriff, night, street, confident", "alias": "bh13", "style": "waterful"},
    {"prompt": f"1girl, {BLACK}, strapless dress, night, elegant, standing", "alias": "bh14", "style": "waterful"},
    {"prompt": f"1girl, {BLACK}, tube top, night, rooftop, wind, hair flowing", "alias": "bh15", "style": "waterful"},
    {"prompt": f"1girl, {BLACK}, white chemise, night, window, moonlight", "alias": "bh16", "style": "waterful"},
    {"prompt": f"1girl, {BLACK}, side slit dress, night, mysterious, walking", "alias": "bh17", "style": "waterful"},
    {"prompt": f"1girl, {BLACK}, bare back, night, looking over shoulder", "alias": "bh18", "style": "waterful"},
    {"prompt": f"1girl, {BLACK}, white sleepwear, bedroom, night, relaxed", "alias": "bh19", "style": "waterful"},
    {"prompt": f"1girl, {BLACK}, revealing outfit, night, confident, smirk", "alias": "bh20", "style": "waterful"},
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
    print("블랙 하네카와 배치 20장", flush=True)
    print("과감한 의상 버전", flush=True)
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
