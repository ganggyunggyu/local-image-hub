"""와타나레 전 캐릭터 테스트 - 다양한 구도"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_watanare_chars"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 와타나레 캐릭터들
CHARACTERS = {
    "renako": {
        "tags": "amaori renako, watanare, pink hair, short hair, bob cut, black hairpin, purple eyes",
        "name": "레나코",
    },
    "mai": {
        "tags": "oozuka mai, watanare, blonde hair, long hair, blue eyes, model",
        "name": "마이",
    },
    "satsuki": {
        "tags": "koto satsuki, watanare, black hair, long hair, red eyes, elegant",
        "name": "사츠키",
    },
    "ajisai": {
        "tags": "sena ajisai, watanare, light purple hair, wavy hair, gentle, angel",
        "name": "아지사이",
    },
    "kaho": {
        "tags": "koyanagi kaho, watanare, light blue hair, twintails, yellow eyes, energetic",
        "name": "카호",
    },
}

# 다양한 구도/포즈
COMPOSITIONS = [
    ("smile, looking at viewer, upper body, school uniform", "기본"),
    ("from side, profile, wind, hair flowing, outdoor", "옆모습"),
    ("from below, looking down at viewer, confident", "올려다보기"),
    ("sitting, window, sunlight, peaceful, indoor", "창가"),
    ("walking, dynamic pose, street, city background", "거리"),
]

# 3가지 스타일만
STYLES = ["pale_aqua", "monogatari", "waterful"]

# 캐릭터 x 구도 x 스타일 조합 (5 x 5 x 3 = 75장은 너무 많음)
# 캐릭터별로 다른 구도 1개씩 + 스타일 3개 = 5 x 3 = 15장
JOBS = []
for i, (char_key, char_data) in enumerate(CHARACTERS.items()):
    comp, comp_name = COMPOSITIONS[i % len(COMPOSITIONS)]  # 캐릭터마다 다른 구도
    for style in STYLES:
        JOBS.append({
            "prompt": f"1girl, {char_data['tags']}, {comp}, masterpiece, best quality",
            "style": style,
            "alias": f"{char_key}_{style}",
            "char_name": char_data['name'],
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
    print(f"와타나레 전 캐릭터 테스트 {TOTAL}장")
    print(f"캐릭터: {', '.join([c['name'] for c in CHARACTERS.values()])}")
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
