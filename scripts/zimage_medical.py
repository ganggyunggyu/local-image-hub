"""
Z-Image Turbo - 위고비 / 스마일라식 / 브로멜라인 각 5장
"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_zimage_medical"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    # 위고비 (Wegovy) - 다이어트 주사
    {"prompt": "Wegovy semaglutide injection pen on clean white surface, medical product photography, soft lighting", "alias": "wegovy_product"},
    {"prompt": "person holding Wegovy injection pen, lifestyle shot, modern kitchen background, healthy living", "alias": "wegovy_lifestyle"},
    {"prompt": "Wegovy pen with measuring tape and fresh vegetables, weight loss concept, bright studio", "alias": "wegovy_diet"},
    {"prompt": "doctor explaining injection pen to patient, medical consultation, warm professional office", "alias": "wegovy_consult"},
    {"prompt": "flat lay of Wegovy pen with fitness gear, running shoes, water bottle, healthy lifestyle concept", "alias": "wegovy_flatlay"},

    # 스마일라식 (SMILE eye surgery)
    {"prompt": "ophthalmologist performing SMILE laser eye surgery, modern clinic, blue surgical light, professional", "alias": "smile_surgery"},
    {"prompt": "woman smiling after eye surgery, no glasses, clear vision concept, bright sunny outdoor", "alias": "smile_after"},
    {"prompt": "close-up of human eye with laser beam overlay, SMILE procedure visualization, medical tech", "alias": "smile_laser"},
    {"prompt": "modern eye clinic interior, high-tech equipment, clean white, futuristic medical facility", "alias": "smile_clinic"},
    {"prompt": "before and after concept, glasses on one side, free eyes on other, split composition, clear vision", "alias": "smile_before_after"},

    # 브로멜라인 (Bromelain)
    {"prompt": "fresh pineapple sliced open with supplement capsules, natural enzyme concept, bright studio", "alias": "bromelain_pineapple"},
    {"prompt": "bromelain supplement bottle with pineapple fruit, product photography, clean background", "alias": "bromelain_product"},
    {"prompt": "golden capsules scattered on wooden surface, natural supplement, warm morning light", "alias": "bromelain_capsules"},
    {"prompt": "tropical pineapple plantation, golden fruit close-up, natural source of bromelain, vivid colors", "alias": "bromelain_nature"},
    {"prompt": "woman taking supplement with water, healthy morning routine, kitchen, natural light", "alias": "bromelain_routine"},
]

TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{job['prompt']}, photorealistic, high quality",
        "negative_prompt": "cartoon, anime, ugly, blurry, deformed, text, watermark",
        "width": 1024,
        "height": 1024,
        "steps": 8,
        "guidance_scale": 0.0,
        "model": "z-image-turbo",
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
    print(f"Z-Image Turbo 의료/건강 배치 {TOTAL}장")
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
    print(f"저장: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
