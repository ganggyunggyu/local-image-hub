"""pale_aqua 스타일 테스트 50장 - 다양한 캐릭터"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pale_aqua_50"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# pale_aqua에 어울리는 캐릭터들 - 청순/차분/블루톤 계열
JOBS = [
    # 프리렌 캐릭터
    {"prompt": "1girl, frieren, sousou no frieren, white hair, elf ears, green eyes, calm, upper body", "name": "frieren_calm"},
    {"prompt": "1girl, frieren, sousou no frieren, white hair, reading book, peaceful", "name": "frieren_read"},
    {"prompt": "1girl, fern, sousou no frieren, purple hair, twintails, gentle smile, upper body", "name": "fern_gentle"},

    # 보컬로이드
    {"prompt": "1girl, hatsune miku, vocaloid, twintails, aqua hair, aqua eyes, smile, upper body", "name": "miku_smile"},
    {"prompt": "1girl, hatsune miku, vocaloid, twintails, aqua hair, singing, side view", "name": "miku_sing"},
    {"prompt": "1girl, luka megurine, vocaloid, pink hair, long hair, elegant, upper body", "name": "luka_elegant"},

    # 레이/아야나미 계열
    {"prompt": "1girl, ayanami rei, evangelion, blue hair, short hair, red eyes, stoic, upper body", "name": "rei_stoic"},
    {"prompt": "1girl, ayanami rei, evangelion, school uniform, looking away, melancholic", "name": "rei_school"},

    # 블루 아카이브
    {"prompt": "1girl, shiroko, blue archive, white hair, blue eyes, halo, gentle, upper body", "name": "shiroko_gentle"},
    {"prompt": "1girl, hoshino, blue archive, pink hair, tired eyes, relaxed, upper body", "name": "hoshino_relax"},
    {"prompt": "1girl, arona, blue archive, blue hair, halo, cheerful, upper body", "name": "arona_cheer"},

    # 리코리스 리코일
    {"prompt": "1girl, takina inoue, lycoris recoil, black hair, long hair, serious, upper body", "name": "takina_serious"},
    {"prompt": "1girl, chisato nishikigi, lycoris recoil, blonde hair, red eyes, smile, upper body", "name": "chisato_smile"},

    # 모노가타리
    {"prompt": "1girl, senjougahara hitagi, monogatari, purple hair, sharp eyes, elegant, upper body", "name": "hitagi_elegant"},
    {"prompt": "1girl, hanekawa tsubasa, monogatari, black hair, braids, glasses, gentle, upper body", "name": "hanekawa_gentle"},
    {"prompt": "1girl, shinobu oshino, monogatari, blonde hair, golden eyes, mysterious, upper body", "name": "shinobu_mystery"},

    # 바이올렛 에버가든
    {"prompt": "1girl, violet evergarden, blonde hair, blue eyes, brooch, stoic, upper body", "name": "violet_stoic"},
    {"prompt": "1girl, violet evergarden, blonde hair, writing, peaceful, side view", "name": "violet_write"},

    # 스파이 패밀리
    {"prompt": "1girl, yor forger, spy x family, black hair, red eyes, elegant, upper body", "name": "yor_elegant"},
    {"prompt": "1girl, anya forger, spy x family, pink hair, green eyes, curious, upper body", "name": "anya_curious"},

    # 귀멸의 칼날
    {"prompt": "1girl, kochou shinobu, kimetsu no yaiba, butterfly hairpin, gentle smile, upper body", "name": "shinobu_gentle"},
    {"prompt": "1girl, nezuko kamado, kimetsu no yaiba, bamboo, pink eyes, cute, upper body", "name": "nezuko_cute"},

    # 주술회전
    {"prompt": "1girl, nobara kugisaki, jujutsu kaisen, orange hair, confident, upper body", "name": "nobara_conf"},

    # 원신
    {"prompt": "1girl, ganyu, genshin impact, blue hair, horns, gentle, upper body", "name": "ganyu_gentle"},
    {"prompt": "1girl, keqing, genshin impact, purple twintails, elegant, upper body", "name": "keqing_elegant"},
    {"prompt": "1girl, ayaka, genshin impact, light blue hair, graceful, upper body", "name": "ayaka_grace"},
    {"prompt": "1girl, furina, genshin impact, blue eyes, multicolored hair, noble, upper body", "name": "furina_noble"},

    # 명일방주
    {"prompt": "1girl, amiya, arknights, brown hair, bunny ears, determined, upper body", "name": "amiya_determ"},
    {"prompt": "1girl, texas, arknights, grey hair, wolf ears, cool, upper body", "name": "texas_cool"},

    # 케이온
    {"prompt": "1girl, akiyama mio, k-on!, black long hair, shy, bass guitar, upper body", "name": "mio_shy"},
    {"prompt": "1girl, hirasawa yui, k-on!, brown hair, cheerful, guitar, upper body", "name": "yui_cheer"},

    # 봇치더락
    {"prompt": "1girl, gotoh hitori, bocchi the rock!, pink hair, anxious, guitar, upper body", "name": "bocchi_anxious"},
    {"prompt": "1girl, kita ikuyo, bocchi the rock!, red hair, bright smile, upper body", "name": "kita_bright"},

    # 러브라이브
    {"prompt": "1girl, nishikino maki, love live!, red hair, tsundere, upper body", "name": "maki_tsun"},
    {"prompt": "1girl, sonoda umi, love live!, blue hair, serious, elegant, upper body", "name": "umi_serious"},

    # 냥냥돌쇠 (기본 캐릭터)
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, smile, upper body", "name": "dolsoe_smile"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, reading, cozy", "name": "dolsoe_read"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, looking at viewer, gentle", "name": "dolsoe_gentle"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, head tilt, curious", "name": "dolsoe_curious"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, sleepy, yawn", "name": "dolsoe_sleepy"},

    # 다양한 포즈/표정 추가
    {"prompt": "1girl, white hair, blue eyes, elf ears, serene, flowers, upper body", "name": "elf_serene"},
    {"prompt": "1girl, silver hair, red eyes, vampire, elegant, mysterious, upper body", "name": "vamp_elegant"},
    {"prompt": "1girl, light blue hair, sailor uniform, shy, blushing, upper body", "name": "sailor_shy"},
    {"prompt": "1girl, lavender hair, witch hat, gentle, magic, upper body", "name": "witch_gentle"},
    {"prompt": "1girl, mint green hair, maid, cheerful, serving, upper body", "name": "maid_cheer"},
    {"prompt": "1girl, pink hair, nurse, caring, gentle smile, upper body", "name": "nurse_caring"},
    {"prompt": "1girl, blonde hair, twintails, ribbon, innocent, upper body", "name": "twin_innocent"},
    {"prompt": "1girl, black hair, ponytail, kendo, serious, upper body", "name": "kendo_serious"},
    {"prompt": "1girl, brown hair, glasses, bookworm, reading, focused", "name": "bookworm_focus"},
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
    print(f"pale_aqua 스타일 테스트 {TOTAL}장")
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
