"""냥냥돌쇠 D버전 100장 - 점 일관성 + 다양한 프리셋"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_nyang_dolsoe_D100"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 점: 오른눈밑2 + 왼눈밑1 + 목왼쪽1
CHAR = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes, facial mole, multiple moles, mole under eye, mole on neck"
NEG = "moles on body, mole on forehead, mole on nose"

JOBS = [
    # === pale_aqua (40장) ===
    {"prompt": f"{CHAR}, white blouse, face close-up, looking at viewer, soft light, portrait", "alias": "pa01_front", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, turtleneck, face close-up, three quarter view, warm light, portrait", "alias": "pa02_quarter", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, school uniform, face close-up, slight smile, classroom, portrait", "alias": "pa03_school", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, black dress, face close-up, cool expression, dark background, portrait", "alias": "pa04_dark", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, kimono, face close-up, cherry blossoms, elegant, portrait", "alias": "pa05_kimono", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, off shoulder sweater, upper body, window light, melancholic, portrait", "alias": "pa06_neck", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, maid outfit, face close-up, slight blush, soft light, portrait", "alias": "pa07_maid", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, hoodie, face close-up, sleepy, morning light, portrait", "alias": "pa08_morning", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, suit, necktie, upper body, confident, office, portrait", "alias": "pa09_suit", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, chinese dress, red, upper body, night market, lanterns, portrait", "alias": "pa10_china", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, detective coat, hat, rainy street, side profile, night, portrait", "alias": "pa11_detective", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, bartender vest, bar counter, dim light, cool, upper body", "alias": "pa12_bar", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, military uniform, beret, arms crossed, serious, upper body", "alias": "pa13_military", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, nurse uniform, arms behind back, hospital, calm, upper body", "alias": "pa14_nurse", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, black dress, piano, spotlight, elegant, side profile", "alias": "pa15_pianist", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, school uniform, rooftop, sunset, wind, hair blowing, upper body", "alias": "pa16_rooftop", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, headphones, night, convenience store, casual, face close-up", "alias": "pa17_konbini", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, kyudo outfit, bow, dojo, focused, side profile, upper body", "alias": "pa18_kyudo", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, lab coat, glasses, clipboard, serious, upper body", "alias": "pa19_scientist", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, leather jacket, night city, wind, cool, side profile, upper body", "alias": "pa20_biker", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, winter coat, scarf, snow, night, face close-up, portrait", "alias": "pa21_snow", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, swimsuit, beach, summer, cheerful, upper body", "alias": "pa22_beach", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, witch hat, cloak, halloween, pumpkins, playful, upper body", "alias": "pa23_witch", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, gothic lolita, black dress, parasol, rose garden, elegant, upper body", "alias": "pa24_gothic", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, yukata, summer festival, lanterns, evening, gentle smile, face close-up", "alias": "pa25_yukata", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, apron, kitchen, mixing bowl, flour on cheek, happy, upper body", "alias": "pa26_baking", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, pajamas, yawning, bed, morning light, sleepy, face close-up", "alias": "pa27_pajama", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, raincoat, rain, umbrella, puddle, outdoor, upper body", "alias": "pa28_rain", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, gym clothes, track field, daytime, sporty, upper body", "alias": "pa29_gym", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, artist smock, paintbrush, art studio, colorful, happy, upper body", "alias": "pa30_artist", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, idol costume, stage, colorful lights, wink, face close-up", "alias": "pa31_idol", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, armor, sword, mountain cliff, sunrise, confident, upper body", "alias": "pa32_warrior", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, evening dress, balcony, moonlight, elegant, upper body", "alias": "pa33_evening", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, volleyball uniform, gymnasium, dynamic, determined, upper body", "alias": "pa34_volley", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, cardigan, reading, library window, afternoon light, upper body", "alias": "pa35_reading", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, leather apron, blacksmith, forge, fire glow, serious, upper body", "alias": "pa36_smith", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, astronaut suit, helmet off, stars, space station, upper body", "alias": "pa37_space", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, chef uniform, kitchen, tasting, calm, upper body", "alias": "pa38_chef", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, florist apron, flower shop, roses, warm light, gentle, upper body", "alias": "pa39_florist", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, vampire, red eyes, fangs, moonlight, dark, face close-up", "alias": "pa40_vamp", "style": "pale_aqua"},

    # === monogatari (10장) ===
    {"prompt": f"{CHAR}, school uniform, head tilt, looking at viewer, face close-up, portrait", "alias": "mn01_tilt", "style": "monogatari"},
    {"prompt": f"{CHAR}, white dress, wind, hair blowing, rooftop, face close-up", "alias": "mn02_wind", "style": "monogatari"},
    {"prompt": f"{CHAR}, black turtleneck, side profile, night sky, portrait", "alias": "mn03_night", "style": "monogatari"},
    {"prompt": f"{CHAR}, casual clothes, sitting, cafe, looking away, upper body", "alias": "mn04_cafe", "style": "monogatari"},
    {"prompt": f"{CHAR}, sundress, flower field, summer, gentle smile, face close-up", "alias": "mn05_field", "style": "monogatari"},
    {"prompt": f"{CHAR}, oversized shirt, bedroom, morning, sleepy, face close-up", "alias": "mn06_lazy", "style": "monogatari"},
    {"prompt": f"{CHAR}, blazer, library, books, intellectual, upper body", "alias": "mn07_lib", "style": "monogatari"},
    {"prompt": f"{CHAR}, swimsuit, pool, summer, wet hair, face close-up", "alias": "mn08_pool", "style": "monogatari"},
    {"prompt": f"{CHAR}, scarf, autumn, leaves falling, nostalgic, face close-up", "alias": "mn09_fall", "style": "monogatari"},
    {"prompt": f"{CHAR}, raincoat, rain, looking at viewer, cool, face close-up", "alias": "mn10_rain", "style": "monogatari"},

    # === pop_fanart (10장) ===
    {"prompt": f"{CHAR}, school uniform, peace sign, cheerful, face close-up", "alias": "pf01_peace", "style": "pop_fanart"},
    {"prompt": f"{CHAR}, hoodie, headphones, cool, looking at viewer, upper body", "alias": "pf02_cool", "style": "pop_fanart"},
    {"prompt": f"{CHAR}, maid outfit, serving tray, smile, upper body", "alias": "pf03_maid", "style": "pop_fanart"},
    {"prompt": f"{CHAR}, santa costume, christmas, wink, face close-up", "alias": "pf04_xmas", "style": "pop_fanart"},
    {"prompt": f"{CHAR}, bunny ears, easter, cute, face close-up", "alias": "pf05_bunny", "style": "pop_fanart"},
    {"prompt": f"{CHAR}, sailor uniform, wind, looking back, upper body", "alias": "pf06_sailor", "style": "pop_fanart"},
    {"prompt": f"{CHAR}, cat cafe, apron, holding cat plush, cute, upper body", "alias": "pf07_catcafe", "style": "pop_fanart"},
    {"prompt": f"{CHAR}, gym clothes, towel, sporty, face close-up", "alias": "pf08_gym", "style": "pop_fanart"},
    {"prompt": f"{CHAR}, nurse cap, white coat, calm, face close-up", "alias": "pf09_nurse", "style": "pop_fanart"},
    {"prompt": f"{CHAR}, detective hat, magnifying glass, smirk, upper body", "alias": "pf10_detect", "style": "pop_fanart"},

    # === cozy_gouache (5장) ===
    {"prompt": f"{CHAR}, knit sweater, hot cocoa, winter, cozy room, upper body", "alias": "cg01_cocoa", "style": "cozy_gouache"},
    {"prompt": f"{CHAR}, blanket, reading, fireplace, night, upper body", "alias": "cg02_fire", "style": "cozy_gouache"},
    {"prompt": f"{CHAR}, rain, window, tea cup, melancholic, face close-up", "alias": "cg03_tea", "style": "cozy_gouache"},
    {"prompt": f"{CHAR}, oversized sweater, cat on lap, couch, relaxed, upper body", "alias": "cg04_cat", "style": "cozy_gouache"},
    {"prompt": f"{CHAR}, camping, tent, starry sky, marshmallow, upper body", "alias": "cg05_camp", "style": "cozy_gouache"},

    # === watercolor_sketch (10장) ===
    {"prompt": f"{CHAR}, white dress, field, wind, ethereal, face close-up", "alias": "ws01_field", "style": "watercolor_sketch"},
    {"prompt": f"{CHAR}, umbrella, cherry blossoms, spring rain, dreamy, upper body", "alias": "ws02_sakura", "style": "watercolor_sketch"},
    {"prompt": f"{CHAR}, train station, platform, evening, lonely, upper body", "alias": "ws03_train", "style": "watercolor_sketch"},
    {"prompt": f"{CHAR}, rooftop, night, city lights, wind, melancholic, face close-up", "alias": "ws04_city", "style": "watercolor_sketch"},
    {"prompt": f"{CHAR}, forest, sunbeam, morning mist, peaceful, face close-up", "alias": "ws05_forest", "style": "watercolor_sketch"},
    {"prompt": f"{CHAR}, violin, concert hall, spotlight, elegant, upper body", "alias": "ws06_violin", "style": "watercolor_sketch"},
    {"prompt": f"{CHAR}, balcony, sunset, looking at sky, nostalgic, face close-up", "alias": "ws07_sunset", "style": "watercolor_sketch"},
    {"prompt": f"{CHAR}, beach, dawn, barefoot, sand, peaceful, upper body", "alias": "ws08_dawn", "style": "watercolor_sketch"},
    {"prompt": f"{CHAR}, piano, empty room, light from window, serene, upper body", "alias": "ws09_piano", "style": "watercolor_sketch"},
    {"prompt": f"{CHAR}, snow, bridge, river, winter morning, quiet, upper body", "alias": "ws10_bridge", "style": "watercolor_sketch"},

    # === kyoto_animation (5장) ===
    {"prompt": f"{CHAR}, school uniform, corridor, golden hour, gentle, upper body", "alias": "ka01_corridor", "style": "kyoto_animation"},
    {"prompt": f"{CHAR}, summer dress, riverside, cicadas, evening, face close-up", "alias": "ka02_river", "style": "kyoto_animation"},
    {"prompt": f"{CHAR}, classroom, window seat, breeze, daydream, face close-up", "alias": "ka03_dream", "style": "kyoto_animation"},
    {"prompt": f"{CHAR}, festival, goldfish scooping, summer night, fun, upper body", "alias": "ka04_fest", "style": "kyoto_animation"},
    {"prompt": f"{CHAR}, graduation, tears, cherry blossoms, bittersweet, face close-up", "alias": "ka05_grad", "style": "kyoto_animation"},

    # === pale_aqua 추가 (10장) ===
    {"prompt": f"{CHAR}, train, window, countryside, sunset, nostalgic, face close-up", "alias": "pa41_train", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, rooftop, meteor shower, night sky, amazed, upper body", "alias": "pa42_meteor", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, hilltop, clouds, golden hour, wind, peaceful, upper body", "alias": "pa43_hill", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, snow, street lamp, town, quiet night, face close-up", "alias": "pa44_snow2", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, leather jacket, sunglasses, cool, face close-up, portrait", "alias": "pa45_cool", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, tank top, boxing gloves, gym, fierce, upper body", "alias": "pa46_box", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, trench coat, rain, street, mysterious, upper body", "alias": "pa47_trench", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, hanbok, traditional, palace, elegant, upper body", "alias": "pa48_hanbok", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, pilot jacket, aviator goggles, sky, confident, upper body", "alias": "pa49_pilot", "style": "pale_aqua"},
    {"prompt": f"{CHAR}, shrine maiden, hakama, shrine, serene, face close-up", "alias": "pa50_miko", "style": "pale_aqua"},

    # === shinkai (5장) ===
    {"prompt": f"{CHAR}, umbrella, rain, crossing, neon reflections, night, upper body", "alias": "sk01_rain", "style": "shinkai"},
    {"prompt": f"{CHAR}, bridge, river, cherry blossoms, spring, upper body", "alias": "sk02_bridge", "style": "shinkai"},
    {"prompt": f"{CHAR}, bus stop, rural, summer, cicadas, face close-up", "alias": "sk03_bus", "style": "shinkai"},
    {"prompt": f"{CHAR}, tower, city panorama, twilight, wind, upper body", "alias": "sk04_tower", "style": "shinkai"},
    {"prompt": f"{CHAR}, field, sunflowers, summer, bright, face close-up", "alias": "sk05_sun", "style": "shinkai"},

    # === mono_halftone (5장) ===
    {"prompt": f"{CHAR}, suit, noir, dramatic shadow, upper body", "alias": "mh01_noir", "style": "mono_halftone"},
    {"prompt": f"{CHAR}, school uniform, wind, hair blowing, sharp, face close-up", "alias": "mh02_wind", "style": "mono_halftone"},
    {"prompt": f"{CHAR}, motorcycle, night, city, cool, upper body", "alias": "mh03_bike", "style": "mono_halftone"},
    {"prompt": f"{CHAR}, katana, stance, intense, face close-up", "alias": "mh04_katana", "style": "mono_halftone"},
    {"prompt": f"{CHAR}, cigarette, rooftop, night, lonely, face close-up", "alias": "mh05_smoke", "style": "mono_halftone"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
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
            print(f"[{idx:03d}/{TOTAL}] OK {job['alias']} [{job['style']}] (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:03d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:03d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print(f"냥냥돌쇠 D버전 100장 배치", flush=True)
    print(f"캐릭: 남색보브컷 호박안 쿨뷰티", flush=True)
    print(f"점: 눈밑+목 (facial mole, multiple moles, mole under eye, mole on neck)", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)
    print(f"프리셋: pale_aqua(50) watercolor_sketch(10) monogatari(10) pop_fanart(10) cozy_gouache(5) kyoto_animation(5) shinkai(5) mono_halftone(5)", flush=True)
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
