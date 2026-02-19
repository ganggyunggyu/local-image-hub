"""전체 프리셋 테스트 - 냥냥돌쇠"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_all_presets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHAR_BASE = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes"

# 스타일별 포즈/프롬프트
JOBS = [
    # 일반 스타일
    {"style": "pale_aqua", "pose": "smile, looking at viewer, upper body"},
    {"style": "mono_halftone", "pose": "smirk, looking at viewer, upper body"},
    {"style": "chibi_sketch", "pose": "happy, full body, jumping"},
    {"style": "cozy_gouache", "pose": "reading book, sitting, cozy"},
    {"style": "watercolor_sketch", "pose": "gentle smile, wind, hair flowing"},
    {"style": "kyoto_animation", "pose": "school uniform, classroom, window"},
    {"style": "ufotable", "pose": "action pose, dramatic, magic"},
    {"style": "shinkai", "pose": "looking at sky, sunset, wind"},
    {"style": "ghibli", "pose": "nature, peaceful, walking"},
    {"style": "trigger", "pose": "dynamic pose, energetic, action"},
    {"style": "mappa", "pose": "intense, dramatic lighting, cool"},
    {"style": "shaft", "pose": "head tilt, mysterious, artistic"},
    {"style": "monogatari", "pose": "head tilt, elegant, looking at viewer"},
    {"style": "genshin", "pose": "fantasy outfit, magic, glowing"},
    {"style": "blue_archive", "pose": "school uniform, halo, cheerful"},
    {"style": "arknights", "pose": "tactical, cool, industrial"},
    {"style": "fate", "pose": "elegant dress, noble, dramatic"},
    {"style": "cyberpunk", "pose": "neon, night city, futuristic"},
    {"style": "pastel_soft", "pose": "gentle, dreamy, flowers"},
    {"style": "inuyasha", "pose": "feudal japan, wind, nostalgic"},
    {"style": "sepia_backlit", "pose": "backlit, sunset, dreamy"},
    {"style": "mono_accent", "pose": "stylish, cool, limited color"},
    {"style": "sketch_colorpop", "pose": "sketch, color accent, artistic"},
    {"style": "pop_fanart", "pose": "cute, blush, looking at viewer"},
    # 포즈 프리셋 - 해당 포즈 추가
    {"style": "gyaru_peace", "pose": "gyaru peace, v sign, wink, cheerful"},
    {"style": "double_peace", "pose": "double peace sign, both hands, energetic"},
    {"style": "ura_peace", "pose": "peace sign, back of hand showing, cool"},
    {"style": "face_peace", "pose": "peace sign near face, cute"},
    {"style": "cheek_peace", "pose": "peace sign on cheek, adorable"},
    {"style": "heart_hands", "pose": "heart hands, finger heart, lovely"},
    {"style": "cheek_heart", "pose": "heart on cheek, cute pose"},
    {"style": "finger_gun", "pose": "finger gun, pointing, confident"},
    {"style": "cat_paw", "pose": "cat pose, paw hands, playful, nya"},
    {"style": "thumbs_up", "pose": "thumbs up, encouraging, bright"},
    {"style": "hand_wave", "pose": "waving hand, greeting, friendly"},
    {"style": "split_sketch", "pose": "close up face, expressive eyes"},
    {"style": "waterful", "pose": "serene, flowers, soft lighting"},
    {"style": "bold_pop", "pose": "confident, stylish, bold expression"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    style = job["style"]
    pose = job["pose"]
    payload = {
        "prompt": f"{CHAR_BASE}, {pose}, masterpiece",
        "negative_prompt": "low quality, worst quality",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": style,
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{idx:02d}_{style}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {style}")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {style}: {data.get('error', '?')[:40]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {style}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"전체 프리셋 테스트 {TOTAL}장 (냥냥돌쇠)")
    print(f"포즈 다양하게!")
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


if __name__ == "__main__":
    asyncio.run(main())
