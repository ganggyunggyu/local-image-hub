"""냥냥돌쇠 캐릭터 디자인 테스트 - 4가지 컨셉 x 2~3장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_nyang_dolsoe_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 캐릭터 코어 태그 (버전별 고정)
CHAR = {
    "A": "1girl, cat ears, cat tail, silver hair, short messy hair, ahoge, golden eyes, fang, small build, white ribbon choker",
    "B": "1girl, cat ears, cat tail, black hair, long hair, hime cut, blue eyes, pale skin, red hair ribbon, petite",
    "C": "1girl, cat ears, cat tail, pink hair, medium hair, side braid, green eyes, freckles, bandaid on cheek, energetic",
    "D": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, mole under left eye, sharp eyes, cool beauty",
}

JOBS = [
    # === 버전 A: 은발 숏컷 아호게 금안 ===
    {
        "prompt": f"{CHAR['A']}, maid outfit, white apron, holding tray, indoor, smile, looking at viewer, upper body",
        "alias": "A4_maid",
    },
    {
        "prompt": f"{CHAR['A']}, winter coat, scarf, snow falling, night, street lamp, breath visible, face close-up",
        "alias": "A5_snow",
    },
    {
        "prompt": f"{CHAR['A']}, swimsuit, beach, ocean, summer, holding straw hat, cheerful, sunny",
        "alias": "A6_beach",
    },
    {
        "prompt": f"{CHAR['A']}, witch hat, black cloak, holding magic wand, halloween, pumpkins, night, playful",
        "alias": "A7_witch",
    },

    # === 버전 B: 흑발 히메컷 청안 ===
    {
        "prompt": f"{CHAR['B']}, miko outfit, shrine maiden, shrine, torii gate, autumn leaves, praying, serene",
        "alias": "B4_miko",
    },
    {
        "prompt": f"{CHAR['B']}, gothic lolita, black dress, parasol, rose garden, elegant, looking at viewer, upper body",
        "alias": "B5_gothic",
    },
    {
        "prompt": f"{CHAR['B']}, yukata, summer festival, holding fan, lanterns, evening, gentle smile, face close-up",
        "alias": "B6_yukata",
    },
    {
        "prompt": f"{CHAR['B']}, school uniform, library, sitting, hugging book to chest, looking away, shy, soft light",
        "alias": "B7_library",
    },

    # === 버전 C: 핑크발 사이드브레이드 녹안 주근깨 ===
    {
        "prompt": f"{CHAR['C']}, gym clothes, running, track field, determined expression, ponytail, daytime, dynamic",
        "alias": "C3_running",
    },
    {
        "prompt": f"{CHAR['C']}, pajamas, messy hair, yawning, morning, bedroom, sunlight through curtain, sleepy",
        "alias": "C4_morning",
    },
    {
        "prompt": f"{CHAR['C']}, artist smock, holding paintbrush, paint on face, art studio, colorful, happy",
        "alias": "C5_artist",
    },
    {
        "prompt": f"{CHAR['C']}, raincoat, yellow, puddle jumping, rain, umbrella, laughing, full body",
        "alias": "C6_rain",
    },

    # === 버전 D: 남색 보브컷 호박안 점 ===
    {
        "prompt": f"{CHAR['D']}, suit, necktie, office, sitting at desk, legs crossed, confident, looking at viewer, upper body",
        "alias": "D3_office",
    },
    {
        "prompt": f"{CHAR['D']}, leather jacket, motorcycle, night city, wind, hair blowing, cool, side profile",
        "alias": "D4_bike",
    },
    {
        "prompt": f"{CHAR['D']}, kimono, black and gold, fan, new year, shrine, elegant, face close-up",
        "alias": "D5_kimono",
    },
    {
        "prompt": f"{CHAR['D']}, lab coat, glasses, holding clipboard, laboratory, serious expression, intellectual, upper body",
        "alias": "D6_scientist",
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
    print(f"냥냥돌쇠 캐릭터 디자인 테스트 {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)
    print("A: 은발 숏컷 아호게 금안 송곳니")
    print("B: 흑발 히메컷 청안 레드리본")
    print("C: 핑크발 사이드브레이드 녹안 주근깨")
    print("D: 남색 보브컷 호박안 점")
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
