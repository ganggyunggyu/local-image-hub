"""걸밴크라이 새끼손가락 포즈 + NANA 레이라"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_gbc_pinky_layla"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    # 걸밴크라이 새끼손가락 포즈 (시그니처 포즈)
    {"prompt": "1girl, nina, girls band cry, short blonde hair, red eyes, pinky finger up, pinky gesture, confident, upper body, looking at viewer", "name": "nina_pinky1"},
    {"prompt": "1girl, nina, girls band cry, short blonde hair, pinky up, rock gesture, energetic, smile, upper body", "name": "nina_pinky2"},
    {"prompt": "1girl, nina, girls band cry, guitar, pinky finger raised, cool, stage, performing", "name": "nina_pinky_stage"},

    {"prompt": "1girl, momoka, girls band cry, pink hair, twintails, pinky finger up, cute, cheerful, upper body", "name": "momoka_pinky1"},
    {"prompt": "1girl, momoka, girls band cry, pink hair, pinky gesture, guitar, energetic, smile", "name": "momoka_pinky2"},

    {"prompt": "1girl, subaru, girls band cry, green hair, pinky finger up, calm, cool, drums, upper body", "name": "subaru_pinky"},

    {"prompt": "1girl, rupa, girls band cry, dark skin, white hair, pinky finger raised, bass guitar, cool, upper body", "name": "rupa_pinky"},

    {"prompt": "1girl, tomo, girls band cry, brown hair, small, pinky up, keyboard, determined, upper body", "name": "tomo_pinky"},

    # 단체 새끼손가락
    {"prompt": "5girls, girls band cry, band members, all raising pinky finger, group pose, energetic, unity, together", "name": "gbc_pinky_group1"},
    {"prompt": "5girls, girls band cry, togenashi togeari, pinky gesture together, stage, concert, dramatic", "name": "gbc_pinky_group2"},

    # NANA 레이라 (TRAPNEST 보컬)
    {"prompt": "1girl, serizawa reira, layla, nana (anime), long blonde hair, elegant, singing, microphone, beautiful, upper body", "name": "layla_sing"},
    {"prompt": "1girl, serizawa reira, layla, nana (anime), blonde hair, cigarette, melancholic, lonely, window, night", "name": "layla_smoke"},
    {"prompt": "1girl, serizawa reira, layla, nana (anime), blonde hair, glamorous dress, stage, spotlight, dramatic", "name": "layla_stage"},
    {"prompt": "1girl, serizawa reira, layla, nana (anime), blonde hair, vulnerable, crying, emotional, close up", "name": "layla_cry"},
    {"prompt": "1girl, serizawa reira, layla, nana (anime), blonde hair, gentle smile, soft lighting, beautiful, portrait", "name": "layla_gentle"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{job['prompt']}, masterpiece",
        "negative_prompt": "low quality, worst quality, bad hands, extra fingers, missing fingers",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{idx:02d}_{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"걸밴크라이 새끼손가락 + NANA 레이라 {TOTAL}장")
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


if __name__ == "__main__":
    asyncio.run(main())
