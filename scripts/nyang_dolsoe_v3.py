"""냥냥돌쇠 캐릭터 디자인 v3 - 신규 10타입 (E~N)"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_nyang_dolsoe_v3"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHAR = {
    # 크림슨 트윈테 오드아이 보이시
    "E": "1girl, cat ears, cat tail, crimson hair, twin tails, heterochromia, red eye, gold eye, fang, bandana, tomboyish",
    # 백금발 롱헤어 보라눈 점 우아
    "F": "1girl, cat ears, cat tail, platinum blonde hair, very long hair, violet eyes, beauty mark on lip, elegant, mature",
    # 오렌지 하이포니 갈색눈 건강미
    "G": "1girl, cat ears, cat tail, orange hair, high ponytail, brown eyes, tanned skin, sporty, wristband",
    # 민트 웨이브 핑크눈 안경 문학소녀
    "H": "1girl, cat ears, cat tail, mint green hair, wavy hair, medium hair, pink eyes, round glasses, bookish",
    # 금발 롤컬 적안 고딕인형
    "I": "1girl, cat ears, cat tail, blonde hair, ringlet curls, red eyes, doll-like, cross hair clip, porcelain skin",
    # 보라 비대칭 금안 피어싱 펑크
    "J": "1girl, cat ears, cat tail, purple hair, asymmetrical hair, one side long, yellow eyes, ear piercing, rebellious",
    # 카라멜 플러피 헤이즐 보조개 온화
    "K": "1girl, cat ears, cat tail, light brown hair, fluffy hair, shoulder length hair, hazel eyes, dimples, gentle expression",
    # 회백발 스트레이트 빙결안 무표정 붕대
    "L": "1girl, cat ears, cat tail, ash gray hair, straight hair, very long hair, ice blue eyes, stoic, bandaged hands",
    # 딸기금발 쌍꽈배기 터콰이즈 별핀 겐키
    "M": "1girl, cat ears, cat tail, strawberry blonde hair, twin braids, turquoise eyes, star hair clip, cheerful, genki",
    # 틸그린 하이포니 주황눈 흉터 전사
    "N": "1girl, cat ears, cat tail, teal hair, high ponytail, orange eyes, scar on cheek, fierce, warrior",
}

JOBS = [
    # E: 크림슨 트윈테 오드아이
    {
        "prompt": f"{CHAR['E']}, oversized hoodie, headphones around neck, skateboard, street, sunset, wind, looking at viewer, upper body",
        "alias": "E1_street",
    },
    # F: 백금발 우아
    {
        "prompt": f"{CHAR['F']}, evening dress, wine glass, balcony, night city view, moonlight, arms behind back, looking over shoulder, upper body",
        "alias": "F1_evening",
    },
    # G: 오렌지 건강미
    {
        "prompt": f"{CHAR['G']}, volleyball uniform, jumping, gymnasium, dynamic pose, determined, daytime, sweat, upper body",
        "alias": "G1_volleyball",
    },
    # H: 민트 안경 문학소녀
    {
        "prompt": f"{CHAR['H']}, cardigan, hugging book to chest, library, sitting by window, afternoon light, gentle smile, face close-up",
        "alias": "H1_library",
    },
    # I: 금발 고딕인형
    {
        "prompt": f"{CHAR['I']}, gothic lolita dress, black and red, sitting on throne, dark room, candles, roses, looking at viewer, upper body",
        "alias": "I1_gothic",
    },
    # J: 보라 펑크
    {
        "prompt": f"{CHAR['J']}, leather jacket, ripped jeans, electric guitar, live house, spotlight, smirk, looking at viewer, upper body",
        "alias": "J1_punk",
    },
    # K: 카라멜 온화
    {
        "prompt": f"{CHAR['K']}, apron, kitchen, mixing bowl, flour on cheek, warm light, happy, looking at viewer, upper body",
        "alias": "K1_baking",
    },
    # L: 회백발 무표정
    {
        "prompt": f"{CHAR['L']}, black cloak, arms crossed, ruins, fog, dramatic lighting, wind, hair blowing, looking at viewer, upper body",
        "alias": "L1_ruins",
    },
    # M: 딸기금발 겐키
    {
        "prompt": f"{CHAR['M']}, idol costume, stage, colorful lights, peace sign, wink, sparkles, energetic, face close-up",
        "alias": "M1_idol",
    },
    # N: 틸그린 전사
    {
        "prompt": f"{CHAR['N']}, armor, shoulder guard, sword on back, mountain cliff, wind, sunrise, confident, looking at viewer, upper body",
        "alias": "N1_warrior",
    },
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": "",
        "width": 832,
        "height": 1216,
        "model": "animagine-xl-4",
        "style": "pale_aqua",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=600.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['alias']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} (seed: {seed})")
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}")
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"냥냥돌쇠 신규 타입 테스트 {TOTAL}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)
    print("E: 크림슨 트윈테 오드아이 보이시")
    print("F: 백금발 롱헤어 보라눈 우아")
    print("G: 오렌지 하이포니 갈색눈 건강미")
    print("H: 민트 웨이브 핑크눈 안경 문학소녀")
    print("I: 금발 롤컬 적안 고딕인형")
    print("J: 보라 비대칭 금안 피어싱 펑크")
    print("K: 카라멜 플러피 헤이즐 보조개 온화")
    print("L: 회백발 스트레이트 빙결안 무표정")
    print("M: 딸기금발 쌍꽈배기 터콰이즈 겐키")
    print("N: 틸그린 하이포니 주황눈 전사")
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
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
