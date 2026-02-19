"""pale_aqua 스타일에 어울리는 캐릭터 5장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pale_aqua"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# pale_aqua: 연한 파스텔, 수채화, 청량하고 몽환적
JOBS = [
    # 프리렌 - 은발, 몽환적, 요정
    {
        "prompt": "1girl, frieren, sousou no frieren, white hair, long hair, elf ears, green eyes, staff, robe, peaceful, forest, sunlight, masterpiece",
        "alias": "frieren",
        "name": "프리렌",
    },
    # 렘 - 파란 머리, 청순, 메이드
    {
        "prompt": "1girl, rem, re:zero, blue hair, short hair, blue eyes, maid, gentle smile, flowers, soft lighting, masterpiece",
        "alias": "rem",
        "name": "렘",
    },
    # 비올렛 에버가든 - 금발, 우아함
    {
        "prompt": "1girl, violet evergarden, blonde hair, braided bun, blue eyes, white dress, brooch, elegant, letter, window light, masterpiece",
        "alias": "violet",
        "name": "비올렛",
    },
    # 치노 - 파란 머리, 작은 체구, 카페
    {
        "prompt": "1girl, kafuu chino, gochuumon wa usagi desu ka, blue hair, long hair, blue eyes, cafe uniform, rabbit, cute, indoor, masterpiece",
        "alias": "chino",
        "name": "치노",
    },
    # 코코아 - 연한 갈색, 밝은 분위기
    {
        "prompt": "1girl, hoto cocoa, gochuumon wa usagi desu ka, light brown hair, pink eyes, cafe uniform, cheerful, smile, warm lighting, masterpiece",
        "alias": "cocoa",
        "name": "코코아",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": "pale_aqua",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['name']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"pale_aqua 스타일 캐릭터 {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.5)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
