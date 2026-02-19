"""봇치 더 락 성인 캐릭터 3명 메가 배치 300장"""

import asyncio
from datetime import datetime
from pathlib import Path
from base64 import b64decode

import httpx

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_bocchi_adults_300"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 봇치 더 락 성인 캐릭터 3명
CHARACTERS = [
    ("nijika", "ijichi nijika, bocchi the rock, pink hair, side ponytail, yellow eyes, cheerful, energetic, drummer, band leader"),
    ("pa_san", "pa-san, bocchi the rock, long black hair, red glasses, mature, professional, live house staff, ponytail, cool"),
    ("kikuri", "hiroi kikuri, bocchi the rock, pink twin tails, yellow eyes, bassist, drunk, devilish, chaotic, mischievous"),
]

# 이쁜 프리셋 모음
PRETTY_PRESETS = [
    "pale_aqua", "monogatari", "kyoto_animation", "pastel_soft",
    "waterful", "blue_archive", "pop_fanart", "watercolor_sketch",
    "cozy_gouache", "ghibli", "shinkai", "sepia_backlit",
]

NEGATIVE = "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers"

JOBS = []

# === 1. 일상 상황 75장 ===
DAILY_SCENES = [
    # 라이브하우스/직장
    "live house, working, professional, focused, upper body",
    "live house, backstage, preparing, busy, upper body",
    "live house, bar counter, serving drinks, smiling, upper body",
    "live house, soundcheck, microphone, testing, upper body",
    "live house, stage, setting up, equipment, full body",
    "live house, office, paperwork, serious, upper body",
    "live house, cleaning, responsible, working, full body",
    "live house, talking to customer, friendly, professional, upper body",

    # 카페/음식
    "cafe, sitting, drinking coffee, relaxed, warm lighting, upper body",
    "cafe, reading menu, thinking, choosing, upper body",
    "cafe, eating dessert, happy, enjoying, upper body",
    "restaurant, dining, happy, delicious, upper body",
    "bar, drinking, relaxed, adult, night, upper body",
    "izakaya, eating, drinking, cheerful, casual, upper body",
    "kitchen, cooking, focused, home, upper body",
    "convenience store, shopping, casual, night, upper body",

    # 거리/도시
    "city street, walking, casual clothes, shopping bags, full body",
    "night city, neon lights, colorful, vibrant, urban, upper body",
    "park, sitting on bench, relaxed, peaceful, full body",
    "bookstore, browsing, interested, intellectual, upper body",
    "shopping mall, walking, shopping, happy, full body",
    "street, window shopping, looking at display, upper body",

    # 집/방
    "bedroom, lying on bed, relaxed, cozy, full body",
    "living room, sitting on sofa, watching tv, casual, upper body",
    "desk, working, laptop, focused, night, upper body",
    "window, looking outside, thoughtful, peaceful, upper body",
    "balcony, evening, city view, relaxed, upper body",
    "bathroom, mirror, fixing hair, preparing, upper body",
    "kitchen, making coffee, morning routine, upper body",
]

for i in range(75):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = DAILY_SCENES[i % len(DAILY_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {scene}",
        "style": preset,
        "name": f"bocchi_adults_daily_{i+1:03d}_{alias}_{preset}",
        "category": "daily",
    })

# === 2. 감정 표현 75장 ===
EMOTION_POSES = [
    # 기쁨/행복
    "laughing, bright smile, sparkling eyes, joyful, happy, upper body",
    "giggling, amused, entertained, cheerful, upper body",
    "excited, arms up, energetic, thrilled, upper body",
    "satisfied, content smile, peaceful, happy, upper body",
    "playful, winking, fun, cheerful, upper body",
    "proud, confident smile, accomplished, upper body",
    "cheerful, peace sign, bright, energetic, upper body",
    "delighted, eyes shining, amazed, happy, upper body",

    # 성숙/쿨
    "cool, composed, calm, collected, confident, upper body",
    "serious, focused, professional, mature, upper body",
    "confident, smirking, self-assured, cool, upper body",
    "mature, elegant, graceful, sophisticated, upper body",
    "determined, strong-willed, focused, intense, upper body",
    "charismatic, attractive, charming, confident, upper body",

    # 수줍음/부끄러움
    "shy, blushing, looking away, embarrassed, upper body",
    "flustered, red face, panicked, embarrassed, upper body",
    "bashful, hiding face, cute, shy, upper body",
    "embarrassed, puffed cheeks, flustered, cute, upper body",

    # 피곤/술취함
    "sleepy, yawning, tired, drowsy, upper body",
    "exhausted, half-closed eyes, tired, weary, upper body",
    "drunk, tipsy, red face, dizzy, happy, upper body",
    "hangover, tired, suffering, headache, upper body",
    "lazy, stretching, relaxed, comfortable, upper body",

    # 장난기/악동
    "mischievous, plotting, scheming smile, playful, upper body",
    "teasing, playful, cheeky, mischievous, upper body",
    "smug, smirking, confident, superior, upper body",
    "devilish, evil grin, mischievous, chaotic, upper body",
    "prankster, planning, scheming, playful, upper body",

    # 기타 감정
    "thinking, hand on chin, pondering, thoughtful, upper body",
    "worried, anxious, concerned, nervous, upper body",
    "surprised, eyes wide, shock, amazed, upper body",
    "gentle, warm smile, kind, caring, upper body",
    "nostalgic, remembering, thoughtful, emotional, upper body",
    "hopeful, looking up, optimistic, bright, upper body",
]

for i in range(75):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    emotion = EMOTION_POSES[i % len(EMOTION_POSES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {emotion}",
        "style": preset,
        "name": f"bocchi_adults_emotion_{i+1:03d}_{alias}_{preset}",
        "category": "emotion",
    })

# === 3. 음악/라이브 75장 ===
MUSIC_SCENES = [
    # 연주
    "playing drums, energetic, dynamic, powerful, performance, upper body",
    "playing bass, focused, cool, professional, upper body",
    "holding instrument, confident, musician, proud, upper body",
    "tuning instrument, careful, focused, preparing, upper body",
    "practicing, focused, serious, dedicated, upper body",
    "jamming, energetic, happy, enjoying music, upper body",
    "solo performance, spotlight, confident, cool, upper body",
    "playing passionately, emotional, intense, moved, upper body",

    # 라이브/공연
    "live performance, stage, lights, exciting, energetic, upper body",
    "concert, audience, performing, passionate, upper body",
    "stage lights, colorful, exciting, dynamic, performance, upper body",
    "band performance, together, teamwork, harmony, upper body",
    "finale, ending, triumphant, successful, happy, upper body",
    "encore, excited, happy, grateful, performing, upper body",
    "soundcheck, preparing, focused, professional, upper body",
    "backstage, nervous, excited, preparing, upper body",
    "after performance, happy, exhausted, satisfied, upper body",

    # 직원/스태프
    "managing, professional, responsible, focused, upper body",
    "organizing, planning, serious, professional, upper body",
    "checking equipment, technical, careful, upper body",
    "helping band, supportive, kind, professional, upper body",
    "teaching, explaining, patient, knowledgeable, upper body",

    # 음악 감상
    "listening to music, headphones, enjoying, peaceful, upper body",
    "absorbed in music, eyes closed, emotional, peaceful, upper body",
    "nodding to music, enjoying rhythm, relaxed, upper body",
]

for i in range(75):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = MUSIC_SCENES[i % len(MUSIC_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {scene}",
        "style": preset,
        "name": f"bocchi_adults_music_{i+1:03d}_{alias}_{preset}",
        "category": "music",
    })

# === 4. 특별한 순간 75장 ===
SPECIAL_SCENES = [
    "sunset, golden hour, wind, hair flowing, emotional, upper body",
    "night, moonlight, mysterious, beautiful, urban, upper body",
    "neon lights, colorful, vibrant, modern, night, upper body",
    "rain, umbrella, wet, atmospheric, night, upper body",
    "starry sky, looking up, dreamy, peaceful, upper body",
    "dramatic lighting, cinematic, intense, emotional, upper body",
    "soft lighting, gentle, peaceful, serene, upper body",
    "backlight, silhouette, dramatic, mysterious, upper body",
    "spotlight, stage, performance, confident, dramatic, upper body",
    "candlelight, warm, intimate, gentle, atmospheric, upper body",
    "natural light, window, peaceful, gentle, morning, upper body",
    "magic hour, dreamy, beautiful, enchanting, romantic, upper body",
    "city lights, night, urban, modern, beautiful, upper body",
    "reflections, water, mirror, beautiful, artistic, upper body",
    "wind, hair flowing, dynamic, beautiful, elegant, upper body",
    "lens flare, bright, hopeful, optimistic, cheerful, upper body",
    "bokeh, blurred background, focused, beautiful, artistic, upper body",
    "fireworks, colorful, night, festive, amazed, upper body",
    "cherry blossoms, spring, petals falling, peaceful, beautiful, upper body",
    "autumn leaves, falling, nostalgic, warm colors, atmospheric, upper body",
    "snow, winter, cold, beautiful, peaceful, upper body",
    "morning light, fresh, hopeful, new beginning, bright, upper body",
    "evening glow, warm, peaceful, relaxed, calm, upper body",
    "blue hour, twilight, mysterious, beautiful, atmospheric, upper body",
    "golden light, warm, beautiful, enchanting, magical, upper body",
]

for i in range(75):
    char_idx = i % len(CHARACTERS)
    alias, char_tags = CHARACTERS[char_idx]
    preset = PRETTY_PRESETS[i % len(PRETTY_PRESETS)]
    scene = SPECIAL_SCENES[i % len(SPECIAL_SCENES)]

    JOBS.append({
        "prompt": f"1girl, {char_tags}, {scene}",
        "style": preset,
        "name": f"bocchi_adults_special_{i+1:03d}_{alias}_{preset}",
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
    print(f"🎸 봇치 더 락 성인 캐릭터 3명 메가 배치 {TOTAL}장! 🎸", flush=True)
    print(f"니지카, PA상, 키쿠리 각 100장씩", flush=True)
    print(f"일상 75 + 감정 75 + 음악 75 + 특별한 순간 75", flush=True)
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
