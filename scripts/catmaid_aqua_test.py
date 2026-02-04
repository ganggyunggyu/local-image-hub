"""pale_aqua 프리셋 - 고양이귀 메이드 10장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_catmaid_aqua"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {
        "prompt": "1girl, cat ears, cat tail, maid outfit, white apron, black dress, silver hair, long hair, blue eyes, holding tray, gentle smile, indoor, looking at viewer, upper body",
        "alias": "catmaid_silver",
    },
    {
        "prompt": "1girl, cat ears, cat tail, maid outfit, frilly apron, pink hair, twintails, green eyes, arms behind back, cheerful, tilting head, simple background",
        "alias": "catmaid_pink",
    },
    {
        "prompt": "1girl, cat ears, cat tail, maid headdress, maid outfit, black hair, short hair, golden eyes, face close-up, slight smile, looking at viewer, portrait",
        "alias": "catmaid_black_closeup",
    },
    {
        "prompt": "1girl, cat ears, cat tail, maid outfit, white thighhighs, blonde hair, long hair, blue eyes, hugging pillow to chest, sitting on bed, cozy, soft light",
        "alias": "catmaid_blonde_cozy",
    },
    {
        "prompt": "1girl, cat ears, cat tail, maid outfit, frilly headband, white hair, red eyes, arms crossed, cool expression, looking at viewer, elegant interior, upper body",
        "alias": "catmaid_white_cool",
    },
    {
        "prompt": "1girl, cat ears, cat tail, maid outfit, apron, blue hair, short hair, purple eyes, hands clasped in front, shy, blush, flower vase, window light",
        "alias": "catmaid_blue_shy",
    },
    {
        "prompt": "1girl, cat ears, cat tail, maid outfit, long sleeves, lavender hair, long hair, heterochromia, face close-up, wink, playful, portrait",
        "alias": "catmaid_lavender_wink",
    },
    {
        "prompt": "1girl, cat ears, cat tail, maid outfit, apron, brown hair, braids, amber eyes, holding broom, standing, full body, wooden floor, warm interior",
        "alias": "catmaid_brown_broom",
    },
    {
        "prompt": "1girl, cat ears, cat tail, gothic maid outfit, black frills, silver hair, long hair, red eyes, sitting on ornate chair, legs crossed, elegant, dark interior, candles",
        "alias": "catmaid_gothic",
    },
    {
        "prompt": "1girl, cat ears, cat tail, maid outfit, white apron, light green hair, ponytail, green eyes, hands behind back, looking over shoulder, garden background, sunlight",
        "alias": "catmaid_green_garden",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "",
        "width": 832,
        "height": 1216,
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
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"고양이귀 메이드 x pale_aqua 테스트 {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
