"""냥냥돌쇠 시즌2 메가 배치 300장 - 특수 의상 + 시간대 + 추가 일상"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_season2_300"
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

# === 1. 특수 의상 150장 ===
OUTFIT_SCENES = [
    # 메이드 (15)
    "maid outfit, maid dress, apron, frills, serving, professional, smiling, upper body",
    "maid outfit, curtsy, elegant, formal, greeting, full body",
    "maid outfit, holding tray, tea, serving, gentle, upper body",
    "maid outfit, cleaning, feather duster, working, upper body",
    "maid outfit, standing, confident, professional, upper body",
    "maid outfit, sitting, tea time, relaxed, upper body",
    "maid outfit, winking, playful, cute, cheerful, upper body",
    "maid outfit, shy, blushing, embarrassed, cute, upper body",
    "maid outfit, serious, focused, professional, upper body",
    "maid outfit, happy, bright smile, cheerful, upper body",
    "maid outfit, elegant, graceful, refined, upper body",
    "maid outfit, energetic, dynamic, lively, upper body",
    "maid outfit, gentle, caring, kind, upper body",
    "maid outfit, looking at viewer, inviting, welcoming, upper body",
    "maid outfit, working, focused, dedicated, upper body",

    # 학교 교복 (15)
    "school uniform, blazer, skirt, student, classroom, upper body",
    "school uniform, standing, blackboard, studying, upper body",
    "school uniform, sitting at desk, reading, focused, upper body",
    "school uniform, running, hurry, energetic, full body",
    "school uniform, carrying books, library, intellectual, upper body",
    "school uniform, eating lunch, bento, happy, upper body",
    "school uniform, rooftop, wind, peaceful, upper body",
    "school uniform, hallway, walking, casual, full body",
    "school uniform, cleaning duty, responsible, working, upper body",
    "school uniform, sports, gym, athletic, full body",
    "school uniform, music room, relaxed, peaceful, upper body",
    "school uniform, window, looking outside, thoughtful, upper body",
    "school uniform, friends, chatting, happy, cheerful, upper body",
    "school uniform, serious, focused, studying, upper body",
    "school uniform, cheerful, peace sign, energetic, upper body",

    # 캐주얼 (15)
    "casual clothes, t-shirt, jeans, relaxed, comfortable, shopping, full body",
    "casual clothes, hoodie, comfortable, cozy, relaxed, upper body",
    "casual clothes, cardigan, soft, gentle, warm, upper body",
    "casual clothes, sweater, cozy, autumn, comfortable, upper body",
    "casual clothes, summer dress, light, breezy, cheerful, full body",
    "casual clothes, jacket, cool, stylish, confident, upper body",
    "casual clothes, tank top, casual, summer, relaxed, upper body",
    "casual clothes, shorts, sporty, energetic, summer, full body",
    "casual clothes, leggings, comfortable, active, casual, full body",
    "casual clothes, skirt, cute, fashionable, stylish, full body",
    "casual clothes, overalls, playful, cute, casual, full body",
    "casual clothes, flannel shirt, casual, comfortable, relaxed, upper body",
    "casual clothes, sundress, summer, bright, cheerful, full body",
    "casual clothes, jumpsuit, stylish, fashionable, cool, full body",
    "casual clothes, sports jacket, active, energetic, sporty, upper body",

    # 스포츠/운동복 (10)
    "sports wear, gym clothes, exercising, energetic, athletic, full body",
    "sports wear, running, jogging, active, healthy, full body",
    "sports wear, yoga, stretching, flexible, peaceful, full body",
    "sports wear, basketball, playing, energetic, dynamic, full body",
    "sports wear, tennis, racket, sporty, active, full body",
    "sports wear, swimming, pool, swimsuit, cheerful, full body",
    "sports wear, cycling, bike, active, energetic, full body",
    "sports wear, training, workout, focused, determined, upper body",
    "sports wear, stretching, warming up, preparing, full body",
    "sports wear, resting, towel, tired, relaxed, upper body",

    # 드레스/정장 (15)
    "dress, elegant dress, formal, beautiful, graceful, full body",
    "dress, party dress, festive, cheerful, happy, full body",
    "dress, evening gown, elegant, sophisticated, mature, full body",
    "dress, cocktail dress, stylish, fashionable, confident, full body",
    "dress, summer dress, light, breezy, cute, full body",
    "dress, sundress, casual, cheerful, bright, full body",
    "dress, ball gown, princess, elegant, beautiful, full body",
    "dress, lace dress, delicate, feminine, gentle, full body",
    "dress, floral dress, cute, spring, colorful, full body",
    "dress, mini dress, stylish, fashionable, confident, full body",
    "business suit, formal, professional, confident, mature, upper body",
    "business suit, office, working, serious, focused, upper body",
    "business suit, elegant, sophisticated, powerful, upper body",
    "blazer, professional, stylish, confident, cool, upper body",
    "formal wear, ceremony, elegant, graceful, formal, upper body",

    # 전통 의상 (10)
    "kimono, traditional, elegant, graceful, japanese, full body",
    "kimono, festival, yukata, summer, cheerful, full body",
    "kimono, sitting, formal, traditional, elegant, full body",
    "kimono, standing, graceful, beautiful, refined, full body",
    "kimono, cherry blossoms, spring, peaceful, beautiful, full body",
    "hanbok, traditional, korean, colorful, elegant, full body",
    "traditional dress, cultural, beautiful, elegant, graceful, full body",
    "yukata, summer festival, fireworks, night, cheerful, full body",
    "traditional outfit, formal, ceremonial, elegant, full body",
    "ethnic dress, colorful, cultural, beautiful, unique, full body",

    # 잠옷/편안한 옷 (10)
    "pajamas, sleepwear, comfortable, cozy, relaxed, upper body",
    "pajamas, cute, adorable, sleepy, peaceful, upper body",
    "nightgown, elegant, comfortable, gentle, peaceful, upper body",
    "pajamas, stretching, yawning, morning, sleepy, upper body",
    "pajamas, sitting on bed, relaxed, comfortable, cozy, upper body",
    "sleepwear, reading, peaceful, quiet, calm, upper body",
    "pajamas, drinking tea, relaxed, peaceful, cozy, upper body",
    "loungewear, comfortable, relaxed, casual, home, upper body",
    "bathrobe, after bath, relaxed, comfortable, fresh, upper body",
    "onesie, cute, adorable, comfortable, playful, full body",

    # 기타 특수 의상 (10)
    "witch costume, hat, magical, mysterious, playful, full body",
    "gothic lolita, elegant, dark, beautiful, stylish, full body",
    "idol outfit, stage, performance, cheerful, energetic, full body",
    "nurse outfit, medical, caring, professional, kind, upper body",
    "police uniform, professional, cool, confident, strong, upper body",
    "chef outfit, cooking, apron, professional, focused, upper body",
    "santa outfit, christmas, festive, cheerful, happy, full body",
    "halloween costume, playful, fun, cheerful, cute, full body",
    "cosplay, character, fun, energetic, playful, full body",
    "fantasy outfit, magical, mystical, beautiful, enchanting, full body",
]

for i in range(150):
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = OUTFIT_SCENES[i % len(OUTFIT_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {DOLSOE}, {scene}",
        "style": preset,
        "name": f"dolsoe_outfit_{i+1:03d}_{preset}",
        "category": "outfit",
    })

# === 2. 시간대별 75장 ===
TIME_SCENES = [
    # 아침 (20)
    "morning, sunrise, waking up, stretching, sleepy, bedroom, upper body",
    "morning, breakfast, eating, kitchen, cheerful, upper body",
    "morning, getting ready, mirror, preparing, focused, upper body",
    "morning, fresh, energetic, bright, hopeful, upper body",
    "morning, coffee, drinking, peaceful, relaxed, upper body",
    "morning, window, looking outside, peaceful, gentle light, upper body",
    "morning, exercise, stretching, healthy, energetic, full body",
    "morning, shower, refreshed, clean, fresh, upper body",
    "morning, reading newspaper, relaxed, peaceful, upper body",
    "morning, making bed, tidy, responsible, organized, full body",
    "morning, brushing teeth, routine, casual, bathroom, upper body",
    "morning, watering plants, caring, gentle, garden, upper body",
    "morning, jogging, running, active, healthy, full body",
    "morning, meditation, peaceful, calm, serene, upper body",
    "morning, yawning, tired, sleepy, lazy, upper body",
    "morning, breakfast cooking, apron, focused, kitchen, upper body",
    "morning, balcony, fresh air, peaceful, relaxed, upper body",
    "morning, planning day, notebook, thinking, organized, upper body",
    "morning, cheerful, energetic, ready, motivated, upper body",
    "morning, gentle smile, peaceful, calm, content, upper body",

    # 낮 (20)
    "daytime, walking, city, shopping, casual, cheerful, full body",
    "daytime, cafe, sitting, drinking coffee, relaxed, upper body",
    "daytime, park, sitting on bench, peaceful, nature, full body",
    "daytime, shopping, bags, happy, satisfied, full body",
    "daytime, working, desk, focused, professional, upper body",
    "daytime, lunch, eating, restaurant, happy, upper body",
    "daytime, studying, library, focused, quiet, upper body",
    "daytime, meeting friends, chatting, cheerful, happy, upper body",
    "daytime, exercise, gym, active, energetic, full body",
    "daytime, reading, park, peaceful, relaxed, upper body",
    "daytime, window shopping, looking, interested, upper body",
    "daytime, bright, cheerful, energetic, happy, upper body",
    "daytime, productive, working, focused, determined, upper body",
    "daytime, relaxing, peaceful, calm, comfortable, upper body",
    "daytime, active, energetic, lively, dynamic, full body",
    "daytime, social, friendly, chatting, happy, upper body",
    "daytime, busy, working, multitasking, focused, upper body",
    "daytime, break time, resting, relaxed, peaceful, upper body",
    "daytime, outdoor, nature, fresh air, peaceful, full body",
    "daytime, confident, strong, capable, professional, upper body",

    # 저녁 (20)
    "evening, sunset, golden hour, beautiful, peaceful, upper body",
    "evening, walking home, tired, peaceful, relaxed, full body",
    "evening, cooking dinner, kitchen, focused, home, upper body",
    "evening, eating dinner, happy, satisfied, relaxed, upper body",
    "evening, watching tv, relaxed, comfortable, casual, upper body",
    "evening, reading, peaceful, quiet, calm, upper body",
    "evening, balcony, city view, peaceful, thoughtful, upper body",
    "evening, warm light, cozy, comfortable, peaceful, upper body",
    "evening, relaxing, tired, peaceful, calm, upper body",
    "evening, bathing, relaxed, comfortable, fresh, upper body",
    "evening, phone call, chatting, casual, relaxed, upper body",
    "evening, listening to music, peaceful, enjoying, upper body",
    "evening, drawing, creative, focused, artistic, upper body",
    "evening, gaming, playing, fun, energetic, upper body",
    "evening, social media, browsing, relaxed, casual, upper body",
    "evening, planning tomorrow, thinking, organized, upper body",
    "evening, stretching, relaxing, comfortable, peaceful, full body",
    "evening, gentle, peaceful, calm, serene, upper body",
    "evening, thoughtful, contemplative, reflective, peaceful, upper body",
    "evening, content, satisfied, happy, peaceful, upper body",

    # 밤 (15)
    "night, city lights, neon, colorful, urban, beautiful, upper body",
    "night, starry sky, looking up, peaceful, dreamy, upper body",
    "night, bedroom, preparing to sleep, sleepy, peaceful, upper body",
    "night, reading in bed, peaceful, quiet, calm, upper body",
    "night, late night snack, eating, casual, happy, upper body",
    "night, window, looking at moon, peaceful, thoughtful, upper body",
    "night, studying late, focused, tired, determined, upper body",
    "night, gaming, energetic, fun, excited, upper body",
    "night, mysterious, beautiful, atmospheric, peaceful, upper body",
    "night, sleepy, tired, yawning, drowsy, upper body",
    "night, peaceful, calm, serene, quiet, upper body",
    "night, drinking tea, relaxed, peaceful, warm, upper body",
    "night, writing, creative, focused, quiet, upper body",
    "night, dreamy, thoughtful, contemplative, peaceful, upper body",
    "night, ready to sleep, comfortable, cozy, peaceful, upper body",
]

for i in range(75):
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = TIME_SCENES[i % len(TIME_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {DOLSOE}, {scene}",
        "style": preset,
        "name": f"dolsoe_time_{i+1:02d}_{preset}",
        "category": "time",
    })

# === 3. 추가 일상 75장 ===
ADDITIONAL_DAILY = [
    # 취미/활동 (25)
    "painting, art, creative, focused, artistic, upper body",
    "playing guitar, music, passionate, focused, upper body",
    "taking photos, camera, photographer, interested, upper body",
    "gardening, plants, caring, gentle, outdoor, full body",
    "baking, cooking, apron, focused, kitchen, upper body",
    "knitting, crafting, focused, peaceful, calm, upper body",
    "writing, notebook, creative, thoughtful, focused, upper body",
    "practicing calligraphy, focused, elegant, artistic, upper body",
    "doing yoga, peaceful, calm, flexible, serene, full body",
    "playing video games, focused, fun, energetic, upper body",
    "watching movies, relaxed, enjoying, comfortable, upper body",
    "collecting, hobby, interested, curious, focused, upper body",
    "DIY project, crafting, focused, creative, working, upper body",
    "origami, folding paper, focused, careful, creative, upper body",
    "flower arranging, artistic, elegant, focused, gentle, upper body",
    "bird watching, binoculars, peaceful, nature, interested, upper body",
    "stargazing, telescope, dreamy, peaceful, night, upper body",
    "fishing, peaceful, patient, relaxed, outdoor, full body",
    "hiking, nature, energetic, active, healthy, full body",
    "cycling, bike, active, energetic, outdoor, full body",
    "skateboarding, cool, energetic, dynamic, sporty, full body",
    "dancing, energetic, graceful, dynamic, happy, full body",
    "singing, karaoke, happy, cheerful, energetic, upper body",
    "meditation, peaceful, calm, serene, spiritual, upper body",
    "volunteering, helping, kind, caring, gentle, upper body",

    # 인간관계/소셜 (25)
    "talking on phone, chatting, happy, cheerful, casual, upper body",
    "video call, computer, chatting, happy, casual, upper body",
    "texting, phone, smiling, casual, happy, upper body",
    "meeting friends, greeting, happy, cheerful, excited, upper body",
    "laughing with friends, joyful, happy, cheerful, upper body",
    "sharing food, friendly, kind, caring, happy, upper body",
    "taking selfie, phone, cheerful, fun, playful, upper body",
    "group photo, posing, happy, cheerful, friends, upper body",
    "gift giving, present, happy, kind, caring, upper body",
    "receiving gift, surprised, happy, grateful, excited, upper body",
    "hugging, warm, caring, gentle, loving, upper body",
    "high five, cheerful, energetic, happy, playful, upper body",
    "waving, greeting, cheerful, friendly, happy, upper body",
    "listening, attentive, caring, supportive, kind, upper body",
    "comforting, gentle, caring, kind, supportive, upper body",
    "celebrating, party, happy, cheerful, festive, upper body",
    "toast, drinking, cheers, happy, social, upper body",
    "playing board games, fun, competitive, cheerful, upper body",
    "picnic, outdoor, food, friends, happy, cheerful, full body",
    "shopping together, friends, happy, cheerful, fun, full body",
    "studying together, focused, supportive, helpful, upper body",
    "cooking together, teamwork, fun, happy, cheerful, upper body",
    "watching fireworks, amazed, happy, excited, night, upper body",
    "making memories, camera, happy, nostalgic, cheerful, upper body",
    "farewell, waving goodbye, emotional, sad, caring, upper body",

    # 감정/상태 (25)
    "confident, strong, powerful, determined, cool, upper body",
    "relaxed, peaceful, calm, serene, comfortable, upper body",
    "energetic, lively, dynamic, active, cheerful, upper body",
    "gentle, kind, caring, warm, loving, upper body",
    "focused, determined, serious, concentrated, working, upper body",
    "dreamy, imaginative, thoughtful, creative, peaceful, upper body",
    "playful, fun, mischievous, cheerful, energetic, upper body",
    "elegant, graceful, refined, sophisticated, beautiful, upper body",
    "cool, composed, calm, collected, confident, upper body",
    "warm, friendly, approachable, kind, gentle, upper body",
    "mysterious, enigmatic, intriguing, atmospheric, beautiful, upper body",
    "cheerful, bright, happy, optimistic, positive, upper body",
    "thoughtful, contemplative, reflective, deep, peaceful, upper body",
    "artistic, creative, expressive, imaginative, inspired, upper body",
    "athletic, sporty, strong, energetic, active, upper body",
    "intellectual, smart, knowledgeable, studious, focused, upper body",
    "fashionable, stylish, trendy, cool, confident, upper body",
    "natural, genuine, authentic, real, comfortable, upper body",
    "adventurous, bold, daring, brave, energetic, upper body",
    "nurturing, caring, maternal, gentle, kind, upper body",
    "ambitious, motivated, driven, determined, focused, upper body",
    "patient, calm, understanding, gentle, peaceful, upper body",
    "spontaneous, impulsive, energetic, fun, playful, upper body",
    "reserved, quiet, calm, peaceful, introverted, upper body",
    "expressive, emotional, open, genuine, authentic, upper body",
]

for i in range(75):
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = ADDITIONAL_DAILY[i % len(ADDITIONAL_DAILY)]

    JOBS.append({
        "prompt": f"1girl, {DOLSOE}, {scene}",
        "style": preset,
        "name": f"dolsoe_additional_{i+1:02d}_{preset}",
        "category": "additional",
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
    print(f"🐱💙 냥냥돌쇠 시즌2 메가 배치 {TOTAL}장! 🐱💙", flush=True)
    print(f"특수 의상 150 + 시간대 75 + 추가 일상 75", flush=True)
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
