"""
갸루피스 추가 100장 배치
- 50장 배치 완료 후 자동 실행용
"""

import asyncio
import random
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_gyaru_peace"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PRESET = "gyaru_peace"

CHARACTERS = [
    {"tags": "1girl, reze, chainsaw man, purple hair, short hair, red eyes", "alias": "reze"},
    {"tags": "1girl, makima, chainsaw man, orange hair, braided ponytail, yellow eyes", "alias": "makima"},
    {"tags": "1girl, power, chainsaw man, blonde hair, red horns, red eyes", "alias": "power"},
    {"tags": "1girl, hiroi kikuri, bocchi the rock!, purple hair, long hair, red eyes, mature", "alias": "kikuri"},
    {"tags": "1girl, gotoh hitori, bocchi the rock!, pink hair, blue eyes, shy", "alias": "bocchi"},
    {"tags": "1girl, kita ikuyo, bocchi the rock!, red hair, green eyes", "alias": "kita"},
    {"tags": "1girl, senjougahara hitagi, bakemonogatari, purple hair, sharp eyes", "alias": "hitagi"},
    {"tags": "1girl, oshino shinobu, bakemonogatari, blonde hair, yellow eyes, vampire", "alias": "shinobu"},
    {"tags": "1girl, osaki nana, nana, black hair, short hair, punk", "alias": "nana_o"},
    {"tags": "1girl, komatsu nana, nana, brown hair, long hair, brown eyes, cute", "alias": "hachi"},
    {"tags": "1girl, hirasawa yui, k-on!, brown hair, short hair, hairpin", "alias": "yui"},
    {"tags": "1girl, akiyama mio, k-on!, black hair, long hair, grey eyes", "alias": "mio"},
    {"tags": "1girl, frieren, sousou no frieren, white hair, elf ears, mage", "alias": "frieren"},
    {"tags": "1girl, tohsaka rin, fate stay night, black hair, twintails, aqua eyes", "alias": "rin"},
    {"tags": "1girl, saber, fate stay night, blonde hair, green eyes, ahoge", "alias": "saber"},
    {"tags": "1girl, suzumiya haruhi, suzumiya haruhi no yuuutsu, brown hair, hair ribbon", "alias": "haruhi"},
    {"tags": "1girl, rem, re:zero, blue hair, blue eyes, maid, x hair ornament", "alias": "rem"},
    {"tags": "1girl, zero two, darling in the franxx, pink hair, green eyes, horns", "alias": "zero_two"},
    {"tags": "1girl, megumin, konosuba, brown hair, red eyes, witch hat, eyepatch", "alias": "megumin"},
    {"tags": "1girl, yor briar, spy x family, black hair, red eyes, earrings, elegant", "alias": "yor"},
    {"tags": "1girl, kitagawa marin, sono bisque doll, blonde hair, brown eyes, gyaru", "alias": "marin"},
    {"tags": "1girl, nishikigi chisato, lycoris recoil, blonde hair, red eyes, hair ribbon", "alias": "chisato"},
    {"tags": "1girl, hatsune miku, vocaloid, aqua hair, twintails, aqua eyes, headset", "alias": "miku"},
    {"tags": "1girl, furina, genshin impact, blue hair, blue eyes, hat, top hat", "alias": "furina"},
    {"tags": "1girl, raiden shogun, genshin impact, purple hair, purple eyes, braid", "alias": "raiden"},
    {"tags": "1girl, akemi homura, mahou shoujo madoka magica, black hair, purple eyes, hairband", "alias": "homura"},
    {"tags": "1girl, shana, shakugan no shana, red hair, long hair, red eyes", "alias": "shana"},
    {"tags": "1girl, ayanami rei, neon genesis evangelion, blue hair, short hair, red eyes", "alias": "rei"},
    {"tags": "1girl, souryuu asuka langley, neon genesis evangelion, red hair, blue eyes", "alias": "asuka"},
    {"tags": "1girl, shinku, rozen maiden, blonde hair, twintails, red eyes, gothic lolita", "alias": "shinku"},
    {"tags": "1girl, kitashirakawa tamako, tamako market, black hair, short hair, brown eyes, cheerful", "alias": "tamako"},
    {"tags": "1girl, tokiwa midori, tamako market, green hair, short hair, glasses, shy", "alias": "midori"},
    {"tags": "1girl, makino kanna, tamako market, blonde hair, twintails, blue eyes", "alias": "kanna"},
    {"tags": "1girl, asagiri shiori, tamako market, purple hair, long hair, quiet", "alias": "shiori"},
]

BACKGROUNDS = [
    {"tags": "school, hallway, bright", "alias": "school"},
    {"tags": "cafe, indoors, warm light", "alias": "cafe"},
    {"tags": "cherry blossoms, outdoors, spring", "alias": "sakura"},
    {"tags": "sunset, golden hour, outdoors", "alias": "sunset"},
    {"tags": "purikura, photo booth, stickers, sparkles", "alias": "purikura"},
    {"tags": "selfie, phone camera, mirror", "alias": "selfie"},
    {"tags": "festival, summer, yukata", "alias": "matsuri"},
    {"tags": "convenience store, night, bright light", "alias": "konbini"},
    {"tags": "rooftop, blue sky, wind", "alias": "rooftop"},
    {"tags": "beach, summer, swimsuit", "alias": "beach"},
    {"tags": "classroom, after school, warm light", "alias": "classroom"},
    {"tags": "train station, platform, crowd", "alias": "station"},
    {"tags": "karaoke, neon, microphone", "alias": "karaoke"},
    {"tags": "park, bench, trees, sunny", "alias": "park"},
    {"tags": "arcade, game center, colorful lights", "alias": "arcade"},
]

TOTAL = 100

NEGATIVE = (
    "lowres, bad anatomy, error, text, signature, "
    "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, "
    "poorly drawn hands, wrong number of fingers, six fingers, four fingers, "
    "mutated hands, malformed hands, twisted fingers, interlocked fingers, "
    "extra digit, fewer digits, cropped fingers"
)


async def generate(client, idx, char, bg):
    prompt = (
        f"{char['tags']}, detailed hands, perfect fingers, v sign, peace sign, "
        f"gyaru pose, wink, {bg['tags']}, masterpiece, best quality"
    )
    filename = f"gyarupeace_{char['alias']}_{bg['alias']}"

    payload = {
        "prompt": prompt,
        "negative_prompt": NEGATIVE,
        "width": 832,
        "height": 1216,
        "style": PRESET,
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
            print(f"[{idx:03d}/{TOTAL}] OK {char['alias']}_{bg['alias']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:03d}/{TOTAL}] FAIL: {data.get('error', '?')}")
            return False
    except Exception as e:
        print(f"[{idx:03d}/{TOTAL}] ERROR: {e}")
        return False


async def main():
    jobs = []
    for _ in range(TOTAL):
        jobs.append((random.choice(CHARACTERS), random.choice(BACKGROUNDS)))
    random.shuffle(jobs)

    ok = fail = 0
    print(f"갸루피스 추가 배치 {TOTAL}장")
    print(f"캐릭터 {len(CHARACTERS)}명 / 배경 {len(BACKGROUNDS)}개")
    print(f"프리셋: {PRESET}")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, (char, bg) in enumerate(jobs, 1):
            if await generate(client, i, char, bg):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
