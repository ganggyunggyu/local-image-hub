"""발렌타인 x 인기 캐릭터 10장
조회수 노림수 냥~
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_valentine_popular"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 인기 캐릭터 정의
FRIEREN = "frieren, sousou no frieren, white hair, long hair, twintails, green eyes, elf ears, mage robe"
FERN = "fern, sousou no frieren, purple hair, long hair, twintails, purple eyes, mage robe"
ANYA = "anya forger, spy x family, pink hair, short hair, green eyes, black headband"
MAKIMA = "makima, chainsaw man, red hair, long hair, braided ponytail, yellow eyes, ringed eyes"
POWER = "power, chainsaw man, blonde hair, long hair, red horns, yellow eyes, sharp teeth"
MARIN = "kitagawa marin, sono bisque doll, blonde hair, long hair, pink eyes, gyaru"
CHISATO = "chisato nishikigi, lycoris recoil, blonde hair, bob cut, red eyes"
BOCCHI = "gotoh hitori, bocchi the rock!, pink hair, long hair, blue eyes, pink track jacket"
AI = "hoshino ai, oshi no ko, purple hair, long hair, star eyes, idol"
KAGUYA = "shinomiya kaguya, kaguya-sama, black hair, long hair, red eyes, ribbon"

NEG = "extra fingers, fused fingers, deformed hands, bad hands, bad anatomy, poorly drawn hands"

JOBS = [
    {"prompt": f"1girl, {FRIEREN}, valentine, chocolate box, heart, embarrassed, blushing, looking away, cute", "alias": "val_frieren"},
    {"prompt": f"1girl, {FERN}, valentine, holding chocolate, ribbon, shy, offering, heart background", "alias": "val_fern"},
    {"prompt": f"1girl, {ANYA}, valentine, heart shaped chocolate, excited, sparkling eyes, happy, waku waku", "alias": "val_anya"},
    {"prompt": f"1girl, {MAKIMA}, valentine, elegant, red dress, wine glass, seductive smile, roses", "alias": "val_makima"},
    {"prompt": f"1girl, {POWER}, valentine, messy chocolate, proud, boastful, homemade chocolate", "alias": "val_power"},
    {"prompt": f"1girl, {MARIN}, valentine, gyaru style, heart accessories, excited, love letter, cheerful", "alias": "val_marin"},
    {"prompt": f"1girl, {CHISATO}, valentine, cafe uniform, serving chocolate cake, smile, professional", "alias": "val_chisato"},
    {"prompt": f"1girl, {BOCCHI}, valentine, nervous, hiding behind chocolate box, blushing, trembling", "alias": "val_bocchi"},
    {"prompt": f"1girl, {AI}, valentine, idol costume, heart pose, wink, stage, sparkles, love", "alias": "val_ai"},
    {"prompt": f"1girl, {KAGUYA}, valentine, elegant, ojousama, wrapped chocolate, tsundere, looking away", "alias": "val_kaguya"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": job["prompt"],
        "negative_prompt": NEG,
        "width": 1024,
        "height": 1024,
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
            print(f"[{idx:02d}/{TOTAL}] OK {job['alias']} (seed: {seed})", flush=True)
            return True
        else:
            print(f"[{idx:02d}/{TOTAL}] FAIL {job['alias']}: {data.get('error', '?')}", flush=True)
            return False
    except Exception as e:
        print(f"[{idx:02d}/{TOTAL}] ERROR {job['alias']}: {e}", flush=True)
        return False


async def main():
    ok = fail = 0
    print("발렌타인 x 인기 캐릭터 10장", flush=True)
    print("프리렌/페른/아냐/마키마/파워/마린/치사토/봇치/아이/카구야", flush=True)
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
