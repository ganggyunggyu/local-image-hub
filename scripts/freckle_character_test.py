"""주근깨 캐릭터 3타입 테스트 (15장)"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_freckle_test"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Type A: 오렌지 웨이브 + 녹안 + 코&볼 주근깨 + 밝은 피부 + 활발
CHAR_A = "1girl, orange hair, wavy hair, long hair, green eyes, bright eyes, freckles, nose freckles, cheek freckles, light skin, smile"
NEG_A = "dark skin, moles, facial mole"

# Type B: 브라운 숏컷 + 갈색눈 + 코 주근깨 + 탄 피부 + 보이시
CHAR_B = "1girl, brown hair, short hair, messy hair, brown eyes, freckles, nose freckles, tan skin, tomboy, confident"
NEG_B = "long hair, feminine dress, moles, facial mole"

# Type C: 적갈색 롱헤어 + 청안 + 전면 주근깨 + 창백 + 차분
CHAR_C = "1girl, auburn hair, long hair, straight hair, blue eyes, freckles, heavy freckles, light freckles on face, pale skin, calm, serene"
NEG_C = "tan skin, moles, facial mole, smile"

JOBS = [
    # Type A - 오렌지 웨이브 (5장)
    {"char": CHAR_A, "neg": NEG_A, "prompt_extra": "school uniform, classroom, morning light", "alias": "A01_school", "style": "pale_aqua"},
    {"char": CHAR_A, "neg": NEG_A, "prompt_extra": "sundress, flower field, summer, wind", "alias": "A02_flower", "style": "watercolor_sketch"},
    {"char": CHAR_A, "neg": NEG_A, "prompt_extra": "gym clothes, basketball, sweat, energetic", "alias": "A03_gym", "style": "pop_fanart"},
    {"char": CHAR_A, "neg": NEG_A, "prompt_extra": "hoodie, headphones, rooftop, sunset", "alias": "A04_rooftop", "style": "shinkai"},
    {"char": CHAR_A, "neg": NEG_A, "prompt_extra": "pajamas, stretching, bedroom, morning", "alias": "A05_morning", "style": "cozy_gouache"},

    # Type B - 브라운 숏컷 (5장)
    {"char": CHAR_B, "neg": NEG_B, "prompt_extra": "leather jacket, motorcycle, cool, city night", "alias": "B01_biker", "style": "mono_halftone"},
    {"char": CHAR_B, "neg": NEG_B, "prompt_extra": "baseball cap, jersey, bat, stadium", "alias": "B02_baseball", "style": "pop_fanart"},
    {"char": CHAR_B, "neg": NEG_B, "prompt_extra": "oversized shirt, shorts, convenience store, night", "alias": "B03_konbini", "style": "pale_aqua"},
    {"char": CHAR_B, "neg": NEG_B, "prompt_extra": "rain, umbrella, wet streets, reflections", "alias": "B04_rain", "style": "watercolor_sketch"},
    {"char": CHAR_B, "neg": NEG_B, "prompt_extra": "workshop, goggles, tools, tinkering", "alias": "B05_workshop", "style": "cozy_gouache"},

    # Type C - 적갈색 롱헤어 (5장)
    {"char": CHAR_C, "neg": NEG_C, "prompt_extra": "white dress, library, reading, dim light", "alias": "C01_library", "style": "monogatari"},
    {"char": CHAR_C, "neg": NEG_C, "prompt_extra": "winter coat, snow, breath mist, cold", "alias": "C02_snow", "style": "pale_aqua"},
    {"char": CHAR_C, "neg": NEG_C, "prompt_extra": "kimono, shrine, autumn leaves, wind", "alias": "C03_shrine", "style": "kyoto_animation"},
    {"char": CHAR_C, "neg": NEG_C, "prompt_extra": "nightgown, window, moonlight, contemplative", "alias": "C04_moon", "style": "watercolor_sketch"},
    {"char": CHAR_C, "neg": NEG_C, "prompt_extra": "black turtleneck, cafe, coffee, quiet", "alias": "C05_cafe", "style": "mono_halftone"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    prompt = f"{job['char']}, {job['prompt_extra']}"
    payload = {
        "prompt": prompt,
        "negative_prompt": job["neg"],
        "width": 832,
        "height": 1216,
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
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} [{job['style']}] (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print(f"주근깨 캐릭터 테스트 {TOTAL}장", flush=True)
    print(f"Type A: 오렌지 웨이브 + 녹안 + 활발", flush=True)
    print(f"Type B: 브라운 숏컷 + 갈색눈 + 보이시", flush=True)
    print(f"Type C: 적갈색 롱헤어 + 청안 + 차분", flush=True)
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
