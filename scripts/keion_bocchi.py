"""케이온 & 봇치더락 배치 (50장)
호카고티타임 + 결속밴드
단체샷 포함
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_keion_bocchi"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 케이온 호카고티타임
YUI = "hirasawa yui, k-on!, brown hair, short hair, brown eyes, hairclip"
MIO = "akiyama mio, k-on!, black hair, long hair, grey eyes"
RITSU = "tainaka ritsu, k-on!, brown hair, short hair, headband, yellow eyes"
MUGI = "kotobuki tsumugi, k-on!, blonde hair, long hair, blue eyes, thick eyebrows"
AZUSA = "nakano azusa, k-on!, black hair, twintails, red eyes"

# 봇치더락 결속밴드
BOCCHI = "gotoh hitori, bocchi the rock!, pink hair, long hair, blue eyes"
NIJIKA = "ijichi nijika, bocchi the rock!, blonde hair, short hair, blue eyes, side braid"
RYO = "yamada ryo, bocchi the rock!, blue hair, long hair, red eyes"
KITA = "kita ikuyo, bocchi the rock!, red hair, long hair, green eyes, star hair ornament"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

# 위치 태그
L = "girl on left"
C = "girl in center"
R = "girl on right"

JOBS = [
    # === 케이온 솔로 10장 ===
    {"prompt": f"1girl, {YUI}, guitar, school uniform, classroom, happy", "alias": "keion_yui_01"},
    {"prompt": f"1girl, {YUI}, casual clothes, eating cake, cafe, smile", "alias": "keion_yui_02"},
    {"prompt": f"1girl, {MIO}, bass guitar, stage, spotlight, cool", "alias": "keion_mio_01"},
    {"prompt": f"1girl, {MIO}, school uniform, library, reading, shy", "alias": "keion_mio_02"},
    {"prompt": f"1girl, {RITSU}, drumsticks, energetic, music room", "alias": "keion_ritsu_01"},
    {"prompt": f"1girl, {RITSU}, casual clothes, peace sign, genki", "alias": "keion_ritsu_02"},
    {"prompt": f"1girl, {MUGI}, keyboard, elegant, music room, smiling", "alias": "keion_mugi_01"},
    {"prompt": f"1girl, {MUGI}, tea set, cake, ojousama, happy", "alias": "keion_mugi_02"},
    {"prompt": f"1girl, {AZUSA}, guitar, serious, practicing, music room", "alias": "keion_azusa_01"},
    {"prompt": f"1girl, {AZUSA}, cat ears, embarrassed, cute", "alias": "keion_azusa_02"},

    # === 봇치더락 솔로 10장 ===
    {"prompt": f"1girl, {BOCCHI}, guitar, closet, hiding, nervous", "alias": "bocchi_hitori_01"},
    {"prompt": f"1girl, {BOCCHI}, stage, spotlight, playing guitar, focused", "alias": "bocchi_hitori_02"},
    {"prompt": f"1girl, {NIJIKA}, drumsticks, energetic, live house, smile", "alias": "bocchi_nijika_01"},
    {"prompt": f"1girl, {NIJIKA}, casual clothes, starry, cheerful", "alias": "bocchi_nijika_02"},
    {"prompt": f"1girl, {RYO}, bass guitar, cool, standing, stoic", "alias": "bocchi_ryo_01"},
    {"prompt": f"1girl, {RYO}, eating, curry, happy, rare smile", "alias": "bocchi_ryo_02"},
    {"prompt": f"1girl, {KITA}, guitar, cheerful, energetic, peace sign", "alias": "bocchi_kita_01"},
    {"prompt": f"1girl, {KITA}, school uniform, happy, gyaru", "alias": "bocchi_kita_02"},
    {"prompt": f"1girl, {BOCCHI}, pink track jacket, nervous, looking away", "alias": "bocchi_hitori_03"},
    {"prompt": f"1girl, {KITA}, hugging {BOCCHI}, comedy, school", "alias": "bocchi_kitabochi"},

    # === 케이온 단체샷 10장 ===
    {"prompt": f"5girls, multiple girls, {YUI}, {MIO}, {RITSU}, {MUGI}, {AZUSA}, band, stage, concert, instruments, houkago tea time", "alias": "keion_group_01", "w": 1216, "h": 832},
    {"prompt": f"5girls, multiple girls, {YUI}, {MIO}, {RITSU}, {MUGI}, {AZUSA}, school uniform, music room, tea time", "alias": "keion_group_02", "w": 1216, "h": 832},
    {"prompt": f"5girls, multiple girls, {YUI}, {MIO}, {RITSU}, {MUGI}, {AZUSA}, casual clothes, group photo, smile", "alias": "keion_group_03", "w": 1216, "h": 832},
    {"prompt": f"5girls, multiple girls, {YUI}, {MIO}, {RITSU}, {MUGI}, {AZUSA}, summer, beach, swimsuit, happy", "alias": "keion_group_04", "w": 1216, "h": 832},
    {"prompt": f"5girls, multiple girls, {YUI}, {MIO}, {RITSU}, {MUGI}, {AZUSA}, winter, christmas, santa costume", "alias": "keion_group_05", "w": 1216, "h": 832},
    {"prompt": f"2girls, {L} {YUI} guitar, {R} {AZUSA} guitar, music room, practicing together", "alias": "keion_yuiazu", "w": 1216, "h": 832},
    {"prompt": f"2girls, {L} {MIO} shy, {R} {RITSU} teasing, comedy, school", "alias": "keion_mioritsu", "w": 1216, "h": 832},
    {"prompt": f"3girls, {L} {YUI}, {C} {MIO}, {R} {MUGI}, tea time, cake, happy", "alias": "keion_trio", "w": 1216, "h": 832},
    {"prompt": f"4girls, {YUI}, {MIO}, {RITSU}, {MUGI}, graduation, cherry blossoms, emotional", "alias": "keion_grad", "w": 1216, "h": 832},
    {"prompt": f"5girls, {YUI}, {MIO}, {RITSU}, {MUGI}, {AZUSA}, fuwa fuwa time, stage, spotlight", "alias": "keion_fuwafuwa", "w": 1216, "h": 832},

    # === 봇치더락 단체샷 10장 ===
    {"prompt": f"4girls, multiple girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, band, stage, concert, kessoku band", "alias": "bocchi_group_01", "w": 1216, "h": 832},
    {"prompt": f"4girls, multiple girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, starry, live house, backstage", "alias": "bocchi_group_02", "w": 1216, "h": 832},
    {"prompt": f"4girls, multiple girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, school uniform, group photo", "alias": "bocchi_group_03", "w": 1216, "h": 832},
    {"prompt": f"4girls, multiple girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, casual clothes, cafe, hanging out", "alias": "bocchi_group_04", "w": 1216, "h": 832},
    {"prompt": f"4girls, multiple girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, summer, festival, yukata", "alias": "bocchi_group_05", "w": 1216, "h": 832},
    {"prompt": f"2girls, {L} {BOCCHI} nervous, {R} {RYO} stoic, awkward, comedy", "alias": "bocchi_hitoriryo", "w": 1216, "h": 832},
    {"prompt": f"2girls, {L} {NIJIKA} happy, {R} {KITA} energetic, best friends", "alias": "bocchi_nijikita", "w": 1216, "h": 832},
    {"prompt": f"3girls, {L} {NIJIKA}, {C} {BOCCHI}, {R} {KITA}, starry, group hug", "alias": "bocchi_trio", "w": 1216, "h": 832},
    {"prompt": f"4girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, rooftop, sunset, wind", "alias": "bocchi_sunset", "w": 1216, "h": 832},
    {"prompt": f"4girls, {BOCCHI}, {NIJIKA}, {RYO}, {KITA}, practice, music studio, focused", "alias": "bocchi_practice", "w": 1216, "h": 832},

    # === 크로스오버 10장 ===
    {"prompt": f"2girls, {L} {YUI} guitar, {R} {BOCCHI} guitar, meeting, surprised, crossover", "alias": "cross_yuibocchi", "w": 1216, "h": 832},
    {"prompt": f"2girls, {L} {MIO} bass, {R} {RYO} bass, cool, stoic, crossover", "alias": "cross_mioryo", "w": 1216, "h": 832},
    {"prompt": f"2girls, {L} {AZUSA}, {R} {KITA}, guitar talk, excited, crossover", "alias": "cross_azukita", "w": 1216, "h": 832},
    {"prompt": f"2girls, {L} {RITSU} drums, {R} {NIJIKA} drums, energetic, crossover", "alias": "cross_ritsuniji", "w": 1216, "h": 832},
    {"prompt": f"2girls, {L} {MUGI} keyboard, {R} {BOCCHI} shy, tea time, crossover", "alias": "cross_mugibocchi", "w": 1216, "h": 832},
    {"prompt": f"4girls, {YUI}, {MIO}, {BOCCHI}, {RYO}, jam session, music studio, crossover", "alias": "cross_jam", "w": 1216, "h": 832},
    {"prompt": f"4girls, {AZUSA}, {RITSU}, {KITA}, {NIJIKA}, energetic, genki, crossover", "alias": "cross_genki", "w": 1216, "h": 832},
    {"prompt": f"6girls, {YUI}, {MIO}, {RITSU}, {BOCCHI}, {RYO}, {KITA}, group photo, crossover, smile", "alias": "cross_photo", "w": 1216, "h": 832},
    {"prompt": f"8girls, houkago tea time, kessoku band, joint concert, stage, epic, crossover", "alias": "cross_concert", "w": 1216, "h": 832},
    {"prompt": f"4girls, {YUI}, {BOCCHI}, {AZUSA}, {KITA}, guitar circle, jam session, happy, crossover", "alias": "cross_guitar", "w": 1216, "h": 832},
]

# 스타일 기본값 추가
for job in JOBS:
    if "style" not in job:
        job["style"] = "pale_aqua"
    if "w" not in job:
        job["w"] = 832
        job["h"] = 1216

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": job["w"],
        "height": job["h"],
        "model": "animagine-xl-4",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} [{job['style']}] (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print("케이온 & 봇치더락 배치 50장", flush=True)
    print("호카고티타임 + 결속밴드 + 크로스오버", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)
    print("=" * 60, flush=True)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60, flush=True)
    print(f"완료! 성공: {ok}, 실패: {fail}", flush=True)
    print(f"저장: {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
