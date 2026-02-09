"""냥냥돌쇠 첫 게시글 인사짤 (5장)"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_greeting"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 냥냥돌쇠 D버전 캐릭터
CHAR = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes, facial mole, multiple moles, mole under eye, mole on neck"
NEG = "moles on body, mole on forehead, mole on nose, extra fingers, fused fingers, deformed hands, bad hands, poorly drawn hands"

JOBS = [
    {"prompt": f"{CHAR}, waving hand, smile, greeting, hello, upper body, looking at viewer, cheerful, white background", "alias": "greet_01_wave", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, peace sign, happy, energetic, upper body, looking at viewer, bright, white background", "alias": "greet_02_peace", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, both hands waving, excited, welcoming, upper body, looking at viewer, cute, white background", "alias": "greet_03_welcome", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, hand on chest, bow, polite greeting, upper body, gentle smile, formal, white background", "alias": "greet_04_bow", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, cat pose, paw gesture, playful, nya, upper body, looking at viewer, cute, white background", "alias": "greet_05_nya", "style": "pale_aqua"},
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
    print("냥냥돌쇠 첫 게시글 인사짤 5장", flush=True)
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
