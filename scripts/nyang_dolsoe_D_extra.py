"""냥냥돌쇠 D버전 점 일관성 테스트 10장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_nyang_dolsoe_D_mole"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 점 배치: 오른쪽 눈밑 2개, 왼쪽 눈밑 1개, 목 왼쪽 하단 1개
CHAR_D = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes, cool beauty, facial mole, multiple moles, two moles under right eye, mole under left eye, neck mole on left side"
NEG_MOLE = "moles on body, mole on forehead, mole on nose, mole on cheek"

JOBS = [
    {
        "prompt": f"{CHAR_D}, white blouse, face close-up, looking at viewer, soft light, simple white background, portrait, detailed face",
        "alias": "D_mole01_front",
    },
    {
        "prompt": f"{CHAR_D}, turtleneck sweater, face close-up, three quarter view, looking at viewer, warm light, blurry background, portrait",
        "alias": "D_mole02_3quarter",
    },
    {
        "prompt": f"{CHAR_D}, school uniform, face close-up, slight smile, looking at viewer, classroom, afternoon light, portrait",
        "alias": "D_mole03_school",
    },
    {
        "prompt": f"{CHAR_D}, black dress, face close-up, cool expression, looking at viewer, dark background, dramatic lighting, portrait",
        "alias": "D_mole04_dark",
    },
    {
        "prompt": f"{CHAR_D}, casual clothes, head tilt, face close-up, looking at viewer, outdoor, golden hour, wind, portrait",
        "alias": "D_mole05_golden",
    },
    {
        "prompt": f"{CHAR_D}, kimono, face and neck close-up, looking at viewer, cherry blossoms, spring, elegant, portrait",
        "alias": "D_mole06_kimono",
    },
    {
        "prompt": f"{CHAR_D}, off shoulder sweater, face and neck visible, looking away, window light, melancholic, portrait, upper body",
        "alias": "D_mole07_neck",
    },
    {
        "prompt": f"{CHAR_D}, maid headdress, face close-up, slight blush, looking at viewer, soft light, simple background, portrait",
        "alias": "D_mole08_maid",
    },
    {
        "prompt": f"{CHAR_D}, hoodie, face close-up, sleepy expression, morning light, bed, messy hair, portrait",
        "alias": "D_mole09_morning",
    },
    {
        "prompt": f"{CHAR_D}, suit, necktie, face and neck close-up, confident expression, looking at viewer, office, sharp lighting, portrait",
        "alias": "D_mole10_suit",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG_MOLE,
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
    print(f"냥냥돌쇠 D버전 추가 {TOTAL}장", flush=True)
    print(f"D: 남색 보브컷 호박안 쿨뷰티", flush=True)
    print(f"점: 오른눈밑2 + 왼눈밑1 + 목좌하1", flush=True)
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
