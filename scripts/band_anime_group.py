"""밴드 애니 단체샷 - 케이온 / 봇치더락 / 걸즈밴드크라이"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_band_anime"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 케이온 - 방과후 티타임 (5명)
KEION = {
    "name": "케이온",
    "series": "k-on!",
    "members": [
        "hirasawa yui \\(brown hair, short hair, hairclip, guitar\\)",
        "akiyama mio \\(black hair, long hair, bass\\)",
        "tainaka ritsu \\(light brown hair, headband, drums\\)",
        "kotobuki tsumugi \\(blonde hair, blue eyes, thick eyebrows, keyboard\\)",
        "nakano azusa \\(black hair, twintails, guitar\\)",
    ],
}

# 봇치 더 락 - 결속밴드 (4명)
BOCCHI = {
    "name": "봇치더락",
    "series": "bocchi the rock!",
    "members": [
        "gotoh hitori \\(pink hair, long hair, pink tracksuit, guitar\\)",
        "ijichi nijika \\(blonde hair, ponytail, ahoge, drums\\)",
        "yamada ryo \\(blue hair, short hair, expressionless, bass\\)",
        "kita ikuyo \\(red hair, yellow eyes, guitar\\)",
    ],
}

# 걸즈 밴드 크라이 - 토게나시 토게아리 (5명)
GBC = {
    "name": "걸즈밴드크라이",
    "series": "girls band cry",
    "members": [
        "iseri nina \\(purple hair, short hair, twintails, blue eyes\\)",
        "kawaragi momoka \\(silver hair, medium hair, tomboyish\\)",
        "awa subaru \\(green hair, school uniform\\)",
        "rupa \\(dark skin, bassist\\)",
        "ebizuka tomo \\(ash brown hair, red eyes, headband, drums\\)",
    ],
}

# 다양한 단체샷 구도
COMPOSITIONS = [
    ("group shot, standing together, looking at viewer, casual clothes, city background", "도시 캐주얼"),
    ("band performance, stage, concert, instruments, dynamic, spotlight", "라이브 공연"),
    ("group photo, school uniform, classroom, smile, peace sign", "교실"),
    ("walking together, street, sunset, from behind, looking back", "거리 산책"),
    ("sitting together, cafe, window light, relaxed, talking", "카페"),
    ("practice room, instruments, focused, playing music", "연습실"),
]

STYLES = ["pale_aqua", "monogatari", "waterful"]

JOBS = []

# 각 밴드별 2장씩 (다른 구도)
for band_idx, band in enumerate([KEION, BOCCHI, GBC]):
    members_str = ", ".join(band["members"])
    count = len(band["members"])

    # 각 밴드당 2개 구도
    for comp_idx in range(2):
        comp, comp_name = COMPOSITIONS[(band_idx * 2 + comp_idx) % len(COMPOSITIONS)]
        style = STYLES[(band_idx + comp_idx) % len(STYLES)]

        JOBS.append({
            "prompt": f"{count}girls, {band['series']}, {members_str}, {comp}, masterpiece, best quality",
            "style": style,
            "alias": f"{band['name']}_{comp_idx+1:02d}_{style}",
            "band_name": band['name'],
            "comp_name": comp_name,
        })

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "",
        "width": 1024,  # 단체샷은 가로로
        "height": 832,
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
            print(f"[{idx:02d}/{TOTAL}] OK {job['band_name']} - {job['style']} ({job['comp_name']})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"밴드 애니 단체샷 {TOTAL}장")
    print("케이온 2장 / 봇치더락 2장 / 걸즈밴드크라이 2장")
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
