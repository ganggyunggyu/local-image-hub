"""밴드 애니 크로스오버 - 다른 세계관 그림체로"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_band_crossover"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STYLES = ["pale_aqua", "monogatari", "waterful"]

# 캐릭터 정의
KEION_CHARS = {
    "yui": "hirasawa yui, brown hair, short hair, hairclip, cheerful",
    "mio": "akiyama mio, black long hair, shy, elegant",
    "ritsu": "tainaka ritsu, light brown hair, headband, energetic",
    "mugi": "kotobuki tsumugi, blonde hair, blue eyes, thick eyebrows, gentle",
    "azusa": "nakano azusa, black hair, twintails, serious",
}

BOCCHI_CHARS = {
    "bocchi": "gotoh hitori, pink long hair, anxious, pink tracksuit",
    "nijika": "ijichi nijika, blonde ponytail, ahoge, cheerful",
    "ryo": "yamada ryo, blue short hair, expressionless, cool",
    "kita": "kita ikuyo, red hair, yellow eyes, energetic",
}

GBC_CHARS = {
    "nina": "iseri nina, purple short hair, twintails, blue eyes, passionate",
    "momoka": "kawaragi momoka, silver hair, tomboyish, cool",
    "subaru": "awa subaru, green hair, quiet",
    "tomo": "ebizuka tomo, ash brown hair, red eyes, small, intense",
}

JOBS = [
    # 케이온 캐릭터 → 봇치더락 세계관
    {
        "prompt": f"1girl, bocchi the rock! style, livehouse background, anxious expression, holding guitar nervously, {KEION_CHARS['yui']}, bocchi the rock! parody, masterpiece, best quality",
        "style": "waterful",
        "alias": "yui_in_bocchi",
        "name": "유이 in 봇치더락",
    },
    {
        "prompt": f"1girl, bocchi the rock! style, dark livehouse, spotlight, bass guitar, {KEION_CHARS['mio']}, bocchi the rock! parody, cool bassist, masterpiece, best quality",
        "style": "waterful",
        "alias": "mio_in_bocchi",
        "name": "미오 in 봇치더락",
    },
    # 봇치 캐릭터 → 케이온 세계관
    {
        "prompt": f"1girl, k-on! style, light music club room, tea time, relaxed, school uniform, {BOCCHI_CHARS['bocchi']}, k-on! parody, cozy atmosphere, masterpiece, best quality",
        "style": "pale_aqua",
        "alias": "bocchi_in_keion",
        "name": "봇치 in 케이온",
    },
    {
        "prompt": f"1girl, k-on! style, classroom, after school, warm lighting, {BOCCHI_CHARS['kita']}, k-on! parody, slice of life, masterpiece, best quality",
        "style": "pale_aqua",
        "alias": "kita_in_keion",
        "name": "키타 in 케이온",
    },
    # 걸밴크 캐릭터 → 봇치더락 세계관
    {
        "prompt": f"1girl, bocchi the rock! style, shimokitazawa, street, guitar case, {GBC_CHARS['nina']}, bocchi the rock! parody, urban, masterpiece, best quality",
        "style": "monogatari",
        "alias": "nina_in_bocchi",
        "name": "니나 in 봇치더락",
    },
    # 케이온 캐릭터 → 걸밴크 세계관
    {
        "prompt": f"1girl, girls band cry style, street performance, passionate, screaming, {KEION_CHARS['ritsu']}, girls band cry parody, intense emotion, masterpiece, best quality",
        "style": "monogatari",
        "alias": "ritsu_in_gbc",
        "name": "리츠 in 걸밴크",
    },
    # 봇치 캐릭터 → 걸밴크 세계관
    {
        "prompt": f"1girl, girls band cry style, urban night, neon lights, rebellious, {BOCCHI_CHARS['ryo']}, girls band cry parody, cool, masterpiece, best quality",
        "style": "waterful",
        "alias": "ryo_in_gbc",
        "name": "료 in 걸밴크",
    },
    # 걸밴크 캐릭터 → 케이온 세계관
    {
        "prompt": f"1girl, k-on! style, school rooftop, sunset, peaceful, wind, {GBC_CHARS['momoka']}, k-on! parody, soft lighting, masterpiece, best quality",
        "style": "pale_aqua",
        "alias": "momoka_in_keion",
        "name": "모모카 in 케이온",
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
            print(f"[{idx:02d}/{TOTAL}] OK {job['name']} - {job['style']}")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"밴드 애니 크로스오버 {TOTAL}장")
    print("다른 세계관 그림체로!")
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
