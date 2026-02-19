"""모노가타리 스타일 다양한 캐릭터 50장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_various"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    # 모노가타리 시리즈
    {"prompt": "1girl, senjougahara hitagi, monogatari, purple hair, sharp eyes, head tilt, elegant, upper body", "name": "hitagi"},
    {"prompt": "1girl, hanekawa tsubasa, monogatari, black hair, braids, glasses, gentle, upper body", "name": "hanekawa"},
    {"prompt": "1girl, black hanekawa, monogatari, white hair, cat ears, yellow eyes, smirk, upper body", "name": "black_hanekawa"},
    {"prompt": "1girl, shinobu oshino, monogatari, blonde hair, golden eyes, mysterious, upper body", "name": "shinobu"},
    {"prompt": "1girl, nadeko sengoku, monogatari, orange hair, shy, bangs over eyes, upper body", "name": "nadeko"},
    {"prompt": "1girl, suruga kanbaru, monogatari, short dark hair, athletic, confident, upper body", "name": "kanbaru"},
    {"prompt": "1girl, mayoi hachikuji, monogatari, twintails, backpack, cheerful, upper body", "name": "hachikuji"},

    # 프리렌
    {"prompt": "1girl, frieren, sousou no frieren, white hair, elf ears, calm, staff, upper body", "name": "frieren"},
    {"prompt": "1girl, fern, sousou no frieren, purple hair, twintails, determined, upper body", "name": "fern"},

    # 보컬로이드
    {"prompt": "1girl, hatsune miku, vocaloid, twintails, aqua hair, smile, upper body", "name": "miku"},
    {"prompt": "1girl, luka megurine, vocaloid, pink long hair, elegant, upper body", "name": "luka"},

    # 원신
    {"prompt": "1girl, raiden shogun, genshin impact, purple hair, elegant, serious, upper body", "name": "raiden"},
    {"prompt": "1girl, keqing, genshin impact, purple twintails, confident, upper body", "name": "keqing"},
    {"prompt": "1girl, ganyu, genshin impact, blue hair, horns, gentle, upper body", "name": "ganyu"},
    {"prompt": "1girl, furina, genshin impact, multicolored hair, noble, dramatic, upper body", "name": "furina"},
    {"prompt": "1girl, nahida, genshin impact, white hair, green eyes, small, wise, upper body", "name": "nahida"},

    # 블루 아카이브
    {"prompt": "1girl, shiroko, blue archive, white hair, blue eyes, halo, calm, upper body", "name": "shiroko"},
    {"prompt": "1girl, arona, blue archive, blue hair, halo, cheerful, upper body", "name": "arona"},

    # 귀멸의 칼날
    {"prompt": "1girl, kochou shinobu, kimetsu no yaiba, butterfly hairpin, gentle smile, upper body", "name": "shinobu_k"},
    {"prompt": "1girl, nezuko kamado, kimetsu no yaiba, bamboo, pink eyes, cute, upper body", "name": "nezuko"},

    # 스파이 패밀리
    {"prompt": "1girl, yor forger, spy x family, black hair, red eyes, elegant, upper body", "name": "yor"},
    {"prompt": "1girl, anya forger, spy x family, pink hair, green eyes, smug, upper body", "name": "anya"},

    # 봇치더락
    {"prompt": "1girl, gotoh hitori, bocchi the rock!, pink hair, anxious, guitar, upper body", "name": "bocchi"},
    {"prompt": "1girl, kita ikuyo, bocchi the rock!, red hair, bright smile, energetic, upper body", "name": "kita"},
    {"prompt": "1girl, ryo yamada, bocchi the rock!, blue hair, cool, bass, upper body", "name": "ryo"},

    # 체인소맨
    {"prompt": "1girl, makima, chainsaw man, red hair, yellow eyes, mysterious, upper body", "name": "makima"},
    {"prompt": "1girl, power, chainsaw man, blonde hair, horns, chaotic, upper body", "name": "power"},
    {"prompt": "1girl, reze, chainsaw man, dark hair, cute, mysterious, upper body", "name": "reze"},

    # NANA
    {"prompt": "1girl, oosaki nana, nana (anime), short black hair, punk, cool, cigarette, upper body", "name": "nana_o"},
    {"prompt": "1girl, serizawa reira, layla, nana (anime), blonde hair, elegant, singing, upper body", "name": "layla"},

    # 걸밴크라이
    {"prompt": "1girl, nina, girls band cry, short blonde hair, red eyes, confident, upper body", "name": "nina"},
    {"prompt": "1girl, momoka, girls band cry, pink hair, twintails, cheerful, guitar, upper body", "name": "momoka"},

    # 바이올렛 에버가든
    {"prompt": "1girl, violet evergarden, blonde hair, blue eyes, stoic, brooch, upper body", "name": "violet"},

    # 리코리스 리코일
    {"prompt": "1girl, takina inoue, lycoris recoil, black hair, serious, cool, upper body", "name": "takina"},
    {"prompt": "1girl, chisato nishikigi, lycoris recoil, blonde hair, red eyes, cheerful, upper body", "name": "chisato"},

    # 케이온
    {"prompt": "1girl, akiyama mio, k-on!, black long hair, shy, bass, upper body", "name": "mio"},
    {"prompt": "1girl, hirasawa yui, k-on!, brown hair, cheerful, guitar, upper body", "name": "yui"},

    # 냥냥돌쇠
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, head tilt, smirk, upper body", "name": "dolsoe_smirk"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, mysterious, elegant, upper body", "name": "dolsoe_elegant"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, cool, confident, upper body", "name": "dolsoe_cool"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, playful, wink, upper body", "name": "dolsoe_wink"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, reading, focused, upper body", "name": "dolsoe_read"},

    # 추가
    {"prompt": "1girl, rem, re:zero, blue hair, maid, gentle smile, upper body", "name": "rem"},
    {"prompt": "1girl, emilia, re:zero, silver hair, elf ears, kind, upper body", "name": "emilia"},
    {"prompt": "1girl, zero two, darling in the franxx, pink hair, horns, confident, upper body", "name": "zerotwo"},
    {"prompt": "1girl, asuka langley, evangelion, red hair, plugsuit, fierce, upper body", "name": "asuka"},
    {"prompt": "1girl, rei ayanami, evangelion, blue hair, red eyes, stoic, upper body", "name": "rei"},
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
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['name']}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"모노가타리 스타일 다양한 캐릭터 {TOTAL}장")
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
