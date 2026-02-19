"""냥냥돌쇠 모노가타리 스타일 30장 - 다양한 구도/포즈"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_dolsoe_monogatari"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHAR = "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sharp eyes"

JOBS = [
    # 헤드틸트 시리즈
    {"pose": "head tilt, looking at viewer, elegant, upper body", "name": "head_tilt1"},
    {"pose": "head tilt, mysterious smile, side lighting, upper body", "name": "head_tilt2"},
    {"pose": "head tilt, chin on hand, thinking, upper body", "name": "head_tilt3"},

    # 클로즈업
    {"pose": "close up, face focus, intense gaze, dramatic lighting", "name": "closeup_intense"},
    {"pose": "close up, eye focus, large eyes, sharp highlights", "name": "closeup_eyes"},
    {"pose": "extreme close up, one eye visible, mysterious", "name": "closeup_one_eye"},

    # 포즈 바리에이션
    {"pose": "sitting, crossed legs, confident, full body", "name": "sit_crossed"},
    {"pose": "sitting on chair, legs crossed, elegant, side view", "name": "sit_chair"},
    {"pose": "lying down, on bed, relaxed, looking at viewer", "name": "lying_bed"},
    {"pose": "standing, hand on hip, confident, full body", "name": "stand_hip"},
    {"pose": "leaning against wall, cool, shadow, upper body", "name": "lean_wall"},
    {"pose": "back view, looking over shoulder, mysterious", "name": "back_look"},

    # 샤프트 앵글
    {"pose": "dutch angle, dramatic, artistic, upper body", "name": "dutch_angle"},
    {"pose": "low angle, looking down, powerful, full body", "name": "low_angle"},
    {"pose": "high angle, looking up, vulnerable, upper body", "name": "high_angle"},
    {"pose": "bird eye view, from above, artistic", "name": "bird_eye"},

    # 표정 바리에이션
    {"pose": "smirk, confident, looking at viewer, upper body", "name": "smirk"},
    {"pose": "blank stare, emotionless, stoic, upper body", "name": "blank"},
    {"pose": "gentle smile, warm, soft lighting, upper body", "name": "gentle"},
    {"pose": "surprised, wide eyes, cute, upper body", "name": "surprised"},
    {"pose": "angry, sharp eyes, intense, upper body", "name": "angry"},
    {"pose": "sad, looking down, melancholic, upper body", "name": "sad"},
    {"pose": "yandere, crazy smile, intense, close up", "name": "yandere"},

    # 상황 연출
    {"pose": "reading book, focused, sitting, cozy", "name": "reading"},
    {"pose": "drinking tea, elegant, side profile", "name": "tea"},
    {"pose": "looking at phone, modern, casual, upper body", "name": "phone"},
    {"pose": "in shadow, silhouette, dramatic, artistic", "name": "shadow"},
    {"pose": "window, backlit, atmospheric, looking out", "name": "window"},
    {"pose": "night, stars, looking up at sky, peaceful", "name": "night_sky"},
    {"pose": "rain, wet hair, emotional, dramatic", "name": "rain"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{CHAR}, {job['pose']}, masterpiece",
        "negative_prompt": "low quality, worst quality",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": "monogatari",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{idx:02d}_{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"냥냥돌쇠 모노가타리 스타일 {TOTAL}장")
    print(f"다양한 구도/포즈/표정")
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
