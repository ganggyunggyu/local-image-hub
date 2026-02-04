"""
Watercolor Sketch 스타일 전용 배치 생성 스크립트
프롬프트 77토큰 제한 대응 버전
"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
PRESET_NAME = "watercolor_sketch"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_{PRESET_NAME}"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# Watercolor Sketch 스타일 (간결화)
# ============================================

STYLE = {
    "prompt_suffix": "fine lines, pale watercolor, desaturated, paper texture, soft light, ethereal",
    "negative_suffix": "thick lines, vibrant, saturated, sharp, 3d, digital, text, signature",
    "steps": 35,
    "guidance": 4.0,
}

# ============================================
# 캐릭터 (태그 간결화)
# ============================================

CHARACTERS = {
    # 체인소맨
    "reze": {"tags": "1girl, reze, chainsaw man, purple hair, short hair, red eyes", "alias": "reze"},
    "makima": {"tags": "1girl, makima, chainsaw man, orange hair, braided ponytail, yellow eyes", "alias": "makima"},
    "power": {"tags": "1girl, power, chainsaw man, blonde hair, red horns, red eyes", "alias": "power"},

    # 케이온
    "yui": {"tags": "1girl, hirasawa yui, k-on!, brown hair, short hair, hairpin", "alias": "yui"},
    "mio": {"tags": "1girl, akiyama mio, k-on!, black hair, long hair, grey eyes", "alias": "mio"},
    "ritsu": {"tags": "1girl, tainaka ritsu, k-on!, brown hair, hairband", "alias": "ritsu"},
    "mugi": {"tags": "1girl, kotobuki tsumugi, k-on!, blonde hair, blue eyes", "alias": "mugi"},
    "azusa": {"tags": "1girl, nakano azusa, k-on!, black hair, twintails", "alias": "azusa"},

    # 봇치더록
    "kikuri": {"tags": "1girl, hiroi kikuri, bocchi the rock!, purple hair, long hair, red eyes, mature", "alias": "kikuri"},
    "kikuri_bass": {"tags": "1girl, hiroi kikuri, bocchi the rock!, purple hair, red eyes, playing bass", "alias": "kikuri_bass"},
    "bocchi": {"tags": "1girl, gotoh hitori, bocchi the rock!, pink hair, blue eyes, shy", "alias": "bocchi"},
    "nijika": {"tags": "1girl, ijichi nijika, bocchi the rock!, blonde hair, star hair ornament", "alias": "nijika"},
    "ryo": {"tags": "1girl, yamada ryo, bocchi the rock!, blue hair, stoic", "alias": "ryo"},
    "kita": {"tags": "1girl, kita ikuyo, bocchi the rock!, red hair, green eyes", "alias": "kita"},

    # 바케모노가타리
    "hitagi": {"tags": "1girl, senjougahara hitagi, bakemonogatari, purple hair, sharp eyes", "alias": "hitagi"},
    "hanekawa": {"tags": "1girl, hanekawa tsubasa, bakemonogatari, black hair, glasses, braids", "alias": "hanekawa"},
    "nadeko": {"tags": "1girl, sengoku nadeko, bakemonogatari, orange hair, bangs covering eyes", "alias": "nadeko"},
    "shinobu": {"tags": "1girl, oshino shinobu, bakemonogatari, blonde hair, yellow eyes, vampire", "alias": "shinobu"},

    # NANA
    "nana_o": {"tags": "1girl, osaki nana, nana, black hair, short hair, punk, vocalist", "alias": "nana_o"},
    "hachi": {"tags": "1girl, komatsu nana, nana, brown hair, cute, girly", "alias": "hachi"},

    # 프리렌
    "frieren": {"tags": "1girl, frieren, sousou no frieren, white hair, elf ears, mage", "alias": "frieren"},
    "fern": {"tags": "1girl, fern, sousou no frieren, purple hair, mage", "alias": "fern"},

    # 로젠메이든
    "shinku": {"tags": "1girl, shinku, rozen maiden, blonde hair, twintails, red eyes, gothic lolita", "alias": "shinku"},
    "suiseiseki": {"tags": "1girl, suiseiseki, rozen maiden, green hair, twin drills, heterochromia", "alias": "suiseiseki"},
}

# ============================================
# 장면 (간결화)
# ============================================

SCENES = {
    "window": {"tags": "looking out window, soft light", "filename": "window"},
    "rain": {"tags": "rain, umbrella, melancholic", "filename": "rain"},
    "cafe": {"tags": "cafe, coffee cup, sitting", "filename": "cafe"},
    "sunset": {"tags": "sunset, golden hour, rooftop", "filename": "sunset"},
    "sakura": {"tags": "cherry blossoms, petals, spring", "filename": "sakura"},
    "library": {"tags": "library, reading book", "filename": "library"},
    "night": {"tags": "night, stars, moon", "filename": "night"},
    "morning": {"tags": "morning, sunlight, bedroom", "filename": "morning"},
    "snow": {"tags": "snow, winter, scarf", "filename": "snow"},
    "portrait": {"tags": "portrait, upper body, simple background", "filename": "portrait"},
}

# ============================================
# 표정 (간결화)
# ============================================

EXPRESSIONS = {
    "gentle": {"tags": "gentle smile, soft expression", "filename": "gentle"},
    "melancholy": {"tags": "melancholic, wistful", "filename": "sad"},
    "peaceful": {"tags": "peaceful, serene", "filename": "peaceful"},
    "contemplative": {"tags": "contemplative, thoughtful", "filename": "think"},
    "nostalgic": {"tags": "nostalgic, bittersweet", "filename": "nostalgic"},
}


def build_prompt(character: dict, scene: dict, expression: dict) -> tuple[str, str]:
    """프롬프트 조합 (77토큰 이하로 유지)"""
    positive = f"{character['tags']}, {expression['tags']}, {scene['tags']}, {STYLE['prompt_suffix']}"
    negative = f"lowres, bad anatomy, bad hands, error, {STYLE['negative_suffix']}"
    return positive, negative


def generate_filename(character: dict, scene: dict, expression: dict) -> str:
    return f"{character['alias']}_{scene['filename']}_{expression['filename']}"


async def generate_and_save(client: httpx.AsyncClient, prompt: str, negative: str, filename: str) -> dict:
    payload = {
        "prompt": prompt,
        "negative_prompt": negative,
        "width": 832,
        "height": 1216,
        "steps": STYLE["steps"],
        "guidance_scale": STYLE["guidance"],
        "save_to_disk": False,
    }

    try:
        response = await client.post(API_URL, json=payload, timeout=300.0)
        result = response.json()

        if result.get("success") and result.get("image_base64"):
            seed = result.get("seed", 0)
            filepath = OUTPUT_DIR / f"{filename}_{seed}.webp"
            img_data = b64decode(result["image_base64"])
            filepath.write_bytes(img_data)
            return {"success": True, "filename": filepath.name, "seed": seed}
        else:
            return {"success": False, "error": result.get("error", "No image returned")}

    except Exception as e:
        return {"success": False, "error": str(e)}


async def main():
    characters = list(CHARACTERS.values())
    scenes = list(SCENES.values())
    expressions = list(EXPRESSIONS.values())

    all_combinations = []
    for char in characters:
        for scene in scenes:
            for expr in expressions:
                all_combinations.append((char, scene, expr))

    random.shuffle(all_combinations)

    total = len(all_combinations)
    success_count = 0
    fail_count = 0

    print(f"Watercolor Sketch 배치 생성")
    print(f"저장 폴더: {OUTPUT_DIR}")
    print(f"총 {total}장 생성 예정")
    print("=" * 50)

    async with httpx.AsyncClient() as client:
        for i, (char, scene, expr) in enumerate(all_combinations, 1):
            prompt, negative = build_prompt(char, scene, expr)
            filename = generate_filename(char, scene, expr)

            print(f"[{i:04d}/{total}] {filename}", end=" ")

            result = await generate_and_save(client, prompt, negative, filename)

            if result["success"]:
                success_count += 1
                print(f"OK (seed: {result['seed']})")
            else:
                fail_count += 1
                print(f"FAIL: {result.get('error', '?')}")

            await asyncio.sleep(0.3)

    print("=" * 50)
    print(f"완료! 성공: {success_count}, 실패: {fail_count}")
    print(f"저장 위치: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
