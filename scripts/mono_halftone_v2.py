"""mono_halftone 프리셋 추가 테스트 10장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_mono_halftone"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {
        "prompt": "1girl, long white hair, red eyes, vampire, fangs, licking lips, blood drop, close-up face, seductive",
        "alias": "v2_vampire_lick",
    },
    {
        "prompt": "1boy, messy black hair, detective coat, cigarette, rain, neon signs, looking back, noir atmosphere",
        "alias": "v2_noir_detective",
    },
    {
        "prompt": "1girl, short bob hair, cat ears, choker, crop top, arms crossed, annoyed expression, alley background",
        "alias": "v2_catgirl_alley",
    },
    {
        "prompt": "1girl, long silver hair, military uniform, epaulettes, sword at hip, standing tall, commanding presence, upper body",
        "alias": "v2_military_commander",
    },
    {
        "prompt": "1boy, slicked back hair, bartender vest, shaking cocktail, bar counter, dim lighting, charming smile",
        "alias": "v2_bartender",
    },
    {
        "prompt": "1girl, twin tails, idol costume, microphone, stage spotlight, winking, dynamic pose, energetic",
        "alias": "v2_idol_stage",
    },
    {
        "prompt": "1girl, ponytail, boxing gloves, sports bra, sweat, punching pose, intense eyes, gym background",
        "alias": "v2_boxer_girl",
    },
    {
        "prompt": "1boy, long white hair, eyepatch, black coat, katana drawn, wind blowing hair, rooftop, full moon",
        "alias": "v2_samurai_moon",
    },
    {
        "prompt": "1girl, short hair, nurse outfit, clipboard, glasses, pushing glasses up, serious expression, close-up",
        "alias": "v2_nurse_glasses",
    },
    {
        "prompt": "1girl, drill hair, elegant dress, wine glass, ballroom, smug expression, looking down at viewer, ojou-sama",
        "alias": "v2_ojousama_wine",
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
        "style": "mono_halftone",
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
    print(f"mono_halftone v2 테스트 {TOTAL}장")
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
