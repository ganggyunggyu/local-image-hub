"""케이온 5인 메가 배치 500장 - 일상 + 계절 + 감정 + 음악"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_keion_mega_500"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 케이온 5인
CHARACTERS = [
    ("yui", "hirasawa yui, k-on, brown hair, twin tails, red hairband, cheerful, energetic, guitarist"),
    ("mio", "akiyama mio, k-on, long black hair, straight hair, shy, serious, bassist, blue eyes"),
    ("ritsu", "tainaka ritsu, k-on, short brown hair, yellow hairband, energetic, tomboy, drummer"),
    ("mugi", "kotobuki tsumugi, k-on, blonde hair, long hair, gentle, elegant, pianist, blue eyes"),
    ("azusa", "nakano azusa, k-on, black twin tails, cat ears headband, serious, cute, guitarist, small"),
]

# 이쁜 프리셋 모음
PRETTY_PRESETS = [
    "pale_aqua", "monogatari", "kyoto_animation", "pastel_soft",
    "waterful", "blue_archive", "pop_fanart", "watercolor_sketch",
    "cozy_gouache", "ghibli", "shinkai", "sepia_backlit",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers"

JOBS = []

# === 1. 일상 상황 150장 ===
DAILY_SCENES = [
    # 학교/교실 (12)
    "classroom, sitting at desk, studying, focused, daytime, window light, upper body",
    "classroom, standing, blackboard, teaching, explaining, upper body",
    "classroom, talking with friends, happy, cheerful, group, upper body",
    "classroom, cleaning duty, bucket, mop, casual, full body",
    "school hallway, walking, after school, bag, peaceful, full body",
    "school hallway, running, hurry, late, energetic, full body",
    "school entrance, arriving, morning, greeting, upper body",
    "school rooftop, eating lunch, bento, relaxed, upper body",
    "school rooftop, looking at sky, peaceful, wind, upper body",
    "school stairs, sitting, thinking, alone, upper body",
    "school library, reading, quiet, peaceful, upper body",
    "school yard, walking, trees, nature, full body",

    # 방과후 티타임 (10)
    "music room, tea time, sitting, drinking tea, relaxed, happy, upper body",
    "music room, eating cake, happy, enjoying, sweet, upper body",
    "music room, chatting, laughing, friends, cheerful, upper body",
    "music room, window, afternoon light, peaceful, sitting, upper body",
    "music room, preparing tea, gentle, caring, upper body",
    "music room, reading magazine, relaxed, casual, upper body",
    "music room, lying on sofa, lazy, comfortable, full body",
    "music room, looking outside, thoughtful, peaceful, upper body",
    "music room, serving cake, waitress pose, cute, upper body",
    "music room, group photo pose, happy, together, upper body",

    # 부실/연습 (10)
    "music room, tuning instrument, focused, preparing, upper body",
    "music room, sheet music, studying, learning, upper body",
    "music room, standing, microphone, singing practice, upper body",
    "music room, sitting, resting, break time, tired, upper body",
    "music room, equipment, organizing, responsible, upper body",
    "music room, recording, headphones, focused, upper body",
    "music room, discussing, planning, meeting, upper body",
    "music room, cleaning, tidy, organized, full body",
    "music room, looking at poster, planning, event, upper body",
    "music room, writing lyrics, creative, thinking, upper body",

    # 집/방 (8)
    "bedroom, lying on bed, relaxed, cozy, pillows, full body",
    "bedroom, studying at desk, night, lamp, focused, upper body",
    "bedroom, window, looking outside, thoughtful, upper body",
    "living room, watching tv, casual, relaxed, upper body",
    "kitchen, cooking, apron, focused, home, upper body",
    "bathroom, brushing teeth, morning routine, casual, upper body",
    "bed, waking up, sleepy, morning, stretching, upper body",
    "room, listening to music, headphones, enjoying, upper body",

    # 카페/거리 (10)
    "cafe, sitting, drinking coffee, relaxed, warm lighting, upper body",
    "cafe, reading book, peaceful, cozy, upper body",
    "cafe, eating dessert, happy, sweet, upper body",
    "city street, walking, shopping bags, casual clothes, full body",
    "park, sitting on bench, peaceful, nature, full body",
    "convenience store, shopping, casual, night, upper body",
    "bookstore, browsing, interested, curious, upper body",
    "street, window shopping, looking at display, upper body",
    "crosswalk, waiting, city life, casual, upper body",
    "bus stop, waiting, evening, peaceful, upper body",
]

for i in range(150):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = DAILY_SCENES[i % len(DAILY_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {scene}",
        "style": preset,
        "name": f"keion_daily_{i+1:03d}_{alias}_{preset}",
        "category": "daily",
    })

# === 2. 계절 테마 125장 ===
SEASON_SCENES = [
    # 봄 (13)
    "spring, cherry blossoms, pink petals falling, gentle smile, school uniform, upper body",
    "spring, cherry blossom tree, sitting under tree, peaceful, full body",
    "spring, flower field, colorful flowers, happy, cheerful, full body",
    "spring, park, walking, fresh green, nature, full body",
    "spring, rain, umbrella, gentle, soft lighting, upper body",
    "spring, picnic, blanket, food, friends, relaxed, full body",
    "spring, butterfly, reaching out, curious, gentle, upper body",
    "spring, bike, riding, wind, cheerful, full body",
    "spring, garden, watering flowers, caring, gentle, upper body",
    "spring, entrance ceremony, formal, excited, upper body",
    "spring, new semester, books, bag, hopeful, upper body",
    "spring, bridge, river, sakura, wind, peaceful, upper body",
    "spring, morning, fresh, bright, energetic, upper body",

    # 여름 (13)
    "summer, beach, swimsuit, ocean, cheerful, happy, full body",
    "summer, watermelon, eating, refreshing, happy, upper body",
    "summer, sunflower field, bright, sunny, cheerful, full body",
    "summer, pool, water, splash, playful, fun, full body",
    "summer, festival, yukata, fireworks, night, excited, upper body",
    "summer, ice cream, eating, happy, sweet, cold, upper body",
    "summer, fireworks, night sky, colorful, amazed, upper body",
    "summer, fan, hot, tired, sweating, casual, upper body",
    "summer, shaved ice, dessert, refreshing, happy, upper body",
    "summer, seaside, sunset, peaceful, emotional, upper body",
    "summer, straw hat, sunny day, beach, cheerful, upper body",
    "summer, cicada, catching, playful, energetic, full body",
    "summer, camp, outdoor, nature, happy, full body",

    # 가을 (13)
    "autumn, maple leaves, orange red, falling leaves, nostalgic, upper body",
    "autumn, park, reading, peaceful, warm colors, upper body",
    "autumn, sweater, cozy, warm, comfortable, upper body",
    "autumn, harvest, fruits, basket, happy, cheerful, upper body",
    "autumn, forest, hiking, nature, enjoying, full body",
    "autumn, rain, umbrella, melancholic, thoughtful, upper body",
    "autumn, cafe, window, rainy day, cozy, warm, upper body",
    "autumn, library, books, studying, warm lighting, upper body",
    "autumn, evening, sunset, golden hour, peaceful, upper body",
    "autumn, cultural festival, excited, preparing, busy, upper body",
    "autumn, scarf, wind, leaves, walking, full body",
    "autumn, moon viewing, night, peaceful, traditional, upper body",
    "autumn, school festival, stage, performance, excited, upper body",

    # 겨울 (11)
    "winter, snow, snowing, cold, scarf, coat, upper body",
    "winter, snowman, building, playful, happy, cheerful, full body",
    "winter, hot chocolate, warm, cozy, indoors, upper body",
    "winter, kotatsu, warm, relaxed, comfortable, sleepy, upper body",
    "winter, christmas, tree, lights, happy, festive, upper body",
    "winter, ice skating, rink, fun, playful, full body",
    "winter, coat, walking, city, night, cold, full body",
    "winter, fireplace, warm, cozy, peaceful, reading, upper body",
    "winter, white breath, cold, scarf, cute, shivering, upper body",
    "winter, snow angel, playing, happy, cheerful, full body",
    "winter, new year, shrine, traditional, formal, upper body",
]

for i in range(125):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = SEASON_SCENES[i % len(SEASON_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {scene}",
        "style": preset,
        "name": f"keion_season_{i+1:03d}_{alias}_{preset}",
        "category": "season",
    })

# === 3. 감정 표현 125장 ===
EMOTION_POSES = [
    # 기쁨/행복 (15)
    "laughing, bright smile, sparkling eyes, joyful, happy, cheerful, upper body",
    "giggling, covering mouth, cute, cheerful, amused, upper body",
    "excited, arms up, energetic, thrilled, happy, upper body",
    "satisfied, content smile, peaceful, happy, relaxed, upper body",
    "playful, winking, tongue out, mischievous, fun, upper body",
    "proud, chest out, confident smile, accomplished, happy, upper body",
    "relief, relaxed smile, peaceful, calm, grateful, upper body",
    "cheerful, peace sign, bright, energetic, happy, upper body",
    "delighted, sparkles, eyes shining, amazed, happy, upper body",
    "amused, smirking, entertained, playful, fun, upper body",
    "joyful, jumping, energetic, excited, dynamic, full body",
    "happy tears, emotional, moved, touched, crying, upper body",
    "triumphant, victory pose, winning, successful, upper body",
    "ecstatic, very happy, overjoyed, thrilled, upper body",
    "warm smile, gentle, kind, caring, loving, upper body",

    # 수줍음/부끄러움 (12)
    "shy, blushing, looking away, embarrassed, timid, upper body",
    "nervous, fidgeting hands, anxious, timid, worried, upper body",
    "flustered, red face, panicked, embarrassed, cute, upper body",
    "bashful, hiding face, cute, shy, covering, upper body",
    "timid, looking down, nervous, quiet, reserved, upper body",
    "embarrassed, puffed cheeks, flustered, cute, tsundere, upper body",
    "modest, gentle smile, demure, elegant, graceful, upper body",
    "hesitant, uncertain, nervous, careful, cautious, upper body",
    "self-conscious, touching hair, shy, cute, nervous, upper body",
    "blushing, covering face with hands, embarrassed, hiding, upper body",
    "stammering, confused, flustered, nervous, cute, upper body",
    "avoiding eye contact, shy, nervous, looking away, upper body",

    # 졸림/피곤 (8)
    "sleepy, yawning, tired, drowsy, exhausted, upper body",
    "exhausted, half-closed eyes, tired, weary, worn out, upper body",
    "lazy, stretching, relaxed, comfortable, sleepy, upper body",
    "dozing off, nodding, sleepy, cute, tired, upper body",
    "tired, rubbing eyes, sleepy, drowsy, exhausted, upper body",
    "falling asleep, very sleepy, exhausted, peaceful, upper body",
    "sleepy eyes, drowsy, tired, relaxed, calm, upper body",
    "waking up, stretching, morning, sleepy, refreshed, upper body",

    # 놀람/당황 (10)
    "surprised, eyes wide, shock, amazed, astonished, upper body",
    "startled, jumped, frightened, scared, shocked, upper body",
    "confused, question marks, puzzled, tilting head, wondering, upper body",
    "shocked, mouth open, disbelief, stunned, speechless, upper body",
    "bewildered, lost, confused, uncertain, puzzled, upper body",
    "panicked, worried, anxious, nervous, scared, upper body",
    "amazed, impressed, awed, wonderful, fascinated, upper body",
    "speechless, shocked, stunned, surprised, upper body",
    "wide-eyed, surprised, curious, interested, upper body",
    "taken aback, surprised, unexpected, shocked, upper body",

    # 장난기/활발 (10)
    "mischievous, plotting, scheming smile, playful, fun, upper body",
    "teasing, sticking tongue out, playful, cheeky, cute, upper body",
    "smug, smirking, confident, superior, proud, upper body",
    "playful, winking, fun, cheerful, flirty, upper body",
    "prankster, evil grin, mischievous, planning, scheming, upper body",
    "energetic, dynamic, lively, active, moving, full body",
    "competitive, determined, fired up, motivated, upper body",
    "cheeky, smirking, teasing, playful, mischievous, upper body",
    "silly, funny face, goofy, amusing, entertaining, upper body",
    "rebellious, cool, confident, defiant, strong, upper body",

    # 집중/진지 (8)
    "thinking, hand on chin, pondering, curious, thoughtful, upper body",
    "determined, serious, focused, intense, strong-willed, upper body",
    "concentrated, focused, serious, working hard, studying, upper body",
    "observing, watching, careful, attentive, focused, upper body",
    "analyzing, thinking deeply, intellectual, smart, upper body",
    "planning, strategic, thoughtful, careful, upper body",
    "reading, focused, absorbed, quiet, peaceful, upper body",
    "listening, attentive, focused, careful, interested, upper body",

    # 기타 감정 (12)
    "melancholic, sad, thoughtful, emotional, lonely, upper body",
    "lonely, looking down, sad, isolated, alone, upper body",
    "angry, puffed cheeks, frustrated, annoyed, upset, upper body",
    "pouting, sulking, upset, cute, grumpy, upper body",
    "worried, anxious, concerned, nervous, troubled, upper body",
    "scared, frightened, trembling, afraid, fearful, upper body",
    "curious, interested, wondering, questioning, intrigued, upper body",
    "gentle, warm smile, kind, caring, loving, upper body",
    "cool, composed, calm, collected, confident, upper body",
    "dreamy, daydreaming, peaceful, imagining, thoughtful, upper body",
    "nostalgic, remembering, thoughtful, emotional, reminiscing, upper body",
    "hopeful, looking up, optimistic, bright, positive, upper body",
]

for i in range(125):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    emotion = EMOTION_POSES[i % len(EMOTION_POSES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {emotion}",
        "style": preset,
        "name": f"keion_emotion_{i+1:03d}_{alias}_{preset}",
        "category": "emotion",
    })

# === 4. 음악/악기 100장 ===
MUSIC_SCENES = [
    # 연주 (20)
    "playing guitar, focused, passionate, performance, upper body",
    "playing bass, concentrated, serious, cool, upper body",
    "playing drums, energetic, dynamic, powerful, upper body",
    "playing keyboard, elegant, gentle, graceful, upper body",
    "holding instrument, proud, confident, musician, upper body",
    "tuning instrument, careful, focused, preparing, upper body",
    "practicing, focused, serious, dedicated, upper body",
    "jamming, energetic, happy, enjoying music, upper body",
    "solo performance, spotlight, confident, cool, upper body",
    "playing passionately, emotional, intense, moved, upper body",
    "checking instrument, careful, responsible, upper body",
    "adjusting equipment, focused, technical, upper body",
    "warming up, preparing, stretching fingers, upper body",
    "playing gently, soft, peaceful, melodic, upper body",
    "playing powerfully, energetic, strong, dynamic, upper body",
    "playing happily, smiling, enjoying, cheerful, upper body",
    "playing seriously, focused, concentrated, intense, upper body",
    "playing with eyes closed, absorbed, emotional, peaceful, upper body",
    "playing together, band, teamwork, harmony, upper body",
    "playing on stage, performance, lights, exciting, upper body",

    # 노래/보컬 (10)
    "singing, microphone, passionate, emotional, upper body",
    "singing happily, cheerful, energetic, joyful, upper body",
    "singing gently, soft, peaceful, melodic, upper body",
    "singing powerfully, strong, confident, dynamic, upper body",
    "vocal practice, focused, serious, training, upper body",
    "humming, casual, relaxed, gentle, upper body",
    "singing with eyes closed, emotional, moved, peaceful, upper body",
    "backup vocals, supporting, harmonizing, teamwork, upper body",
    "recording vocals, headphones, focused, studio, upper body",
    "singing on stage, performance, spotlight, confident, upper body",

    # 라이브/공연 (10)
    "live performance, stage, lights, exciting, energetic, upper body",
    "concert, audience, performing, passionate, upper body",
    "stage lights, colorful, exciting, dynamic, performance, upper body",
    "school festival performance, stage, excited, nervous, upper body",
    "band performance, together, teamwork, harmony, upper body",
    "finale, ending, triumphant, successful, happy, upper body",
    "encore, excited, happy, grateful, performing, upper body",
    "soundcheck, preparing, focused, professional, upper body",
    "backstage, nervous, excited, preparing, upper body",
    "after performance, happy, exhausted, satisfied, upper body",
]

for i in range(100):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = MUSIC_SCENES[i % len(MUSIC_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {scene}",
        "style": preset,
        "name": f"keion_music_{i+1:03d}_{alias}_{preset}",
        "category": "music",
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
    print(f"🎸 케이온 5인 메가 배치 {TOTAL}장! 🎸", flush=True)
    print(f"일상 150 + 계절 125 + 감정 125 + 음악 100", flush=True)
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
