"""
300장 다양한 이미지 배치 생성 스크립트
캐릭터 x 스타일 x 장면 x 표정 조합
"""

import asyncio
import random
import httpx
from dataclasses import dataclass
from itertools import product

API_URL = "http://localhost:8002/api/generate"

# ============================================
# 캐릭터 정의
# ============================================

CHARACTERS = {
    # 체인소맨 - 레제 위주
    "reze_csm": {
        "name": "reze",
        "series": "chainsaw man",
        "tags": "purple hair, short hair, red eyes, beautiful, mature",
        "alias": "reze"
    },
    "reze_casual": {
        "name": "reze",
        "series": "chainsaw man",
        "tags": "purple hair, short hair, red eyes, casual clothes, beautiful",
        "alias": "reze_casual"
    },
    "makima": {
        "name": "makima",
        "series": "chainsaw man",
        "tags": "orange hair, long hair, braided ponytail, yellow eyes, ringed eyes, formal suit",
        "alias": "makima"
    },
    "power_csm": {
        "name": "power",
        "series": "chainsaw man",
        "tags": "blonde hair, long hair, red horns, sharp teeth, red eyes, fiend",
        "alias": "power"
    },
    "asa_mitaka": {
        "name": "asa mitaka",
        "series": "chainsaw man",
        "tags": "brown hair, short hair, brown eyes, school uniform, scar on face",
        "alias": "asa"
    },

    # 케이온
    "yui_keion": {
        "name": "hirasawa yui",
        "series": "k-on!",
        "tags": "brown hair, short hair, brown eyes, hairpin, cheerful",
        "alias": "yui"
    },
    "mio_keion": {
        "name": "akiyama mio",
        "series": "k-on!",
        "tags": "black hair, long hair, grey eyes, shy, elegant",
        "alias": "mio"
    },
    "ritsu_keion": {
        "name": "tainaka ritsu",
        "series": "k-on!",
        "tags": "brown hair, short hair, hairband, yellow eyes, energetic",
        "alias": "ritsu"
    },
    "mugi_keion": {
        "name": "kotobuki tsumugi",
        "series": "k-on!",
        "tags": "blonde hair, long hair, blue eyes, thick eyebrows, ojou-sama",
        "alias": "mugi"
    },
    "azusa_keion": {
        "name": "nakano azusa",
        "series": "k-on!",
        "tags": "black hair, twintails, red eyes, cat ears hair ornament",
        "alias": "azusa"
    },

    # 봇치더록
    "bocchi": {
        "name": "gotoh hitori",
        "series": "bocchi the rock!",
        "tags": "pink hair, long hair, blue eyes, shy, anxious, cube hair ornament",
        "alias": "bocchi"
    },
    "nijika": {
        "name": "ijichi nijika",
        "series": "bocchi the rock!",
        "tags": "blonde hair, short hair, blue eyes, star hair ornament, cheerful",
        "alias": "nijika"
    },
    "ryo_btr": {
        "name": "yamada ryo",
        "series": "bocchi the rock!",
        "tags": "blue hair, long hair, blue eyes, stoic, cool, lazy",
        "alias": "ryo"
    },
    "kita": {
        "name": "kita ikuyo",
        "series": "bocchi the rock!",
        "tags": "red hair, long hair, green eyes, cheerful, energetic",
        "alias": "kita"
    },
    # 키쿠리 바리에이션 (비중 UP)
    "kikuri": {
        "name": "hiroi kikuri",
        "series": "bocchi the rock!",
        "tags": "purple hair, long hair, red eyes, drunk, mature, bassist, beautiful",
        "alias": "kikuri"
    },
    "kikuri_sober": {
        "name": "hiroi kikuri",
        "series": "bocchi the rock!",
        "tags": "purple hair, long hair, red eyes, serious, cool, bassist, beautiful",
        "alias": "kikuri_sober"
    },
    "kikuri_stage": {
        "name": "hiroi kikuri",
        "series": "bocchi the rock!",
        "tags": "purple hair, long hair, red eyes, playing bass, passionate, stage outfit",
        "alias": "kikuri_stage"
    },
    "kikuri_casual": {
        "name": "hiroi kikuri",
        "series": "bocchi the rock!",
        "tags": "purple hair, long hair, red eyes, casual clothes, relaxed, mature",
        "alias": "kikuri_casual"
    },
    "kikuri_mentor": {
        "name": "hiroi kikuri",
        "series": "bocchi the rock!",
        "tags": "purple hair, long hair, red eyes, gentle smile, teaching, motherly",
        "alias": "kikuri_mentor"
    },

    # 바케모노가타리
    "senjougahara": {
        "name": "senjougahara hitagi",
        "series": "bakemonogatari",
        "tags": "purple hair, long hair, sharp eyes, tsundere, beautiful, elegant",
        "alias": "hitagi"
    },
    "hanekawa": {
        "name": "hanekawa tsubasa",
        "series": "bakemonogatari",
        "tags": "black hair, long hair, glasses, braids, class president",
        "alias": "hanekawa"
    },
    "nadeko": {
        "name": "sengoku nadeko",
        "series": "bakemonogatari",
        "tags": "orange hair, long hair, bangs covering eyes, shy, cute",
        "alias": "nadeko"
    },
    "shinobu": {
        "name": "oshino shinobu",
        "series": "bakemonogatari",
        "tags": "blonde hair, long hair, yellow eyes, vampire, loli, gothic",
        "alias": "shinobu"
    },
    "kanbaru": {
        "name": "kanbaru suruga",
        "series": "bakemonogatari",
        "tags": "short hair, brown hair, athletic, sporty, tomboyish",
        "alias": "kanbaru"
    },
    "kaiki": {
        "name": "kaiki deishuu",
        "series": "bakemonogatari",
        "tags": "black hair, beard, suit, mysterious, con artist",
        "alias": "kaiki"
    },

    # NANA
    "nana_osaki": {
        "name": "osaki nana",
        "series": "nana",
        "tags": "black hair, short hair, punk, gothic, cigarette, cool, vocalist",
        "alias": "nana_o"
    },
    "nana_komatsu": {
        "name": "komatsu nana",
        "series": "nana",
        "tags": "brown hair, long hair, brown eyes, cute, girly, innocent",
        "alias": "hachi"
    },
    "ren": {
        "name": "honjo ren",
        "series": "nana",
        "tags": "black hair, long hair, handsome, guitarist, cool, mature",
        "alias": "ren"
    },
    "shin": {
        "name": "okazaki shinichi",
        "series": "nana",
        "tags": "blonde hair, young, bassist, pretty boy",
        "alias": "shin"
    },

    # 장송의 프리렌
    "frieren": {
        "name": "frieren",
        "series": "sousou no frieren",
        "tags": "white hair, long hair, elf ears, green eyes, mage, stoic",
        "alias": "frieren"
    },
    "fern": {
        "name": "fern",
        "series": "sousou no frieren",
        "tags": "purple hair, long hair, mage, serious, tall",
        "alias": "fern"
    },

    # 약사의 혼잣말
    "maomao": {
        "name": "maomao",
        "series": "kusuriya no hitorigoto",
        "tags": "brown hair, short hair, green eyes, freckles, apothecary, curious",
        "alias": "maomao"
    },

    # 주술회전
    "gojo": {
        "name": "gojo satoru",
        "series": "jujutsu kaisen",
        "tags": "white hair, blue eyes, blindfold, tall, handsome, confident",
        "alias": "gojo"
    },
    "nobara": {
        "name": "kugisaki nobara",
        "series": "jujutsu kaisen",
        "tags": "orange hair, short hair, confident, hammer, nails",
        "alias": "nobara"
    },

    # 로젠메이든
    "shinku": {
        "name": "shinku",
        "series": "rozen maiden",
        "tags": "blonde hair, twintails, red eyes, gothic lolita, red dress, doll",
        "alias": "shinku"
    },
    "suiseiseki": {
        "name": "suiseiseki",
        "series": "rozen maiden",
        "tags": "green hair, twin drills, heterochromia, gothic lolita, green dress, doll",
        "alias": "suiseiseki"
    },
    "suigintou": {
        "name": "suigintou",
        "series": "rozen maiden",
        "tags": "silver hair, long hair, red eyes, gothic lolita, black dress, wings, doll",
        "alias": "suigintou"
    },
}

# ============================================
# 스타일 정의
# ============================================

STYLES = {
    "gouache_cozy": {
        "tags": "gouache painting style, soft colors, pastel colors, cozy, warm atmosphere, dreamy, artistic",
        "negative_extra": "vibrant colors, saturated, high contrast",
        "cfg": 5.5
    },
    "ghibli_watercolor": {
        "tags": "studio ghibli style, watercolor, soft lighting, hand-painted, dreamy, nostalgic, warm colors",
        "negative_extra": "3d, realistic, sharp lines",
        "cfg": 5.5
    },
    "cyberpunk_neon": {
        "tags": "cyberpunk, neon lights, rain, night city, futuristic, reflections, dramatic lighting",
        "negative_extra": "bright, daylight, soft",
        "cfg": 6.5
    },
    "retro_80s": {
        "tags": "year 1990, retro anime style, cel shading, vintage, old school anime, nostalgic",
        "negative_extra": "modern, digital, clean lines",
        "cfg": 6.0
    },
    "flat_color": {
        "tags": "flat color, clean lines, minimal shading, simple background, graphic style",
        "negative_extra": "gradient, realistic shading, detailed background",
        "cfg": 6.0
    },
    "watercolor_sketch": {
        "tags": "watercolor sketch, loose brushstrokes, soft edges, artistic, delicate, light colors",
        "negative_extra": "sharp, bold, dark",
        "cfg": 5.0
    },
    "soft_pastel": {
        "tags": "soft colors, pastel colors, gentle lighting, dreamy, ethereal, delicate, muted tones",
        "negative_extra": "vibrant, saturated, harsh lighting",
        "cfg": 5.5
    },
    "cinematic": {
        "tags": "cinematic lighting, dramatic, film grain, depth of field, atmospheric, moody",
        "negative_extra": "flat lighting, simple",
        "cfg": 6.5
    },
    "pixel_art": {
        "tags": "pixel art, 16bit, retro game style, sprite, pixelated",
        "negative_extra": "3d, realistic, smooth",
        "cfg": 6.0,
        "size": (512, 512)
    },
    "line_art": {
        "tags": "line art, sketch, monochrome, detailed linework, clean lines, white background",
        "negative_extra": "color, shading, painted",
        "cfg": 6.0
    },
}

# ============================================
# 장면/상황 정의
# ============================================

SCENES = {
    "cafe": {
        "tags": "cafe, holding coffee cup, sitting, table, cozy interior, warm lighting",
        "filename": "cafe"
    },
    "rain": {
        "tags": "rain, holding umbrella, wet, puddles, reflection, melancholy",
        "filename": "rain"
    },
    "cherry_blossom": {
        "tags": "cherry blossoms, petals, spring, wind, hair blowing, outdoors",
        "filename": "sakura"
    },
    "night_city": {
        "tags": "night, city street, neon lights, urban, walking",
        "filename": "night_city"
    },
    "sunset": {
        "tags": "sunset, golden hour, orange sky, rooftop, peaceful",
        "filename": "sunset"
    },
    "library": {
        "tags": "library, bookshelves, reading book, quiet, dust particles, soft lighting",
        "filename": "library"
    },
    "concert": {
        "tags": "concert, stage, spotlight, microphone, performance, energetic",
        "filename": "concert"
    },
    "bedroom": {
        "tags": "bedroom, bed, morning, sunlight through window, waking up, cozy",
        "filename": "bedroom"
    },
    "snow": {
        "tags": "snow, winter, scarf, breath visible, cold, snowflakes",
        "filename": "snow"
    },
    "beach": {
        "tags": "beach, ocean, summer, swimsuit, waves, sand, sunny",
        "filename": "beach"
    },
    "forest": {
        "tags": "forest, trees, nature, sunlight filtering through leaves, peaceful",
        "filename": "forest"
    },
    "studio": {
        "tags": "music studio, instruments, recording, headphones, focused",
        "filename": "studio"
    },
    "window": {
        "tags": "window, looking outside, contemplative, indoor, soft lighting",
        "filename": "window"
    },
    "starry_night": {
        "tags": "starry sky, night, stars, moon, looking up, peaceful",
        "filename": "starry"
    },
    "simple": {
        "tags": "simple background, upper body, looking at viewer",
        "filename": "portrait"
    },
}

# ============================================
# 표정 정의
# ============================================

EXPRESSIONS = {
    "smile": {"tags": "smile, happy, cheerful", "filename": "smile"},
    "gentle": {"tags": "gentle smile, soft expression, warm", "filename": "gentle"},
    "cool": {"tags": "cool, confident, slight smile", "filename": "cool"},
    "shy": {"tags": "shy, blush, looking away, embarrassed", "filename": "shy"},
    "serious": {"tags": "serious, focused, determined", "filename": "serious"},
    "melancholy": {"tags": "melancholy, sad eyes, wistful", "filename": "sad"},
    "tsundere": {"tags": "tsundere, blush, annoyed, looking away", "filename": "tsun"},
    "peaceful": {"tags": "peaceful, eyes closed, serene", "filename": "peaceful"},
    "playful": {"tags": "playful, wink, teasing, mischievous", "filename": "playful"},
    "sleepy": {"tags": "sleepy, tired, half-closed eyes, yawning", "filename": "sleepy"},
}

# ============================================
# 공통 태그
# ============================================

QUALITY_POSITIVE = "masterpiece, best quality, high score, great score, absurdres, detailed"
QUALITY_NEGATIVE = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry"


def build_prompt(character: dict, style: dict, scene: dict, expression: dict) -> tuple[str, str]:
    """프롬프트 조합"""
    # Positive
    char_tags = f"1girl, {character['name']}, {character['series']}, {character['tags']}"
    if "1boy" in character.get('tags', '') or character['alias'] in ['kaiki', 'ren', 'shin', 'gojo']:
        char_tags = f"1boy, {character['name']}, {character['series']}, {character['tags']}"

    positive = f"{char_tags}, {expression['tags']}, {scene['tags']}, {style['tags']}, {QUALITY_POSITIVE}"

    # Negative
    negative = f"{QUALITY_NEGATIVE}, {style.get('negative_extra', '')}"

    return positive, negative


def generate_filename(character: dict, style_name: str, scene: dict, expression: dict) -> str:
    """파일명 생성"""
    return f"{character['alias']}_{style_name}_{scene['filename']}_{expression['filename']}"


async def generate_image(client: httpx.AsyncClient, prompt: str, negative: str, filename: str, style: dict) -> dict:
    """이미지 생성 API 호출"""
    size = style.get("size", (832, 1216))

    payload = {
        "prompt": prompt,
        "negative_prompt": negative,
        "width": size[0],
        "height": size[1],
        "steps": 30,
        "guidance_scale": style.get("cfg", 5.5),
        "filename": filename
    }

    try:
        response = await client.post(API_URL, json=payload, timeout=300.0)
        result = response.json()
        return {
            "success": result.get("success", False),
            "filename": result.get("filename"),
            "seed": result.get("seed"),
            "error": result.get("error")
        }
    except Exception as e:
        return {"success": False, "error": str(e), "filename": filename}


async def main():
    # 조합 생성 (300장 목표)
    all_combinations = []

    characters = list(CHARACTERS.values())
    styles = list(STYLES.items())
    scenes = list(SCENES.values())
    expressions = list(EXPRESSIONS.values())

    # 모든 조합에서 랜덤 샘플링
    for char in characters:
        for style_name, style in styles:
            # 각 캐릭터 x 스타일 당 1~2개 장면/표정 조합
            sampled_scenes = random.sample(scenes, min(2, len(scenes)))
            sampled_expressions = random.sample(expressions, min(2, len(expressions)))

            for scene in sampled_scenes:
                for expr in sampled_expressions:
                    all_combinations.append((char, style_name, style, scene, expr))

    # 300장으로 제한
    random.shuffle(all_combinations)
    selected = all_combinations[:300]

    print(f"총 {len(selected)}장 생성 예정")
    print("=" * 50)

    async with httpx.AsyncClient() as client:
        for i, (char, style_name, style, scene, expr) in enumerate(selected, 1):
            prompt, negative = build_prompt(char, style, scene, expr)
            filename = generate_filename(char, style_name, scene, expr)

            print(f"[{i:03d}/300] {filename}")

            result = await generate_image(client, prompt, negative, filename, style)

            if result["success"]:
                print(f"  -> OK: {result['filename']} (seed: {result['seed']})")
            else:
                print(f"  -> FAIL: {result.get('error', 'Unknown error')}")

            # 연속 생성 시 약간의 딜레이
            await asyncio.sleep(0.5)

    print("=" * 50)
    print("완료!")


if __name__ == "__main__":
    asyncio.run(main())
