"""프리셋 쇼케이스 - 냥냥돌쇠로 전 프리셋 테스트 (26장)"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_preset_showcase"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 냥냥돌쇠 캐릭터
CHAR = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes, mole under eye"
SCENE = "upper body, looking at viewer, portrait"
NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

# 테스트할 프리셋 (포즈 특화 제외)
PRESETS = [
    # 일러스트 스타일
    "pale_aqua",
    "mono_halftone",
    "chibi_sketch",
    "cozy_gouache",
    "watercolor_sketch",
    "sepia_backlit",
    "mono_accent",
    "sketch_colorpop",
    "pop_fanart",
    "pastel_soft",
    "split_sketch",
    "waterful",
    # 스튜디오 스타일
    "kyoto_animation",
    "ufotable",
    "shinkai",
    "ghibli",
    "trigger",
    "mappa",
    "shaft",
    "monogatari",
    "inuyasha",
    # 게임 스타일
    "genshin",
    "blue_archive",
    "arknights",
    "fate",
    "cyberpunk",
]

JOBS = [{"prompt": f"{CHAR}, {SCENE}", "alias": preset, "style": preset} for preset in PRESETS]
TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 1024,
        "height": 1024,
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
    print("프리셋 쇼케이스 - 냥냥돌쇠 26장", flush=True)
    print("일러스트 12 + 스튜디오 9 + 게임 5", flush=True)
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
