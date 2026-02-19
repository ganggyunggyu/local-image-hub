"""모노가타리 서브 캐릭터 10명 메가 배치 500장"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_sub_500"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 모노가타리 서브 캐릭터 10명
CHARACTERS = [
    ("shinobu", "oshino shinobu, monogatari, blonde hair, golden eyes, vampire, loli, fang, cute"),
    ("nadeko", "sengoku nadeko, monogatari, orange hair, long hair, bangs, shy, cute, gentle"),
    ("kanbaru", "kanbaru suruga, monogatari, short dark hair, athletic, tomboy, energetic, sporty"),
    ("hachikuji", "hachikuji mayoi, monogatari, twin tails, backpack, ghost girl, cute, cheerful"),
    ("karen", "araragi karen, monogatari, long black hair, ponytail, tall, martial arts, energetic"),
    ("tsukihi", "araragi tsukihi, monogatari, short black hair, kimono style, cute, phoenix, elegant"),
    ("sodachi", "oikura sodachi, monogatari, light brown hair, twin tails, sharp eyes, angry, intense"),
    ("ougi", "oshino ougi, monogatari, short black hair, mysterious, dark, enigmatic, creepy"),
    ("gaen", "gaen izuko, monogatari, short hair, confident, mature, expert, professional"),
    ("yotsugi", "ononoki yotsugi, monogatari, green hair, hat, expressionless, doll, emotionless"),
]

# 이쁜 프리셋 모음
PRETTY_PRESETS = [
    "pale_aqua", "monogatari", "kyoto_animation", "pastel_soft",
    "waterful", "blue_archive", "pop_fanart", "watercolor_sketch",
    "cozy_gouache", "ghibli", "shinkai", "sepia_backlit",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers"

JOBS = []

# === 1. 일상 상황 125장 ===
DAILY_SCENES = [
    # 학교/교실
    "classroom, sitting at desk, studying, focused, window light, upper body",
    "library, reading book, quiet, peaceful, surrounded by books, upper body",
    "school hallway, walking, after school, gentle smile, full body",
    "rooftop, sitting, looking at sky, wind, peaceful, upper body",
    "school uniform, standing, blackboard, upper body",
    "cafeteria, eating lunch, relaxed, casual, upper body",
    "school gate, leaving, sunset, nostalgic, upper body",
    "gym, exercising, athletic, energetic, full body",
    "school yard, walking, trees, nature, full body",
    "school stairs, sitting, thinking, alone, upper body",

    # 집/방
    "bedroom, lying on bed, reading, relaxed, cozy, full body",
    "desk, studying late night, tired, focused, upper body",
    "window, looking outside, thoughtful, rain, upper body",
    "living room, sitting on sofa, relaxed, home, upper body",
    "kitchen, making tea, gentle, domestic, upper body",
    "balcony, evening, city view, peaceful, upper body",
    "mirror, fixing hair, preparing, morning routine, upper body",
    "bed, waking up, sleepy, morning light, upper body",

    # 도시/거리
    "city street, walking, shopping bags, casual clothes, full body",
    "bookstore, browsing books, interested, intellectual, upper body",
    "cafe, sitting, drinking coffee, relaxed, warm lighting, upper body",
    "park, sitting on bench, reading, peaceful, nature, full body",
    "night city, neon lights, mysterious, urban, upper body",
    "convenience store, shopping, casual, night, upper body",
    "bus stop, waiting, evening, peaceful, upper body",
    "crosswalk, walking, city life, full body",

    # 특별한 장소
    "shrine, traditional, peaceful, spiritual, upper body",
    "temple, quiet, serene, contemplative, upper body",
    "bridge, river, scenic, peaceful, upper body",
    "garden, flowers, nature, peaceful, upper body",
    "museum, art, cultured, interested, upper body",
]

for i in range(125):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = DAILY_SCENES[i % len(DAILY_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {scene}",
        "style": preset,
        "name": f"mono_sub_daily_{i+1:03d}_{alias}_{preset}",
        "category": "daily",
    })

# === 2. 계절 테마 125장 ===
SEASON_SCENES = [
    # 봄
    "spring, cherry blossoms, pink petals falling, gentle smile, upper body",
    "spring, flower field, colorful flowers, happy, full body",
    "spring, park, cherry blossom tree, peaceful, sitting, full body",
    "spring, rain, umbrella, gentle, soft lighting, upper body",
    "spring, picnic, blanket, food, relaxed, full body",
    "spring, butterfly, reaching out, curious, upper body",
    "spring, bike, riding, wind, cheerful, full body",
    "spring, garden, watering flowers, gentle, upper body",
    "spring, festival, yukata, fireworks, excited, upper body",
    "spring, fresh green, nature, peaceful, upper body",
    "spring, morning, dew, fresh, gentle light, upper body",
    "spring, bridge, river, sakura, wind, upper body",

    # 여름
    "summer, beach, swimsuit, ocean, cheerful, full body",
    "summer, watermelon, eating, happy, refreshing, upper body",
    "summer, sunflower field, bright, sunny, full body",
    "summer, pool, water, splash, playful, full body",
    "summer, festival, yukata, goldfish, night, upper body",
    "summer, ice cream, eating, happy, sweet, upper body",
    "summer, fireworks, night sky, colorful, awe, upper body",
    "summer, hot, fan, tired, sweating, upper body",
    "summer, tropical, palm trees, vacation, relaxed, upper body",
    "summer, shaved ice, dessert, refreshing, upper body",
    "summer, seaside, sunset, peaceful, upper body",
    "summer, cicada, catching, playful, full body",
    "summer, straw hat, sunny day, field, upper body",

    # 가을
    "autumn, maple leaves, orange red, falling leaves, upper body",
    "autumn, park, reading, peaceful, warm colors, upper body",
    "autumn, sweater, cozy, warm drink, upper body",
    "autumn, harvest, fruits, basket, happy, upper body",
    "autumn, forest, hiking, nature, full body",
    "autumn, rain, umbrella, melancholic, upper body",
    "autumn, cafe, window, rainy day, cozy, upper body",
    "autumn, library, books, studying, warm lighting, upper body",
    "autumn, evening, sunset, golden hour, peaceful, upper body",
    "autumn, chestnut, eating, enjoying, upper body",
    "autumn, scarf, wind, leaves, walking, full body",
    "autumn, moon viewing, night, peaceful, upper body",

    # 겨울
    "winter, snow, snowing, cold, scarf, upper body",
    "winter, snowman, building, playful, happy, full body",
    "winter, hot chocolate, warm, cozy, indoors, upper body",
    "winter, kotatsu, warm, relaxed, comfortable, upper body",
    "winter, christmas, tree, lights, happy, upper body",
    "winter, ice skating, rink, fun, full body",
    "winter, coat, walking, city, night, full body",
    "winter, fireplace, warm, cozy, peaceful, upper body",
    "winter, ski resort, snow, mountain, full body",
    "winter, frozen lake, ice, cold, beautiful, upper body",
    "winter, white breath, cold, scarf, cute, upper body",
    "winter, snow angel, playing, happy, full body",
    "winter, new year, shrine, traditional, upper body",
]

for i in range(125):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = SEASON_SCENES[i % len(SEASON_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {scene}",
        "style": preset,
        "name": f"mono_sub_season_{i+1:03d}_{alias}_{preset}",
        "category": "season",
    })

# === 3. 감정 표현 125장 ===
EMOTION_POSES = [
    # 기쁨/행복
    "laughing, bright smile, sparkling eyes, joyful, happy, upper body",
    "giggling, covering mouth, cute, cheerful, upper body",
    "excited, arms up, energetic, thrilled, upper body",
    "satisfied, content smile, peaceful, happy, upper body",
    "playful, winking, tongue out, mischievous, upper body",
    "proud, chest out, confident smile, accomplished, upper body",
    "relief, relaxed smile, peaceful, calm, upper body",
    "cheerful, peace sign, bright, energetic, upper body",
    "delighted, sparkles, eyes shining, amazed, upper body",
    "amused, smirking, entertained, playful, upper body",

    # 수줍음/부끄러움
    "shy, blushing, looking away, embarrassed, upper body",
    "nervous, fidgeting hands, anxious, timid, upper body",
    "flustered, red face, panicked, embarrassed, upper body",
    "bashful, hiding face, cute, shy, upper body",
    "timid, looking down, nervous, quiet, upper body",
    "embarrassed, puffed cheeks, flustered, cute, upper body",
    "modest, gentle smile, demure, elegant, upper body",
    "hesitant, uncertain, nervous, careful, upper body",
    "self-conscious, touching hair, shy, cute, upper body",
    "blushing, covering face with hands, embarrassed, upper body",

    # 졸림/피곤
    "sleepy, yawning, tired, drowsy, upper body",
    "exhausted, half-closed eyes, tired, weary, upper body",
    "lazy, stretching, relaxed, comfortable, upper body",
    "dozing off, nodding, sleepy, cute, upper body",
    "tired, rubbing eyes, sleepy, drowsy, upper body",

    # 놀람/당황
    "surprised, eyes wide, shock, amazed, upper body",
    "startled, jumped, frightened, scared, upper body",
    "confused, question marks, puzzled, tilting head, upper body",
    "shocked, mouth open, disbelief, stunned, upper body",
    "bewildered, lost, confused, uncertain, upper body",

    # 장난기/악동
    "mischievous, plotting, scheming smile, playful, upper body",
    "teasing, sticking tongue out, playful, cheeky, upper body",
    "smug, smirking, confident, superior, upper body",
    "playful, winking, fun, cheerful, upper body",
    "prankster, evil grin, mischievous, planning, upper body",

    # 기타 감정
    "thinking, hand on chin, pondering, curious, upper body",
    "determined, serious, focused, intense, upper body",
    "melancholic, sad, thoughtful, emotional, upper body",
    "lonely, looking down, sad, isolated, upper body",
    "angry, puffed cheeks, frustrated, annoyed, upper body",
    "pouting, sulking, upset, cute, upper body",
    "worried, anxious, concerned, nervous, upper body",
    "scared, frightened, trembling, afraid, upper body",
    "curious, interested, wondering, questioning, upper body",
    "gentle, warm smile, kind, caring, upper body",
    "cool, composed, calm, collected, upper body",
    "dreamy, daydreaming, peaceful, imagining, upper body",
    "nostalgic, remembering, thoughtful, emotional, upper body",
    "hopeful, looking up, optimistic, bright, upper body",
    "content, peaceful, satisfied, happy, upper body",
]

for i in range(125):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    emotion = EMOTION_POSES[i % len(EMOTION_POSES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {emotion}",
        "style": preset,
        "name": f"mono_sub_emotion_{i+1:03d}_{alias}_{preset}",
        "category": "emotion",
    })

# === 4. 특별한 순간 125장 ===
SPECIAL_SCENES = [
    "sunset, golden hour, wind, hair flowing, emotional, upper body",
    "rain, umbrella, wet, melancholic, upper body",
    "night, moonlight, mysterious, beautiful, upper body",
    "cherry blossoms, spring, petals falling, peaceful, upper body",
    "snow, winter, cold, scarf, gentle, upper body",
    "starry sky, looking up, dreamy, night, upper body",
    "sunrise, morning, hopeful, new beginning, upper body",
    "autumn leaves, falling, nostalgic, warm colors, upper body",
    "dramatic lighting, cinematic, intense, emotional, upper body",
    "soft lighting, gentle, peaceful, serene, upper body",
    "backlight, silhouette, dramatic, mysterious, upper body",
    "spotlight, stage, performance, confident, upper body",
    "candlelight, warm, intimate, gentle, upper body",
    "neon lights, colorful, urban, modern, upper body",
    "natural light, window, peaceful, gentle, upper body",
    "magic hour, dreamy, beautiful, enchanting, upper body",
    "misty, foggy, mysterious, atmospheric, upper body",
    "reflections, water, mirror, beautiful, upper body",
    "floating, dreamy, ethereal, magical, full body",
    "wind, hair flowing, dynamic, beautiful, upper body",
    "flower petals, falling, beautiful, romantic, upper body",
    "bubbles, soap bubbles, playful, dreamy, upper body",
    "sparkles, glitter, magical, beautiful, upper body",
    "lens flare, bright, hopeful, optimistic, upper body",
    "bokeh, blurred background, focused, beautiful, upper body",
]

for i in range(125):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = SPECIAL_SCENES[i % len(SPECIAL_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {scene}",
        "style": preset,
        "name": f"mono_sub_special_{i+1:03d}_{alias}_{preset}",
        "category": "special",
    })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, idx: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece, best quality",
        "negative_prompt": NEGATIVE,
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=240.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:03d}/{TOTAL}] OK {job['name']} ({job['category']})", flush=True)
            return True
        print(f"[{idx:03d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:50]}", flush=True)
        return False
    except Exception as e:
        print(f"[{idx:03d}/{TOTAL}] ERROR {job['name']}: {e}", flush=True)
        return False


async def main() -> None:
    ok = fail = 0
    print(f"🌟 모노가타리 서브 캐릭터 10명 메가 배치 {TOTAL}장! 🌟", flush=True)
    print(f"일상 125 + 계절 125 + 감정 125 + 특별한 순간 125", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)
    print("=" * 70, flush=True)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 70, flush=True)
    print(f"🎉 완료! 성공: {ok}, 실패: {fail} 🎉", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
