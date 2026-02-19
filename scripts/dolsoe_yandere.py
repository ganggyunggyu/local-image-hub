"""냥냥돌쇠 얀데레 짤"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_yandere"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 냥냥돌쇠 D버전
CHAR = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes, facial mole, multiple moles, mole under eye, mole on neck"
NEG = "moles on body, mole on forehead, mole on nose"

JOBS = [
    {
        "prompt": f"{CHAR}, yandere, crazy smile, wide eyes, looking at viewer, holding knife, dark aura, upper body, masterpiece, best quality",
        "alias": "yandere_knife",
    },
    {
        "prompt": f"{CHAR}, yandere, tilted head, empty eyes, creepy smile, shadow over eyes, upper body, looking at viewer, masterpiece, best quality",
        "alias": "yandere_creepy",
    },
    {
        "prompt": f"{CHAR}, yandere, obsessive, heart pupils, blushing, possessive, grabbing viewer, close up face, masterpiece, best quality",
        "alias": "yandere_obsess",
    },
    {
        "prompt": f"{CHAR}, yandere, tears, crying, smiling, broken heart, emotional, upper body, looking at viewer, masterpiece, best quality",
        "alias": "yandere_tears",
    },
    {
        "prompt": f"{CHAR}, yandere, angry, glaring, jealous, clenched fist, dark background, upper body, looking at viewer, masterpiece, best quality",
        "alias": "yandere_angry",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 832,
        "height": 1216,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')[:80]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"냥냥돌쇠 얀데레 짤 {TOTAL}장 (NAI V4.5 Full)")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(1.0)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
