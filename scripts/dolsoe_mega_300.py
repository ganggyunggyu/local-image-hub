"""냥냥돌쇠 메가 배치 300장 - 바니걸 + 일상 + 계절 + 감정"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_mega_300"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DOLSOE = "cat ears, cat tail, dark blue hair, bob cut, amber eyes"

# 이쁜 프리셋 모음
PRETTY_PRESETS = [
    "pale_aqua", "monogatari", "kyoto_animation", "pastel_soft",
    "waterful", "blue_archive", "pop_fanart", "watercolor_sketch",
    "cozy_gouache", "ghibli", "shinkai", "sepia_backlit",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers"

JOBS = []

# === 1. 바니걸 100장 ===
BUNNY_BASE = "bunny girl, playboy bunny, leotard, bow tie, rabbit ears, wrist cuffs, fishnet pantyhose"
BUNNY_POSES = [
    "standing, looking at viewer, confident smile, hand on hip, upper body",
    "sitting on bar stool, crossed legs, seductive, upper body",
    "winking, peace sign, playful, cheerful, upper body",
    "serving drinks on tray, professional, smiling, upper body",
    "leaning forward, flirty, teasing, upper body",
    "back view, looking over shoulder, elegant, upper body",
    "kneeling, bunny pose, hands up, cute, full body",
    "jumping, energetic, cheerful, full body",
    "shy, blushing, embarrassed, upper body",
    "confident, smirking, cool, upper body",
    "sitting on floor, legs to side, relaxed, full body",
    "stretching, arms up, yawning, upper body",
    "hand on chin, thinking pose, upper body",
    "adjusting bunny ears, cute, upper body",
    "holding champagne glass, elegant, upper body",
    "blowing kiss, flirty, romantic, upper body",
    "laughing, hands covering mouth, joyful, upper body",
    "serious expression, intense gaze, upper body",
    "surprised, eyes wide, cute, upper body",
    "sleepy, tired, lazy, upper body",
]

for i in range(100):
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    pose = BUNNY_POSES[i % len(BUNNY_POSES)]
    JOBS.append({
        "prompt": f"1girl, {DOLSOE}, {BUNNY_BASE}, {pose}",
        "style": preset,
        "name": f"dolsoe_bunny_{i+1:03d}_{preset}",
        "category": "bunny",
    })

# === 2. 일상 상황 100장 ===
DAILY_SCENES = [
    # 카페/음식
    "cafe, sitting at table, drinking coffee, relaxed, warm lighting, upper body",
    "cafe, reading book, peaceful, cozy atmosphere, upper body",
    "bakery, looking at cakes, excited, sweet shop, upper body",
    "restaurant, eating meal, happy, delicious food, upper body",
    "kitchen, cooking, apron, focused, home, upper body",
    "tea time, holding teacup, elegant, afternoon, upper body",

    # 학교/도서관
    "classroom, sitting at desk, studying, focused, daytime, upper body",
    "library, reading book, quiet, peaceful, surrounded by books, upper body",
    "school hallway, walking, casual, after school, full body",
    "rooftop, sitting, looking at sky, peaceful, wind, upper body",
    "school uniform, standing, gentle smile, campus, upper body",

    # 도시/거리
    "city street, walking, shopping bags, happy, daytime, full body",
    "night city, neon lights, colorful, vibrant, urban, upper body",
    "park, sitting on bench, relaxed, nature, daytime, full body",
    "bookstore, browsing books, interested, intellectual, upper body",
    "convenience store, shopping, casual, night, upper body",

    # 집/방
    "bedroom, lying on bed, relaxed, cozy, pillows, full body",
    "living room, sitting on sofa, watching tv, casual, upper body",
    "desk, using computer, working, focused, night, upper body",
    "window, looking outside, thoughtful, rain, upper body",
    "balcony, evening, city view, peaceful, upper body",

    # 여가
    "listening to music, headphones, enjoying, eyes closed, upper body",
    "playing games, controller, focused, excited, upper body",
    "drawing, sketch pad, artistic, creative, upper body",
    "singing, microphone, performance, stage, upper body",
    "dancing, dynamic pose, energetic, full body",
]

for i in range(100):
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = DAILY_SCENES[i % len(DAILY_SCENES)]
    JOBS.append({
        "prompt": f"1girl, {DOLSOE}, {scene}",
        "style": preset,
        "name": f"dolsoe_daily_{i+1:03d}_{preset}",
        "category": "daily",
    })

# === 3. 계절 테마 50장 ===
SEASON_SCENES = [
    # 봄 (12장)
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

    # 여름 (13장)
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

    # 가을 (12장)
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

    # 겨울 (13장)
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

for i in range(50):
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = SEASON_SCENES[i % len(SEASON_SCENES)]
    JOBS.append({
        "prompt": f"1girl, {DOLSOE}, {scene}",
        "style": preset,
        "name": f"dolsoe_season_{i+1:02d}_{preset}",
        "category": "season",
    })

# === 4. 감정 표현 50장 ===
EMOTION_POSES = [
    # 기쁨/행복 (10장)
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

    # 수줍음/부끄러움 (10장)
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

    # 졸림/피곤 (5장)
    "sleepy, yawning, tired, drowsy, upper body",
    "exhausted, half-closed eyes, tired, weary, upper body",
    "lazy, stretching, relaxed, comfortable, upper body",
    "dozing off, nodding, sleepy, cute, upper body",
    "tired, rubbing eyes, sleepy, drowsy, upper body",

    # 놀람/당황 (5장)
    "surprised, eyes wide, shock, amazed, upper body",
    "startled, jumped, frightened, scared, upper body",
    "confused, question marks, puzzled, tilting head, upper body",
    "shocked, mouth open, disbelief, stunned, upper body",
    "bewildered, lost, confused, uncertain, upper body",

    # 장난기/악동 (5장)
    "mischievous, plotting, scheming smile, playful, upper body",
    "teasing, sticking tongue out, playful, cheeky, upper body",
    "smug, smirking, confident, superior, upper body",
    "playful, winking, fun, cheerful, upper body",
    "prankster, evil grin, mischievous, planning, upper body",

    # 기타 감정 (15장)
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

for i in range(50):
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    emotion = EMOTION_POSES[i % len(EMOTION_POSES)]
    JOBS.append({
        "prompt": f"1girl, {DOLSOE}, {emotion}",
        "style": preset,
        "name": f"dolsoe_emotion_{i+1:02d}_{preset}",
        "category": "emotion",
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
    print(f"🐱💙 냥냥돌쇠 메가 배치 {TOTAL}장! 🐱💙", flush=True)
    print(f"바니걸 100 + 일상 100 + 계절 50 + 감정 50", flush=True)
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
