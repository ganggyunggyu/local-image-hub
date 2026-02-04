"""pale_aqua 프리셋 테스트 배치"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pale_aqua_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    # === 손 회피 구도 (뒷짐, 팔짱, 주머니, 등 뒤) ===
    {
        "prompt": "1girl, frieren, sousou no frieren, white hair, long hair, elf ears, green eyes, mage robe, arms behind back, looking at viewer, flower meadow, close-up face, wind",
        "alias": "v2_frieren_behind",
    },
    {
        "prompt": "1boy, himmel, sousou no frieren, blue hair, short hair, blue eyes, hero armor, cape, arms crossed, confident smile, looking at viewer, sky background, upper body",
        "alias": "v2_himmel_crossed",
    },
    {
        "prompt": "1boy, himmel, sousou no frieren, blue hair, short hair, blue eyes, casual clothes, hands in pockets, walking, autumn path, leaves falling, nostalgic",
        "alias": "v2_himmel_pockets",
    },
    {
        "prompt": "1girl, ayanami rei, neon genesis evangelion, blue hair, short hair, red eyes, school uniform, arms behind back, looking at viewer, corridor, soft light, close-up",
        "alias": "v2_rei_behind",
    },
    {
        "prompt": "1girl, rem, re:zero, blue hair, short hair, blue eyes, white dress, hands clasped behind back, flower field, wind, hair blowing, gentle smile",
        "alias": "v2_rem_behind",
    },

    # === 손 가림 구도 (물건 뒤, 소매 숨기기) ===
    {
        "prompt": "1girl, senjougahara hitagi, bakemonogatari, purple hair, long hair, sharp eyes, school uniform, hugging book to chest, looking at viewer, head tilt, wind",
        "alias": "v2_hitagi_book",
    },
    {
        "prompt": "1girl, reze, chainsaw man, purple hair, short hair, red eyes, oversized sweater, long sleeves past wrists, hands hidden in sleeves, night, city lights, cute",
        "alias": "v2_reze_sleeves",
    },

    # === 손 고정 포즈 (양손 모으기, 기도) ===
    {
        "prompt": "1girl, frieren, sousou no frieren, white hair, long hair, elf ears, green eyes, mage robe, hands together, praying pose, magical light, starry sky, peaceful",
        "alias": "v2_frieren_pray",
    },

    # === 클로즈업 (손 프레임 밖) ===
    {
        "prompt": "1girl, rem, re:zero, blue hair, short hair, blue eyes, maid headdress, face close-up, soft smile, looking at viewer, blurry background, portrait",
        "alias": "v2_rem_closeup",
    },
    {
        "prompt": "1boy, himmel, sousou no frieren, blue hair, short hair, blue eyes, face close-up, gentle smile, handsome, looking at viewer, sunset light on face, portrait",
        "alias": "v2_himmel_closeup",
    },
    {
        "prompt": "1girl, frieren, sousou no frieren, white hair, long hair, elf ears, green eyes, face close-up, expressionless, looking at viewer, cherry blossoms, portrait",
        "alias": "v2_frieren_closeup",
    },
    {
        "prompt": "1girl, yamada ryo, bocchi the rock!, blue hair, long hair, blue eyes, face close-up, stoic expression, looking away, cool, portrait",
        "alias": "v2_ryo_closeup",
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
    print(f"pale_aqua 프리셋 테스트 {TOTAL}장")
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
