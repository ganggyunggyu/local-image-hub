"""초메가배치 1000장 - 모노가타리 프리셋 × 7작품 캐릭터"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_mega_monogatari_1000"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTERS = {
    # === 장송의 프리렌 ===
    "frieren": "1girl, frieren, long white hair, green eyes, elf ears, purple robe, calm expression",
    "fern": "1girl, fern \\(frieren\\), long purple hair, dark eyes, serious, mage robe",
    "himmel": "1boy, himmel \\(frieren\\), short blue hair, handsome, hero outfit, kind smile",
    "stark": "1boy, stark \\(frieren\\), spiky red hair, warrior, muscular, shy expression",
    "aura": "1girl, aura \\(frieren\\), long blonde hair, demon, red eyes, elegant, dark dress",
    "serie": "1girl, serie \\(frieren\\), very long purple hair, elf ears, ancient mage, powerful",
    "ubel": "1girl, ubel \\(frieren\\), short dark hair, sharp eyes, mischievous smile, mage robe",

    # === 봇치 더 락 ===
    "bocchi": "1girl, gotoh hitori, long pink hair, blue eyes, shy, anxious, pink tracksuit",
    "nijika": "1girl, ijichi nijika, blonde hair, twin tails, cheerful, energetic, drummer",
    "ryo": "1girl, yamada ryo, long blue hair, cool, stoic, bass guitar, blue eyes",
    "kita": "1girl, kita ikuyo, short red hair, bright smile, energetic, guitar, yellow eyes",
    "pa_san": "1woman, ijichi seika, short dark hair, tired expression, band manager, suit",

    # === 모노가타리 시리즈 ===
    "senjougahara": "1girl, senjougahara hitagi, long purple hair, sharp eyes, cold beauty, school uniform",
    "hanekawa": "1girl, hanekawa tsubasa, long black hair, glasses, gentle, school uniform",
    "shinobu": "1girl, oshino shinobu, blonde hair, golden eyes, white dress, vampire",
    "nadeko": "1girl, sengoku nadeko, short orange hair, bangs covering eyes, shy, school uniform",
    "kanbaru": "1girl, kanbaru suruga, short dark hair, sporty, athletic, tomboyish",
    "yotsugi": "1girl, ononoki yotsugi, short green hair, orange hat, expressionless",
    "kiss_shot": "1girl, kiss-shot acerola-orion heart-under-blade, very long blonde hair, red eyes, elegant dress, vampire queen",
    "black_hanekawa": "1girl, black hanekawa, long white hair, cat ears, golden eyes, seductive",
    "kaiki": "1man, kaiki deishuu, dark hair, black suit, stubble, tired expression",

    # === 걸밴크라이 ===
    "nina": "1girl, nina \\(girl band cry\\), long pink hair, twin tails, guitarist, energetic, cute",
    "subaru": "1girl, subaru \\(girl band cry\\), short black hair, cool, bassist, sharp eyes",
    "rupa": "1girl, rupa \\(girl band cry\\), blonde hair, drummer, cheerful, bright smile",
    "tomo": "1girl, tomo \\(girl band cry\\), brown hair, ponytail, vocalist, passionate",
    "momoka": "1girl, momoka \\(girl band cry\\), purple hair, keyboard, calm, elegant",

    # === 케이온 ===
    "yui": "1girl, hirasawa yui, short brown hair, hairclip, cheerful, guitar, school uniform",
    "mio": "1girl, akiyama mio, long black hair, shy, bass guitar, elegant, school uniform",
    "ritsu": "1girl, tainaka ritsu, short brown hair, headband, energetic, drums, tomboyish",
    "mugi": "1girl, kotobuki tsumugi, long blonde hair, thick eyebrows, gentle, keyboard, rich",
    "azusa": "1girl, nakano azusa, long black hair, twin tails, serious, guitar, cat ears",

    # === 패배히로인이 너무 많아 ===
    "yanami": "1girl, yanami anna, long light brown hair, side ponytail, cheerful, school uniform, ribbon",
    "komari": "1girl, komari chika, short pink hair, glasses, quiet, bookworm, school uniform",
    "lemon": "1girl, hakuto lemon, long blonde hair, twintails, tsundere, school uniform, blue ribbon",
    "karen": "1girl, shikimura karen, long black hair, elegant, ojou-sama, school uniform",

    # === 로젠메이든 ===
    "shinku": "1girl, shinku, long blonde hair, red dress, twin tails, elegant, doll joints, rose",
    "suigintou": "1girl, suigintou, long silver hair, black dress, wings, gothic, dark, violet eyes",
    "suiseiseki": "1girl, suiseiseki, long brown hair, green dress, heterochromia, red and green eyes, desu",
    "souseiseki": "1girl, souseiseki, short blue hair, blue outfit, boyish, hat, heterochromia",
    "hinaichigo": "1girl, hinaichigo, blonde hair, pink dress, small, cute, childish, strawberry",
    "kanaria": "1girl, kanaria, blonde hair, green dress, violin, cheerful, energetic",
    "barasuishou": "1girl, barasuishou, lavender hair, eye patch, crystal dress, mysterious, elegant",
}

POSES = [
    # 모노가타리 시그니처
    "head tilt, looking at viewer, mysterious smile, upper body",
    "head tilt, side glance, enigmatic, close up face",
    "head tilt, finger on lips, playful, upper body",
    "head tilt, closed eyes, serene, profile view",

    # 감정 표현
    "gentle smile, soft lighting, upper body",
    "arms crossed, cool expression, confident",
    "blushing, looking away, shy",
    "laughing, hand near mouth, joyful",
    "melancholic, wind in hair, looking at distance",
    "fierce expression, sharp gaze, intense, close up",
    "surprised, wide eyes, dramatic",
    "pouting, annoyed, cute anger",
    "smug, one eye closed, playful",
    "crying, tears, emotional, beautiful",
    "determined, fist clenched, serious",

    # 일상
    "reading book, sitting, cozy, warm lighting",
    "drinking tea, cafe, relaxed, afternoon",
    "walking, cherry blossoms, spring, peaceful",
    "sitting on bench, park, autumn leaves",
    "leaning on window, rainy day, contemplative",
    "stretching, morning light, sleepy",
    "eating snack, happy, casual",
    "listening to music, headphones, eyes closed",

    # 옥외/배경
    "standing in rain, umbrella, moody atmosphere",
    "rooftop, sunset sky, dramatic clouds, wind",
    "night city, lights, atmospheric, urban",
    "standing under sakura, petals, dreamy",
    "staircase, dramatic lighting, geometric shadow",
    "bus stop, evening, warm street light, waiting",
    "beach, summer, ocean, sun, bright",
    "snowy street, winter coat, cold breath",

    # 스타일리시
    "profile view, wind blowing hair, cinematic",
    "back view, looking over shoulder, elegant",
    "close up eyes, detailed iris, beautiful",
    "silhouette, backlit, dramatic, artistic",
    "mirror reflection, artistic, atmospheric",
    "hand reaching out, emotional, dramatic light",

    # 액션/판타지
    "action pose, dynamic, speed lines",
    "magic circle, glowing, fantasy, powerful",
    "running, hair flowing, dynamic angle",
    "playing instrument, passionate, stage lighting",
]

JOBS = []
random.seed(1000)

char_keys = list(CHARACTERS.keys())

for i in range(1000):
    char_key = char_keys[i % len(char_keys)]
    pose = random.choice(POSES)
    JOBS.append({
        "char_key": char_key,
        "tags": CHARACTERS[char_key],
        "pose": pose,
        "name": f"{i:04d}_{char_key}",
    })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['tags']}, {job['pose']}, masterpiece, best quality",
        "negative_prompt": "low quality, worst quality, bad anatomy, bad hands",
        "width": 832,
        "height": 1216,
        "provider": "nai",
        "model": "nai-diffusion-4-curated-preview",
        "style": "monogatari",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=120.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{num:04d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{num:04d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:60]}")
            return False
    except Exception as e:
        print(f"[{num:04d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0

    series_count = {
        "프리렌": 0, "봇치더락": 0, "모노가타리": 0,
        "걸밴크라이": 0, "케이온": 0, "패배히로인": 0, "로젠메이든": 0,
    }
    series_map = {
        "frieren": "프리렌", "fern": "프리렌", "himmel": "프리렌",
        "stark": "프리렌", "aura": "프리렌", "serie": "프리렌", "ubel": "프리렌",
        "bocchi": "봇치더락", "nijika": "봇치더락", "ryo": "봇치더락",
        "kita": "봇치더락", "pa_san": "봇치더락",
        "senjougahara": "모노가타리", "hanekawa": "모노가타리", "shinobu": "모노가타리",
        "nadeko": "모노가타리", "kanbaru": "모노가타리", "yotsugi": "모노가타리",
        "kiss_shot": "모노가타리", "black_hanekawa": "모노가타리", "kaiki": "모노가타리",
        "nina": "걸밴크라이", "subaru": "걸밴크라이", "rupa": "걸밴크라이",
        "tomo": "걸밴크라이", "momoka": "걸밴크라이",
        "yui": "케이온", "mio": "케이온", "ritsu": "케이온",
        "mugi": "케이온", "azusa": "케이온",
        "yanami": "패배히로인", "komari": "패배히로인",
        "lemon": "패배히로인", "karen": "패배히로인",
        "shinku": "로젠메이든", "suigintou": "로젠메이든", "suiseiseki": "로젠메이든",
        "souseiseki": "로젠메이든", "hinaichigo": "로젠메이든",
        "kanaria": "로젠메이든", "barasuishou": "로젠메이든",
    }
    for j in JOBS:
        series = series_map.get(j["char_key"], "?")
        series_count[series] = series_count.get(series, 0) + 1

    print(f"초메가배치 1000장 - 모노가타리 프리셋 × 7작품")
    print(f"\n작품별 분포:")
    for s, n in sorted(series_count.items(), key=lambda x: -x[1]):
        print(f"  {s}: {n}장")
    print(f"\n캐릭터: {len(CHARACTERS)}명 / 포즈: {len(POSES)}종")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(1.0)

            if i % 100 == 0:
                print(f"--- {i}/{TOTAL} 진행 중 (성공: {ok}, 실패: {fail}) ---")

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
