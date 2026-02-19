"""전체 프리셋 테스트 - 무리무리 캐릭터"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_renako_presets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 와타나레 - 아마오리 레나코 (Amaori Renako)
CHAR = "1girl, amaori renako, watanare, pink hair, short hair, bob cut, black hairpin, purple eyes, school uniform, blazer, smile, looking at viewer, upper body"

# 모든 스타일 프리셋 (포즈 프리셋 제외)
STYLES = [
    "pale_aqua",
    "mono_halftone",
    "chibi_sketch",
    "cozy_gouache",
    "watercolor_sketch",
    "kyoto_animation",
    "ufotable",
    "shinkai",
    "ghibli",
    "trigger",
    "mappa",
    "shaft",
    "monogatari",
    "genshin",
    "blue_archive",
    "arknights",
    "fate",
    "cyberpunk",
    "pastel_soft",
    "inuyasha",
    "sepia_backlit",
    "mono_accent",
    "sketch_colorpop",
    "pop_fanart",
    "split_sketch",
    "waterful",
]

TOTAL = len(STYLES)


async def generate(client, idx, style):
    payload = {
        "prompt": f"{CHAR}, masterpiece, best quality",
        "negative_prompt": "",
        "width": 832,
        "height": 1024,  # Normal Size (무료 생성)
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": style,
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{style}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {style} (seed: {seed})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {style}: {data.get('error', '?')[:60]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {style}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"무리무리 전체 프리셋 테스트 {TOTAL}장 (NAI V4.5 Full, 832x1024)")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, style in enumerate(STYLES, 1):
            if await generate(client, i, style):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.5)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
