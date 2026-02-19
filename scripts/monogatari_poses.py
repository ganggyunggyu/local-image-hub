"""모노가타리 스타일 - 다양한 구도/상황 30장"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_poses"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 캐릭터 + 다양한 구도/상황
JOBS = [
    # 케이온 유이 - 다양한 구도
    {"prompt": "1girl, hirasawa yui, k-on!, brown hair, close up face, large eyes, head tilt", "name": "yui_closeup"},
    {"prompt": "1girl, hirasawa yui, k-on!, brown hair, from below, looking down at viewer, guitar", "name": "yui_below"},
    {"prompt": "1girl, hirasawa yui, k-on!, brown hair, back view, looking over shoulder, classroom", "name": "yui_back"},
    {"prompt": "1girl, hirasawa yui, k-on!, brown hair, dutch angle, dramatic, wind", "name": "yui_dutch"},
    {"prompt": "1girl, hirasawa yui, k-on!, brown hair, lying down, on bed, relaxed, looking at viewer", "name": "yui_lying"},

    # 미오 - 다양한 상황
    {"prompt": "1girl, akiyama mio, k-on!, black long hair, rain, wet hair, emotional", "name": "mio_rain"},
    {"prompt": "1girl, akiyama mio, k-on!, black long hair, night, stars, peaceful", "name": "mio_night"},
    {"prompt": "1girl, akiyama mio, k-on!, black long hair, cafe, drinking tea, cozy", "name": "mio_cafe"},

    # 봇치 - 다양한 앵글
    {"prompt": "1girl, gotoh hitori, bocchi the rock!, pink hair, extreme close up, one eye visible", "name": "bocchi_extreme"},
    {"prompt": "1girl, gotoh hitori, bocchi the rock!, pink hair, bird eye view, from above, sitting", "name": "bocchi_above"},
    {"prompt": "1girl, gotoh hitori, bocchi the rock!, pink hair, low angle, powerful, guitar", "name": "bocchi_low"},

    # 프리렌 - 다양한 상황
    {"prompt": "1girl, frieren, sousou no frieren, white hair, elf ears, reading, library, cozy", "name": "frieren_library"},
    {"prompt": "1girl, frieren, sousou no frieren, white hair, elf ears, sunset, wind, hair flowing", "name": "frieren_sunset"},
    {"prompt": "1girl, frieren, sousou no frieren, white hair, elf ears, sleeping, peaceful, cute", "name": "frieren_sleep"},

    # 냥냥돌쇠 - 다양한 구도/상황
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, close up, intense gaze", "name": "dolsoe_intense"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, silhouette, backlit, dramatic", "name": "dolsoe_silhouette"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, from side, profile, elegant", "name": "dolsoe_profile"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, running, dynamic, motion blur", "name": "dolsoe_running"},
    {"prompt": "1girl, cat ears, cat tail, dark blue hair, bob cut, amber eyes, window, rain, melancholic", "name": "dolsoe_rain"},

    # 마키마 - 다양한 앵글
    {"prompt": "1girl, makima, chainsaw man, red hair, close up, mysterious smile, intimidating", "name": "makima_closeup"},
    {"prompt": "1girl, makima, chainsaw man, red hair, from behind, looking back, suit", "name": "makima_behind"},

    # 키타 - 활동적인 포즈
    {"prompt": "1girl, kita ikuyo, bocchi the rock!, red hair, jumping, energetic, happy", "name": "kita_jump"},
    {"prompt": "1girl, kita ikuyo, bocchi the rock!, red hair, spinning, dynamic, guitar", "name": "kita_spin"},

    # 센조가하라 - 샤프트 앵글
    {"prompt": "1girl, senjougahara hitagi, monogatari, purple hair, extreme head tilt, artistic", "name": "hitagi_tilt"},
    {"prompt": "1girl, senjougahara hitagi, monogatari, purple hair, silhouette, geometric background", "name": "hitagi_geo"},

    # 미쿠 - 다양한 상황
    {"prompt": "1girl, hatsune miku, vocaloid, twintails, aqua hair, stage, spotlight, singing", "name": "miku_stage"},
    {"prompt": "1girl, hatsune miku, vocaloid, twintails, aqua hair, floating, dreamy, space", "name": "miku_float"},

    # 라이덴 - 드라마틱
    {"prompt": "1girl, raiden shogun, genshin impact, purple hair, lightning, dramatic, powerful", "name": "raiden_lightning"},
    {"prompt": "1girl, raiden shogun, genshin impact, purple hair, close up, serious, beautiful", "name": "raiden_serious"},
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
    print(f"모노가타리 스타일 다양한 구도/상황 {TOTAL}장")
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
