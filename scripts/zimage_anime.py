"""
Z-Image Turbo - 애니메이션 스타일 테스트
자연어 프롬프트 기반 (태그 X)
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_zimage_anime"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    # === 교토 애니메이션 스타일 ===
    {
        "prompt": "Anime girl with short brown hair and brown eyes sitting in a cozy cafe, Kyoto Animation style, soft warm lighting, detailed interior background, gentle atmosphere, holding a coffee cup",
        "alias": "kyoani_cafe",
    },
    {
        "prompt": "Anime girl with long black hair reading a book by the window, Kyoto Animation style, afternoon sunlight streaming in, peaceful school library, soft shadows, delicate expression",
        "alias": "kyoani_library",
    },
    {
        "prompt": "Anime girl with blonde hair playing guitar on a school rooftop at sunset, Kyoto Animation style, golden hour lighting, wind blowing hair, warm orange sky, nostalgic mood",
        "alias": "kyoani_sunset",
    },

    # === 신카이 마코토 스타일 ===
    {
        "prompt": "Anime girl standing under cherry blossom trees, Makoto Shinkai style, breathtaking sky with dramatic clouds, lens flare, petals falling, cinematic composition, ultra detailed background",
        "alias": "shinkai_sakura",
    },
    {
        "prompt": "Anime girl looking up at a starry night sky from a hilltop, Makoto Shinkai style, milky way visible, city lights in the distance, atmospheric perspective, emotional scene",
        "alias": "shinkai_stars",
    },
    {
        "prompt": "Anime girl with umbrella walking through rain-soaked city streets, Makoto Shinkai style, neon reflections on wet pavement, twilight sky, cinematic depth of field",
        "alias": "shinkai_rain",
    },

    # === 지브리 스타일 ===
    {
        "prompt": "Anime girl in a white dress exploring a lush green forest, Studio Ghibli style, warm earthy colors, dappled sunlight through trees, hand-painted look, peaceful nature scene",
        "alias": "ghibli_forest",
    },
    {
        "prompt": "Anime girl sitting on a grassy hillside with a small cottage in the background, Studio Ghibli style, fluffy cumulus clouds, wildflowers, idyllic countryside, nostalgic summer day",
        "alias": "ghibli_hill",
    },

    # === 사이버펑크 ===
    {
        "prompt": "Anime girl with neon-lit cyberpunk outfit standing in a futuristic alley, rain falling, holographic signs, dramatic purple and cyan lighting, reflective puddles, dark atmosphere",
        "alias": "cyber_alley",
    },
    {
        "prompt": "Anime girl hacker sitting in a dark room surrounded by floating holographic screens, cyberpunk style, blue glow on face, futuristic headset, moody atmosphere",
        "alias": "cyber_hacker",
    },

    # === 유포테이블 액션 ===
    {
        "prompt": "Anime girl swordsman in dynamic action pose, ufotable animation style, glowing magical effects, dramatic lighting, flowing hair, intense expression, energy particles",
        "alias": "ufo_action",
    },
    {
        "prompt": "Anime girl mage casting a spell, ufotable style, swirling fire and light effects, dramatic camera angle from below, detailed costume, vibrant colors against dark background",
        "alias": "ufo_magic",
    },

    # === 파스텔/몽환 ===
    {
        "prompt": "Anime girl in a dreamy pastel flower garden, soft pink and lavender tones, gentle lighting, delicate features, flowing white dress, ethereal atmosphere, bokeh background",
        "alias": "pastel_garden",
    },
    {
        "prompt": "Anime girl floating in a surreal pastel sky surrounded by clouds and stars, dreamy watercolor style, soft muted colors, peaceful sleeping expression, fantasy atmosphere",
        "alias": "pastel_dream",
    },

    # === 90년대 레트로 ===
    {
        "prompt": "Anime girl in 90s retro anime style, cel shaded, warm earthy tones, film grain texture, nostalgic atmosphere, school uniform, hand-drawn feel, old school anime aesthetic",
        "alias": "retro_school",
    },
    {
        "prompt": "Anime girl vocalist in punk outfit under city lights, 90s anime aesthetic, bold linework, moody color palette, cigarette smoke, urban night scene, NANA anime vibes",
        "alias": "retro_punk",
    },

    # === 모노가타리/샤프트 ===
    {
        "prompt": "Anime girl with long purple hair doing a head tilt pose, Shaft animation studio style, abstract geometric background, high contrast, artistic composition, sharp eye detail, flat color areas",
        "alias": "shaft_headtilt",
    },
    {
        "prompt": "Anime girl standing alone in an empty colorful room, monogatari series style, minimalist abstract background, dramatic shadow, clean lineart, large expressive eyes, artistic framing",
        "alias": "shaft_mono",
    },

    # === 수채화 스케치 ===
    {
        "prompt": "Anime girl portrait with faint pencil sketch lines and pale watercolor wash, desaturated colors, paper texture visible, melancholic expression, soft diffused light, ethereal nostalgic atmosphere",
        "alias": "watercolor_portrait",
    },
    {
        "prompt": "Anime girl playing violin in a sunlit room, watercolor painting style, visible brushstrokes, soft bleeding colors, warm light from window, artistic and delicate rendering",
        "alias": "watercolor_violin",
    },

    # === MAPPA 다크 시네마틱 ===
    {
        "prompt": "Anime girl with short white hair in a dark battlefield, MAPPA animation style, intense cinematic lighting, rain and blood, dramatic atmosphere, detailed expression of determination",
        "alias": "mappa_battle",
    },
    {
        "prompt": "Anime girl standing on a rooftop overlooking a dark cityscape at night, MAPPA style, moody blue and grey tones, wind blowing coat, lonely silhouette against moonlight",
        "alias": "mappa_rooftop",
    },
    {
        "prompt": "Anime girl assassin crouching in shadows, MAPPA animation style, high contrast lighting, red eyes glowing in darkness, tense atmosphere, detailed clothing wrinkles",
        "alias": "mappa_shadow",
    },

    # === 트리거 다이나믹 ===
    {
        "prompt": "Anime girl in an explosive dynamic pose with colorful energy trails, Trigger studio style, exaggerated perspective, speed lines, vivid saturated colors, maximum impact composition",
        "alias": "trigger_burst",
    },
    {
        "prompt": "Anime girl pilot in a mech cockpit with flashing controls, Trigger animation style, vibrant neon colors, intense expression, dramatic diagonal composition, sci-fi atmosphere",
        "alias": "trigger_mech",
    },

    # === 판타지 RPG ===
    {
        "prompt": "Anime elf girl mage with long silver hair and pointed ears in an enchanted forest, fantasy RPG style, glowing magical particles, ornate staff, detailed fantasy costume with gold embroidery",
        "alias": "fantasy_elf",
    },
    {
        "prompt": "Anime girl knight in silver armor standing before a grand castle gate, epic fantasy style, dramatic sunset sky, flowing red cape, majestic atmosphere, detailed medieval architecture",
        "alias": "fantasy_knight",
    },
    {
        "prompt": "Anime girl alchemist in a cluttered magical workshop, fantasy style, glowing potions, floating books, warm candlelight, mysterious atmosphere, detailed interior with magical artifacts",
        "alias": "fantasy_alchemy",
    },

    # === 학원/일상 ===
    {
        "prompt": "Anime girl leaning on a school corridor window during golden hour, slice of life style, warm afternoon light, gentle breeze, cherry blossom petals drifting in, peaceful everyday moment",
        "alias": "school_corridor",
    },
    {
        "prompt": "Anime girl in summer festival yukata holding cotton candy, festival stalls with lanterns in background, warm evening glow, cheerful expression, detailed traditional Japanese pattern on yukata",
        "alias": "festival_yukata",
    },
    {
        "prompt": "Anime girl studying at her desk late at night with a desk lamp, cozy bedroom interior, soft warm light, tired but focused expression, books and notes scattered, realistic everyday scene",
        "alias": "study_night",
    },

    # === 고딕/다크 ===
    {
        "prompt": "Anime girl in gothic lolita dress sitting on an ornate throne in a dark cathedral, stained glass windows with moonlight streaming through, roses, elegant and dark atmosphere",
        "alias": "gothic_cathedral",
    },
    {
        "prompt": "Anime vampire girl with crimson eyes and pale skin under a blood moon, gothic style, dark flowing dress, bats in background, hauntingly beautiful, dark romantic atmosphere",
        "alias": "gothic_vampire",
    },

    # === 클로즈업 포트레이트 ===
    {
        "prompt": "Close-up portrait of an anime girl with heterochromia eyes, one blue and one gold, detailed iris rendering, soft studio lighting, slight smile, flowing silver hair framing face",
        "alias": "portrait_hetero",
    },
    {
        "prompt": "Close-up portrait of an anime girl with tears streaming down her face, emotional expression, rain in background, dramatic backlighting, detailed eye reflections, cinematic mood",
        "alias": "portrait_tears",
    },
    {
        "prompt": "Close-up portrait of anime girl with fox ears and amber eyes, playful wink expression, autumn leaves in hair, warm golden lighting, soft bokeh background, cute and charming",
        "alias": "portrait_fox",
    },

    # === 계절/날씨 ===
    {
        "prompt": "Anime girl in a thick winter coat walking through heavy snowfall in a quiet town, warm scarf and mittens, breath visible in cold air, street lamps glowing warmly, peaceful winter night",
        "alias": "season_winter",
    },
    {
        "prompt": "Anime girl lying in a field of sunflowers on a bright summer day, straw hat on chest, blue sky with white clouds, warm golden sunlight, relaxed happy expression, vivid colors",
        "alias": "season_summer",
    },
    {
        "prompt": "Anime girl walking through a path lined with autumn maple trees, red and orange leaves falling, golden afternoon light, cozy cardigan and scarf, melancholic beautiful atmosphere",
        "alias": "season_autumn",
    },

    # === 음악/밴드 ===
    {
        "prompt": "Anime girl bassist performing on a live house stage with dramatic purple stage lighting, sweat on forehead, passionate expression, electric bass guitar detail, energetic crowd silhouettes",
        "alias": "band_bassist",
    },
    {
        "prompt": "Anime girl with headphones sitting in a record shop, surrounded by vinyl records, warm retro interior, afternoon sunlight, relaxed expression listening to music, vintage aesthetic",
        "alias": "band_records",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "ugly, blurry, deformed, extra fingers, bad anatomy, low quality, watermark, text, signature",
        "width": 1024,
        "height": 1024,
        "steps": 8,
        "guidance_scale": 0.0,
        "model": "z-image-turbo",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"Z-Image Turbo 애니메이션 스타일 테스트 {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
