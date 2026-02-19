"""pale_aqua v2 테스트 30장 - 개선된 프리셋"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pale_aqua_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    # 케이온
    {"prompt": "1girl, hirasawa yui, k-on!, brown hair, cheerful, guitar, upper body", "name": "yui"},
    {"prompt": "1girl, akiyama mio, k-on!, black long hair, shy, upper body", "name": "mio"},
    {"prompt": "1girl, tainaka ritsu, k-on!, light brown hair, headband, energetic, upper body", "name": "ritsu"},

    # 봇치더락
    {"prompt": "1girl, gotoh hitori, bocchi the rock!, pink hair, anxious, guitar, upper body", "name": "bocchi"},
    {"prompt": "1girl, kita ikuyo, bocchi the rock!, red hair, bright smile, upper body", "name": "kita"},

    # 프리렌
    {"prompt": "1girl, frieren, sousou no frieren, white hair, elf ears, calm, upper body", "name": "frieren"},
    {"prompt": "1girl, fern, sousou no frieren, purple hair, twintails, gentle, upper body", "name": "fern"},

    # 보컬로이드
    {"prompt": "1girl, hatsune miku, vocaloid, twintails, aqua hair, smile, upper body", "name": "miku"},
    {"prompt": "1girl, luka megurine, vocaloid, pink hair, elegant, upper body", "name": "luka"},

    # 블루 아카이브
    {"prompt": "1girl, shiroko, blue archive, white hair, blue eyes, halo, upper body", "name": "shiroko"},
    {"prompt": "1girl, arona, blue archive, blue hair, halo, cheerful, upper body", "name": "arona"},

    # 원신
    {"prompt": "1girl, ganyu, genshin impact, blue hair, horns, gentle, upper body", "name": "ganyu"},
    {"prompt": "1girl, ayaka, genshin impact, light blue hair, graceful, upper body", "name": "ayaka"},
    {"prompt": "1girl, furina, genshin impact, multicolored hair, noble, upper body", "name": "furina"},

    # 모노가타리
    {"prompt": "1girl, senjougahara hitagi, monogatari, purple hair, sharp eyes, elegant, upper body", "name": "hitagi"},
    {"prompt": "1girl, hanekawa tsubasa, monogatari, black hair, braids, gentle, upper body", "name": "hanekawa"},

    # 바이올렛 에버가든
    {"prompt": "1girl, violet evergarden, blonde hair, blue eyes, stoic, upper body", "name": "violet"},

    # 리코리스 리코일
    {"prompt": "1girl, takina inoue, lycoris recoil, black hair, serious, upper body", "name": "takina"},
    {"prompt": "1girl, chisato nishikigi, lycoris recoil, blonde hair, smile, upper body", "name": "chisato"},

    # 귀멸의 칼날
    {"prompt": "1girl, kochou shinobu, kimetsu no yaiba, butterfly hairpin, gentle smile, upper body", "name": "shinobu"},
    {"prompt": "1girl, nezuko kamado, kimetsu no yaiba, pink eyes, cute, upper body", "name": "nezuko"},

    # 냥냥돌쇠
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, smile, upper body", "name": "dolsoe_smile"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, reading, cozy", "name": "dolsoe_read"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, head tilt, curious", "name": "dolsoe_curious"},

    # 다양한 오리지널
    {"prompt": "1girl, white hair, blue eyes, elf ears, serene, flowers, upper body", "name": "elf_serene"},
    {"prompt": "1girl, light blue hair, sailor uniform, shy, blushing, upper body", "name": "sailor_shy"},
    {"prompt": "1girl, lavender hair, gentle, magic, upper body", "name": "lavender_magic"},
    {"prompt": "1girl, silver hair, red eyes, elegant, mysterious, upper body", "name": "silver_elegant"},
    {"prompt": "1girl, blonde hair, twintails, ribbon, innocent, upper body", "name": "twin_innocent"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{job['prompt']}, masterpiece",
        "negative_prompt": "low quality, worst quality",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": "pale_aqua",
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
    print(f"pale_aqua v2 테스트 {TOTAL}장 (개선버전)")
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
