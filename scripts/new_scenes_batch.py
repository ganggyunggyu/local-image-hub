"""
새 장면 + 새 캐릭터 위주 200장 배치
- 감성 장면 / 일본 지역 / 클래식~최신 캐릭터
"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_new_scenes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PRESETS = [
    "cozy_gouache", "watercolor_sketch", "kyoto_animation",
    "shinkai", "ghibli", "monogatari",
    "pastel_soft", "inuyasha", "sepia_backlit",
    "mono_accent", "sketch_colorpop",
]

CHARACTERS = [
    # 기존 인기
    {"tags": "1girl, reze, chainsaw man, purple hair, short hair, red eyes", "alias": "reze"},
    {"tags": "1girl, hiroi kikuri, bocchi the rock!, purple hair, long hair, red eyes, mature", "alias": "kikuri"},
    {"tags": "1girl, senjougahara hitagi, bakemonogatari, purple hair, sharp eyes", "alias": "hitagi"},
    {"tags": "1girl, osaki nana, nana, black hair, short hair, punk", "alias": "nana_o"},
    {"tags": "1girl, akiyama mio, k-on!, black hair, long hair, grey eyes", "alias": "mio"},
    {"tags": "1girl, shinku, rozen maiden, blonde hair, twintails, red eyes, gothic lolita", "alias": "shinku"},
    {"tags": "1girl, frieren, sousou no frieren, white hair, elf ears, mage", "alias": "frieren"},

    # 클래식
    {"tags": "1girl, tsukino usagi, sailor moon, blonde hair, twintails, blue eyes, tiara", "alias": "usagi"},
    {"tags": "1girl, ayanami rei, neon genesis evangelion, blue hair, short hair, red eyes", "alias": "rei"},
    {"tags": "1girl, souryuu asuka langley, neon genesis evangelion, red hair, blue eyes", "alias": "asuka"},
    {"tags": "1girl, kinomoto sakura, cardcaptor sakura, brown hair, green eyes, magical girl", "alias": "sakura_ccs"},
    {"tags": "1girl, kusanagi motoko, ghost in the shell, purple hair, red eyes, bodysuit", "alias": "motoko"},
    {"tags": "1girl, kikyo, inuyasha, black hair, long hair, miko, priestess", "alias": "kikyo"},

    # 2000s
    {"tags": "1girl, tohsaka rin, fate stay night, black hair, twintails, aqua eyes", "alias": "rin"},
    {"tags": "1girl, suzumiya haruhi, suzumiya haruhi no yuuutsu, brown hair, hair ribbon", "alias": "haruhi"},
    {"tags": "1girl, shana, shakugan no shana, red hair, long hair, red eyes, flame", "alias": "shana"},

    # 2010s
    {"tags": "1girl, akemi homura, mahou shoujo madoka magica, black hair, purple eyes, hairband", "alias": "homura"},
    {"tags": "1girl, rem, re:zero, blue hair, blue eyes, maid, x hair ornament", "alias": "rem"},
    {"tags": "1girl, zero two, darling in the franxx, pink hair, green eyes, horns", "alias": "zero_two"},

    # 2020s
    {"tags": "1girl, yor briar, spy x family, black hair, red eyes, earrings, elegant", "alias": "yor"},
    {"tags": "1girl, kitagawa marin, sono bisque doll, blonde hair, brown eyes, gyaru", "alias": "marin"},
    {"tags": "1girl, nishikigi chisato, lycoris recoil, blonde hair, red eyes, hair ribbon", "alias": "chisato"},

    # 보컬로이드 / 게임
    {"tags": "1girl, hatsune miku, vocaloid, aqua hair, twintails, aqua eyes, headset", "alias": "miku"},
    {"tags": "1girl, furina, genshin impact, blue hair, blue eyes, hat, top hat", "alias": "furina"},
]

# 새로 추가한 장면 위주
SCENES = [
    # 일본 지역
    {"tags": "nara, deer, temple, ancient", "alias": "nara"},
    {"tags": "kyoto, torii gate, shrine, traditional", "alias": "kyoto"},
    {"tags": "tokyo, city lights, night, neon", "alias": "tokyo"},
    {"tags": "okinawa, tropical, clear water, palm tree", "alias": "okinawa"},
    {"tags": "hokkaido, lavender field, countryside", "alias": "hokkaido"},
    {"tags": "kamakura, great buddha, seaside town", "alias": "kamakura"},

    # 감성 장면
    {"tags": "empty classroom, sunset, desk, memories", "alias": "classroom"},
    {"tags": "staircase, school, leaning on railing, alone", "alias": "stairs"},
    {"tags": "rainy window, indoors, warm light, tea cup", "alias": "rainy_window"},
    {"tags": "old bookstore, dim light, dusty shelves", "alias": "bookstore"},
    {"tags": "train, window seat, passing scenery, travel", "alias": "train"},
    {"tags": "night walk, streetlight, puddle, reflection", "alias": "night_walk"},
    {"tags": "laundromat, late night, fluorescent light", "alias": "laundromat"},
    {"tags": "convenience store, night, glass door, warm glow", "alias": "konbini"},
    {"tags": "park bench, autumn, alone, falling leaves", "alias": "park_bench"},
    {"tags": "record store, vinyl, headphones, listening", "alias": "record_shop"},
    {"tags": "bicycle, riverside, golden hour, wind", "alias": "bicycle"},
    {"tags": "vending machine, night, glow, cicada", "alias": "vending"},
    {"tags": "pier, calm sea, early morning, mist", "alias": "pier"},
    {"tags": "graduation, diploma, tears, cherry blossoms", "alias": "graduation"},

    # 분위기
    {"tags": "fireworks, yukata, summer festival", "alias": "matsuri"},
    {"tags": "bridge, river, reflection, dusk", "alias": "bridge"},
    {"tags": "alley, lantern, old town, nostalgic", "alias": "alley"},
    {"tags": "seaside, ocean, waves, beach", "alias": "seaside"},
    {"tags": "field of flowers, meadow, breeze", "alias": "flower_field"},
]

EXPRESSIONS = [
    {"tags": "gentle smile, soft expression", "alias": "gentle"},
    {"tags": "melancholic, wistful", "alias": "sad"},
    {"tags": "peaceful, serene", "alias": "peaceful"},
    {"tags": "contemplative, thoughtful", "alias": "think"},
    {"tags": "confident, cool", "alias": "cool"},
    {"tags": "nostalgic, bittersweet smile", "alias": "nostalgic"},
    {"tags": "surprised, wide eyes", "alias": "surprised"},
]

TOTAL_IMAGES = 200


def build_prompt(char: dict, scene: dict, expr: dict) -> tuple[str, str]:
    positive = f"{char['tags']}, {expr['tags']}, {scene['tags']}, masterpiece, best quality, absurdres"
    negative = "lowres, bad anatomy, bad hands, error, text, signature"
    return positive, negative


def build_filename(preset: str, char: dict, scene: dict) -> str:
    return f"{preset}_{char['alias']}_{scene['alias']}"


async def generate_and_save(
    client: httpx.AsyncClient,
    prompt: str,
    negative: str,
    preset: str,
    filename: str,
) -> dict:
    payload = {
        "prompt": prompt,
        "negative_prompt": negative,
        "width": 832,
        "height": 1216,
        "style": preset,
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
            return {"success": False, "error": result.get("error", "No image")}

    except Exception as e:
        return {"success": False, "error": str(e)}


async def main():
    all_jobs = []
    for _ in range(TOTAL_IMAGES):
        preset = random.choice(PRESETS)
        char = random.choice(CHARACTERS)
        scene = random.choice(SCENES)
        expr = random.choice(EXPRESSIONS)
        all_jobs.append((preset, char, scene, expr))

    random.shuffle(all_jobs)

    success_count = 0
    fail_count = 0

    print(f"새 장면 배치 생성")
    print(f"저장 폴더: {OUTPUT_DIR}")
    print(f"총 {TOTAL_IMAGES}장 생성 예정")
    print(f"캐릭터 {len(CHARACTERS)}명 / 장면 {len(SCENES)}개 / 프리셋 {len(PRESETS)}개")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, (preset, char, scene, expr) in enumerate(all_jobs, 1):
            prompt, negative = build_prompt(char, scene, expr)
            filename = build_filename(preset, char, scene)

            print(f"[{i:03d}/{TOTAL_IMAGES}] [{preset}] {filename}", end=" ")

            result = await generate_and_save(client, prompt, negative, preset, filename)

            if result["success"]:
                success_count += 1
                print(f"OK (seed: {result['seed']})")
            else:
                fail_count += 1
                print(f"FAIL: {result.get('error', '?')}")

            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"완료! 성공: {success_count}, 실패: {fail_count}")
    print(f"저장 위치: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
