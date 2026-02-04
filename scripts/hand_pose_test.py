"""
손가락 포즈 프리셋 테스트 배치
- 갸루피스 바리에이션 + 핸드 포즈 전체 테스트
- 프리셋별 10장씩 = 총 110장
"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_hand_pose_test"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

POSE_PRESETS = {
    "gyaru_peace": {
        "pose_tags": "detailed hands, perfect fingers, v sign, peace sign, gyaru pose, wink",
    },
    "double_peace": {
        "pose_tags": "detailed hands, perfect fingers, double v sign, both hands peace sign, w pose, cheerful",
    },
    "ura_peace": {
        "pose_tags": "detailed hands, perfect fingers, reverse peace sign, back of hand, v sign",
    },
    "face_peace": {
        "pose_tags": "detailed hands, perfect fingers, peace sign covering eye, hand near face",
    },
    "cheek_peace": {
        "pose_tags": "detailed hands, perfect fingers, peace sign on cheek, touching face, cute pose",
    },
    "heart_hands": {
        "pose_tags": "detailed hands, perfect fingers, heart hands, finger heart, heart shape",
    },
    "cheek_heart": {
        "pose_tags": "detailed hands, perfect fingers, hands on cheeks, heart shape on face, cute",
    },
    "finger_gun": {
        "pose_tags": "detailed hands, perfect fingers, finger gun, pointing, index finger",
    },
    "cat_paw": {
        "pose_tags": "detailed hands, perfect fingers, cat paw pose, curled fingers, playful",
    },
    "thumbs_up": {
        "pose_tags": "detailed hands, perfect fingers, thumbs up, fist, thumb raised",
    },
    "hand_wave": {
        "pose_tags": "detailed hands, perfect fingers, waving hand, open palm, greeting",
    },
}

PER_PRESET = 10

CHARACTERS = [
    {"tags": "1girl, reze, chainsaw man, purple hair, short hair, red eyes", "alias": "reze"},
    {"tags": "1girl, makima, chainsaw man, orange hair, braided ponytail, yellow eyes", "alias": "makima"},
    {"tags": "1girl, power, chainsaw man, blonde hair, red horns, red eyes", "alias": "power"},
    {"tags": "1girl, gotoh hitori, bocchi the rock!, pink hair, blue eyes, shy", "alias": "bocchi"},
    {"tags": "1girl, kita ikuyo, bocchi the rock!, red hair, green eyes", "alias": "kita"},
    {"tags": "1girl, senjougahara hitagi, bakemonogatari, purple hair, sharp eyes", "alias": "hitagi"},
    {"tags": "1girl, oshino shinobu, bakemonogatari, blonde hair, yellow eyes, vampire", "alias": "shinobu"},
    {"tags": "1girl, frieren, sousou no frieren, white hair, elf ears, mage", "alias": "frieren"},
    {"tags": "1girl, kitagawa marin, sono bisque doll, blonde hair, brown eyes, gyaru", "alias": "marin"},
    {"tags": "1girl, hatsune miku, vocaloid, aqua hair, twintails, aqua eyes, headset", "alias": "miku"},
    {"tags": "1girl, zero two, darling in the franxx, pink hair, green eyes, horns", "alias": "zero_two"},
    {"tags": "1girl, rem, re:zero, blue hair, blue eyes, maid, x hair ornament", "alias": "rem"},
    {"tags": "1girl, kitashirakawa tamako, tamako market, black hair, short hair, brown eyes, cheerful", "alias": "tamako"},
    {"tags": "1girl, nishikigi chisato, lycoris recoil, blonde hair, red eyes, hair ribbon", "alias": "chisato"},
]

BACKGROUNDS = [
    {"tags": "school, hallway, bright", "alias": "school"},
    {"tags": "cafe, indoors, warm light", "alias": "cafe"},
    {"tags": "cherry blossoms, outdoors, spring", "alias": "sakura"},
    {"tags": "purikura, photo booth, stickers, sparkles", "alias": "purikura"},
    {"tags": "selfie, phone camera, mirror", "alias": "selfie"},
    {"tags": "rooftop, blue sky, wind", "alias": "rooftop"},
    {"tags": "park, bench, trees, sunny", "alias": "park"},
]

NEGATIVE = (
    "lowres, bad anatomy, error, text, signature, "
    "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, "
    "poorly drawn hands, wrong number of fingers, six fingers, four fingers, "
    "mutated hands, malformed hands, twisted fingers, interlocked fingers, "
    "extra digit, fewer digits, cropped fingers"
)


async def generate(client, idx, total, preset_name, pose_tags, char, bg):
    prompt = (
        f"{char['tags']}, {pose_tags}, "
        f"{bg['tags']}, masterpiece, best quality"
    )
    filename = f"{preset_name}_{char['alias']}_{bg['alias']}"

    payload = {
        "prompt": prompt,
        "negative_prompt": NEGATIVE,
        "width": 832,
        "height": 1216,
        "style": preset_name,
        "model": "animagine-xl-4",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=300.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{filename}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:03d}/{total}] OK [{preset_name}] {char['alias']}_{bg['alias']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:03d}/{total}] FAIL [{preset_name}]: {data.get('error', '?')}")
            return False
    except Exception as e:
        print(f"[{idx:03d}/{total}] ERROR [{preset_name}]: {e}")
        return False


async def main():
    jobs = []
    for preset_name, preset_info in POSE_PRESETS.items():
        for _ in range(PER_PRESET):
            jobs.append((
                preset_name,
                preset_info["pose_tags"],
                random.choice(CHARACTERS),
                random.choice(BACKGROUNDS),
            ))
    random.shuffle(jobs)

    total = len(jobs)
    ok = fail = 0

    print(f"손가락 포즈 테스트 배치 {total}장")
    print(f"프리셋 {len(POSE_PRESETS)}개 x {PER_PRESET}장")
    print(f"캐릭터 {len(CHARACTERS)}명 / 배경 {len(BACKGROUNDS)}개")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)
    for name in POSE_PRESETS:
        print(f"  - {name}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, (preset_name, pose_tags, char, bg) in enumerate(jobs, 1):
            if await generate(client, i, total, preset_name, pose_tags, char, bg):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
