"""냥냥돌쇠 프리셋별 테스트"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_normal"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 냥냥돌쇠 D버전 (app/presets/characters.py에서 관리)
CHAR = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes, facial mole, multiple moles, mole under eye, mole on neck"
NEG = "moles on body, mole on forehead, mole on nose"

JOBS = [
    {
        "prompt": f"{CHAR}, smile, looking at viewer, upper body, masterpiece, best quality",
        "style": "pale_aqua",
        "alias": "dolsoe_pale_aqua",
    },
    {
        "prompt": f"{CHAR}, smirk, looking at viewer, upper body, masterpiece, best quality",
        "style": "mono_halftone",
        "alias": "dolsoe_mono_halftone",
    },
    {
        "prompt": f"{CHAR}, happy, looking at viewer, masterpiece, best quality",
        "style": "chibi_sketch",
        "alias": "dolsoe_chibi",
    },
    {
        "prompt": f"{CHAR}, gentle smile, looking at viewer, upper body, masterpiece, best quality",
        "style": "cozy_gouache",
        "alias": "dolsoe_gouache",
    },
    {
        "prompt": f"{CHAR}, peaceful, looking at viewer, upper body, masterpiece, best quality",
        "style": "waterful",
        "alias": "dolsoe_waterful",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "",
        "width": 832,
        "height": 1024,  # Normal Size (각 변 1024 이하)
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": job["style"],
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
    print(f"냥냥돌쇠 프리셋별 테스트 {TOTAL}장 (NAI V4.5 Full)")
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
