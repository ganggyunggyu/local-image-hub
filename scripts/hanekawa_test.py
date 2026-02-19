"""하네카와 츠바사 & 블랙 하네카와 다양한 구도"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_hanekawa"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 캐릭터 정의
CHARACTERS = {
    "black_hanekawa": {
        "tags": "black hanekawa, monogatari \\(series\\), nekomonogatari, white hair, long hair, cat ears, animal ears, yellow eyes, slit pupils, pale skin",
        "name": "블랙 하네카와",
    },
    "tsubasa": {
        "tags": "hanekawa tsubasa, monogatari \\(series\\), bakemonogatari, black hair, long hair, braids, twin braids, glasses, purple eyes",
        "name": "하네카와 츠바사",
    },
}

# 다양한 구도/상황
COMPOSITIONS = [
    ("smile, looking at viewer, upper body, school uniform", "교복"),
    ("from side, profile, moonlight, night sky, outdoor", "달빛"),
    ("sitting, window, curtains, indoor, peaceful", "창가"),
    ("lying down, bed, white sheets, relaxed", "침대"),
    ("from below, looking down at viewer, confident, smirk", "올려다보기"),
    ("walking, street, city lights, night, dynamic pose", "야경"),
    ("close up, face focus, detailed eyes, gentle expression", "클로즈업"),
    ("back view, looking back, wind, hair flowing", "뒤돌아보기"),
    ("standing, full body, casual clothes, hands in pockets", "전신"),
    ("reading book, library, bookshelf, focused", "독서"),
]

STYLES = ["pale_aqua", "monogatari", "waterful"]

# 블랙 하네카와 10장 + 하네카와 츠바사 10장 = 20장
JOBS = []

# 블랙 하네카와 - 10장
for i, (comp, comp_name) in enumerate(COMPOSITIONS):
    style = STYLES[i % len(STYLES)]
    char = CHARACTERS["black_hanekawa"]
    JOBS.append({
        "prompt": f"1girl, {char['tags']}, {comp}, masterpiece, best quality",
        "style": style,
        "alias": f"black_hanekawa_{i+1:02d}_{style}",
        "char_name": char['name'],
        "comp_name": comp_name,
    })

# 하네카와 츠바사 - 10장
for i, (comp, comp_name) in enumerate(COMPOSITIONS):
    style = STYLES[i % len(STYLES)]
    char = CHARACTERS["tsubasa"]
    JOBS.append({
        "prompt": f"1girl, {char['tags']}, {comp}, masterpiece, best quality",
        "style": style,
        "alias": f"tsubasa_{i+1:02d}_{style}",
        "char_name": char['name'],
        "comp_name": comp_name,
    })

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
            print(f"[{idx:02d}/{TOTAL}] OK {job['char_name']} - {job['style']} ({job['comp_name']})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"하네카와 테스트 {TOTAL}장 (블랙 하네카와 10장 + 츠바사 10장)")
    print(f"스타일: {', '.join(STYLES)}")
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
