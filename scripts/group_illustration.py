"""걸밴드 크로스오버 그룹샷 (20장)
케이온 x 봇치더락 x 걸즈밴드크라이
핵심: 다른 애니 캐릭터들이 한 프레임에 등장
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_girlband_xover"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === K-ON (けいおん！) - 방과후 티타임 ===
MIO = "black long hair, grey eyes"              # 아키야마 미오 - Bass/Vo, 쿨뷰티
RITSU = "brown short hair, yellow headband"      # 타이나카 리츠 - Drums, 보이시
YUI = "brown short hair, brown eyes, hairpin"    # 히라사와 유이 - Guitar/Vo, 에어헤드
MUGI = "blonde long hair, blue eyes, thick eyebrows"  # 코토부키 츠무기 - Key, 오죠사마
AZUSA = "black hair, twintails, red eyes"        # 나카노 아즈사 - Guitar, 츤데레

# === Bocchi the Rock (ぼっち・ざ・ろっく！) - 결속밴드 ===
BOCCHI = "pink long hair, blue eyes, pink jacket"   # 고토 히토리 - Guitar, 음침
NIJIKA = "blonde short hair, blue eyes, side braid" # 이지치 니지카 - Drums, 밝음
RYO = "blue long hair, red eyes, cool"              # 야마다 료 - Bass, 데드팬
KITA = "red long hair, green eyes, star hairpin"     # 키타 이쿠요 - Vo/Gt, 갸루

# === Girls Band Cry (ガールズバンドクライ) - 토게나시토게아리 ===
NINA = "black long hair, blue eyes, passionate"    # 이세리 니나 - Vo/Gt, 열혈
SUBARU = "silver short hair, purple eyes, cool"    # 아와 스바루 - Guitar, 쿨
TOMO = "brown short hair, green eyes, calm"        # 에바 토모 - Drums, 성숙
MOMOKA = "pink hair, twintails, brown eyes"        # 카와라기 모모카 - Bass, 쾌활

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    # ==========================================
    # 3애니 크로스오버 (각 애니 1명 이상 = 핵심)
    # ==========================================
    # 쿨뷰티 삼국지: 미오(K) x 료(B) x 스바루(G)
    {
        "prompt": f"3girls, multiple girls, {MIO}, {RYO}, {SUBARU}, casual clothes, standing together, arms crossed, cool, white background",
        "alias": "xo01_cool3",
        "style": "pop_fanart",
        "w": 1216, "h": 832,
    },
    # 드러머 삼국지: 리츠(K) x 니지카(B) x 토모(G)
    {
        "prompt": f"3girls, multiple girls, {RITSU}, {NIJIKA}, {TOMO}, drumsticks, peace sign, energetic, white background",
        "alias": "xo02_drum3",
        "style": "pop_fanart",
        "w": 1216, "h": 832,
    },
    # 겐키 삼국지: 유이(K) x 키타(B) x 니나(G)
    {
        "prompt": f"3girls, multiple girls, {YUI}, {KITA}, {NINA}, excited, arm raised, jumping, white background, cheerful",
        "alias": "xo03_genki3",
        "style": "pop_fanart",
        "w": 1216, "h": 832,
    },
    # 베이스 삼국지: 미오(K) x 료(B) x 모모카(G)
    {
        "prompt": f"3girls, multiple girls, {MIO} bass guitar, {RYO} bass guitar, {MOMOKA} bass guitar, stage, spotlight, cool",
        "alias": "xo04_bass3",
        "style": "mono_halftone",
        "w": 1216, "h": 832,
    },
    # 쿨 라인 카페: 미오(K) x 료(B) x 스바루(G)
    {
        "prompt": f"3girls, multiple girls, {MIO}, {RYO}, {SUBARU}, cafe, coffee, sitting, quiet, afternoon, relaxed",
        "alias": "xo05_cool_cafe",
        "style": "pale_aqua",
        "w": 1216, "h": 832,
    },
    # 겐키 라인 축제: 유이(K) x 키타(B) x 니나(G)
    {
        "prompt": f"3girls, multiple girls, {YUI}, {KITA}, {NINA}, yukata, summer festival, fireworks, sparklers, laughing",
        "alias": "xo06_genki_fest",
        "style": "kyoto_animation",
        "w": 1216, "h": 832,
    },
    # 오죠 라인: 츠무기(K) x 니지카(B) x 토모(G) - 안정/서포트
    {
        "prompt": f"3girls, multiple girls, {MUGI}, {NIJIKA}, {TOMO}, tea party, cake, smiling, warm light, cozy room",
        "alias": "xo07_support3",
        "style": "cozy_gouache",
        "w": 1216, "h": 832,
    },
    # 음침 x 열혈 x 에어헤드: 봇치(B) x 니나(G) x 유이(K)
    {
        "prompt": f"3girls, multiple girls, {BOCCHI} nervous, {NINA} passionate fist, {YUI} carefree smile, school corridor, standing, comedy",
        "alias": "xo08_contrast3",
        "style": "pop_fanart",
        "w": 1216, "h": 832,
    },
    # 츤데레 라인: 아즈사(K) x 료(B) x 스바루(G)
    {
        "prompt": f"3girls, multiple girls, {AZUSA}, {RYO}, {SUBARU}, annoyed expression, arms crossed, school, white background, tsundere",
        "alias": "xo09_tsun3",
        "style": "pop_fanart",
        "w": 1216, "h": 832,
    },
    # 셀카: 키타(B) x 니나(G) x 리츠(K)
    {
        "prompt": f"3girls, multiple girls, {KITA} holding phone selfie, {NINA} peace sign, {RITSU} arm around, close-up faces, white background",
        "alias": "xo10_selfie3",
        "style": "pop_fanart",
        "w": 1024, "h": 1024,
    },

    # ==========================================
    # 3애니 합동 그룹샷 (4인 이상)
    # ==========================================
    # 합동 라이브: 미오(K) + 료(B) + 니나(G) + 키타(B)
    {
        "prompt": f"4girls, multiple girls, {MIO} bass, {RYO} bass, {NINA} guitar singing, {KITA} guitar, stage, concert, spotlight",
        "alias": "xo11_joint_live",
        "style": "pale_aqua",
        "w": 1216, "h": 832,
    },
    # 합동 단체사진: 미오(K) + 봇치(B) + 니나(G) + 츠무기(K)
    {
        "prompt": f"4girls, multiple girls, {MIO}, {BOCCHI}, {NINA}, {MUGI}, group photo, cherry blossoms, spring, school, standing, smile",
        "alias": "xo12_group4",
        "style": "kyoto_animation",
        "w": 1216, "h": 832,
    },

    # ==========================================
    # 크로스오버 투샷 (다른 애니 캐릭 둘)
    # ==========================================
    # 미오(K) x 료(B): 베이스 쿨 대결
    {
        "prompt": f"2girls, multiple girls, girl on left {MIO} bass guitar, girl on right {RYO} bass guitar, back to back, rivalry, white background",
        "alias": "xo13_mio_ryo",
        "style": "pop_fanart",
        "w": 1024, "h": 1024,
    },
    # 봇치(B) x 미오(K): 수줍음 실력파
    {
        "prompt": f"2girls, multiple girls, {BOCCHI} nervous, {MIO} shy, bench, park, awkward, both looking away, cute",
        "alias": "xo14_shy_duo",
        "style": "pale_aqua",
        "w": 1024, "h": 1024,
    },
    # 니나(G) x 봇치(B): 정반대 대비
    {
        "prompt": f"2girls, multiple girls, girl on left {NINA} shouting passionate, girl on right {BOCCHI} scared cowering, stage, comedy",
        "alias": "xo15_fire_ice",
        "style": "pop_fanart",
        "w": 1024, "h": 1024,
    },
    # 키타(B) x 유이(K): 에어헤드 폭발
    {
        "prompt": f"2girls, multiple girls, {KITA} selfie pose peace sign, {YUI} eating cake, convenience store, night, fun",
        "alias": "xo16_airhead2",
        "style": "cozy_gouache",
        "w": 1024, "h": 1024,
    },
    # 스바루(G) x 아즈사(K): 진지한 기타리스트
    {
        "prompt": f"2girls, multiple girls, {SUBARU} electric guitar, {AZUSA} electric guitar, practice room, focused, serious, cool",
        "alias": "xo17_guitar_duo",
        "style": "pale_aqua",
        "w": 1024, "h": 1024,
    },
    # 리츠(K) x 니지카(B): 드러머 케미
    {
        "prompt": f"2girls, multiple girls, {RITSU} arm around shoulder, {NIJIKA} thumbs up, music room, drums, friendly, laughing",
        "alias": "xo18_drum_duo",
        "style": "kyoto_animation",
        "w": 1024, "h": 1024,
    },

    # ==========================================
    # 분위기 크로스오버
    # ==========================================
    # 쿨 라인 밤산책: 미오(K) x 료(B) x 스바루(G)
    {
        "prompt": f"3girls, multiple girls, {MIO}, {RYO}, {SUBARU}, night walk, city lights, quiet, streetlight, cool",
        "alias": "xo19_cool_night",
        "style": "shinkai",
        "w": 1216, "h": 832,
    },
    # 포스터: 미오(K) x 료(B) x 스바루(G)
    {
        "prompt": f"3girls, multiple girls, {MIO}, {RYO}, {SUBARU}, leather jacket, rooftop, city skyline, sunset, wind, cool",
        "alias": "xo20_poster",
        "style": "shinkai",
        "w": 832, "h": 1216,
    },
]

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
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} [{job['style']}] ({job['w']}x{job['h']}) (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print("걸밴드 크로스오버 일러스트", flush=True)
    print(f"총 {TOTAL}장", flush=True)
    print("K-ON: 미오(Bass) 리츠(Dr) 유이(Gt)", flush=True)
    print("봇치: 봇치(Gt) 니지카(Dr) 료(Bass) 키타(Vo)", flush=True)
    print("GBC: 니나(Vo) 스바루(Gt) 토모(Dr)", flush=True)
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
