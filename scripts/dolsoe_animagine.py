"""냥냥돌쇠 전체 프리셋 테스트 - Animagine XL 4.0"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_animagine"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHAR = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes"

# 프리셋 + 어울리는 포즈/상황
JOBS = [
    # 일반 스타일
    {"style": "pale_aqua", "pose": "gentle smile, flowers, soft lighting, upper body", "name": "pale_aqua"},
    {"style": "mono_halftone", "pose": "smirk, cool pose, stylish, upper body", "name": "mono_halftone"},
    {"style": "chibi_sketch", "pose": "happy, jumping, full body, cute", "name": "chibi_sketch"},
    {"style": "cozy_gouache", "pose": "reading book, cozy room, warm lighting", "name": "cozy_gouache"},
    {"style": "watercolor_sketch", "pose": "wind, hair flowing, melancholic, looking away", "name": "watercolor_sketch"},

    # 스튜디오 스타일
    {"style": "kyoto_animation", "pose": "school uniform, classroom, window light, gentle", "name": "kyoto_animation"},
    {"style": "ufotable", "pose": "action pose, magic effects, dramatic lighting", "name": "ufotable"},
    {"style": "shinkai", "pose": "looking at sky, sunset, clouds, wind", "name": "shinkai"},
    {"style": "ghibli", "pose": "nature, walking, grass field, peaceful", "name": "ghibli"},
    {"style": "trigger", "pose": "dynamic pose, speed lines, energetic", "name": "trigger"},
    {"style": "mappa", "pose": "intense expression, dramatic shadow, cool", "name": "mappa"},
    {"style": "shaft", "pose": "head tilt, geometric background, artistic", "name": "shaft"},
    {"style": "monogatari", "pose": "head tilt, elegant, looking at viewer, mysterious", "name": "monogatari"},

    # 게임 스타일
    {"style": "genshin", "pose": "fantasy outfit, magic circle, glowing, dramatic", "name": "genshin"},
    {"style": "blue_archive", "pose": "school uniform, halo, rooftop, cheerful", "name": "blue_archive"},
    {"style": "arknights", "pose": "tactical outfit, industrial background, cool", "name": "arknights"},
    {"style": "fate", "pose": "elegant dress, noble, dramatic pose", "name": "fate"},

    # 분위기 스타일
    {"style": "cyberpunk", "pose": "neon lights, night city, futuristic outfit", "name": "cyberpunk"},
    {"style": "pastel_soft", "pose": "dreamy, flowers, soft, gentle smile", "name": "pastel_soft"},
    {"style": "inuyasha", "pose": "feudal japan outfit, wind, nostalgic", "name": "inuyasha"},
    {"style": "sepia_backlit", "pose": "backlit, sunset, dreamy, silhouette", "name": "sepia_backlit"},
    {"style": "mono_accent", "pose": "stylish pose, limited color, cool", "name": "mono_accent"},
    {"style": "sketch_colorpop", "pose": "artistic pose, color accent, expressive", "name": "sketch_colorpop"},
    {"style": "pop_fanart", "pose": "cute, blush, looking at viewer, simple", "name": "pop_fanart"},

    # 특수 스타일
    {"style": "split_sketch", "pose": "close up face, expressive eyes", "name": "split_sketch"},
    {"style": "waterful", "pose": "serene, flowers, soft lighting, peaceful", "name": "waterful"},
    {"style": "bold_pop", "pose": "confident, stylish, bold expression, cool", "name": "bold_pop"},
    {"style": "retro_glitch", "pose": "glitch aesthetic, digital, artistic", "name": "retro_glitch"},

    # 손포즈
    {"style": "gyaru_peace", "pose": "gyaru peace, wink, selfie angle, cheerful", "name": "gyaru_peace"},
    {"style": "double_peace", "pose": "double peace sign, energetic, jumping", "name": "double_peace"},
    {"style": "heart_hands", "pose": "heart hands, cute, blushing, lovely", "name": "heart_hands"},
    {"style": "finger_gun", "pose": "finger gun, confident, wink, cool", "name": "finger_gun"},
    {"style": "cat_paw", "pose": "cat pose, paw hands, playful, nya", "name": "cat_paw"},
    {"style": "thumbs_up", "pose": "thumbs up, bright smile, encouraging", "name": "thumbs_up"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{CHAR}, {job['pose']}, masterpiece, best quality",
        "negative_prompt": "low quality, worst quality, bad anatomy, bad hands",
        "width": 832,
        "height": 1216,  # Animagine XL은 세로 길이 조금 더 가능
        "steps": 28,
        "guidance_scale": 7.0,  # Animagine은 보통 7.0 권장
        "provider": "local",  # 로컬 모델 사용
        "model": "animagine-xl-4",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=300.0)  # 로컬은 더 오래 걸릴 수 있음
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{idx:02d}_{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:60]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"냥냥돌쇠 전체 프리셋 - Animagine XL 4.0 ({TOTAL}장)")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.5)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
