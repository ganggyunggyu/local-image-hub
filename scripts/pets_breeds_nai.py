"""고양이 & 강아지 품종별 생성 - NAI full"""

import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_pets_breeds"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CATS = [
    {"breed": "calico cat", "desc": "sitting on white pillow, grassy lawn, sunny day"},
    {"breed": "russian blue cat", "desc": "lying on windowsill, rain outside, cozy indoor"},
    {"breed": "scottish fold cat", "desc": "curled up on sofa, warm lighting, sleepy face"},
    {"breed": "persian cat", "desc": "sitting elegantly, marble floor, luxurious room"},
    {"breed": "siamese cat", "desc": "stretching on wooden deck, morning sunlight"},
    {"breed": "maine coon cat", "desc": "sitting in snow, winter forest, fluffy fur, majestic"},
    {"breed": "british shorthair cat", "desc": "loafing on bed, soft blanket, round face, cute"},
    {"breed": "bengal cat", "desc": "crouching on tree branch, jungle vibe, wild eyes"},
    {"breed": "ragdoll cat", "desc": "being held in arms, floppy, relaxed, blue eyes"},
    {"breed": "munchkin cat", "desc": "standing on hind legs, curious, kitchen counter, short legs"},
    {"breed": "sphynx cat", "desc": "sitting on velvet cushion, warm room, wrinkly skin, dignified"},
    {"breed": "norwegian forest cat", "desc": "sitting on mossy rock, forest background, long fur, autumn"},
    {"breed": "abyssinian cat", "desc": "jumping mid-air, playful, living room, athletic"},
    {"breed": "turkish angora cat", "desc": "white fur, sitting by fireplace, elegant, fluffy tail"},
    {"breed": "black cat", "desc": "sitting on fence, full moon, night, glowing yellow eyes, mysterious"},
]

DOGS = [
    {"breed": "shiba inu", "desc": "sitting on grass, cherry blossom petals falling, smile"},
    {"breed": "golden retriever", "desc": "running on beach, waves, sunset, happy, tongue out"},
    {"breed": "corgi", "desc": "lying on back, belly up, carpet, cute butt, playful"},
    {"breed": "pomeranian", "desc": "sitting in flower field, fluffy, spring, tiny, adorable"},
    {"breed": "husky", "desc": "standing in snow, blue eyes, winter mountains, wolf-like"},
    {"breed": "toy poodle", "desc": "sitting in cafe, wearing bow, coffee table, fancy"},
    {"breed": "french bulldog", "desc": "sleeping on couch, snoring, cozy, wrinkly face"},
    {"breed": "dachshund", "desc": "running through autumn leaves, long body, park, happy"},
    {"breed": "samoyed", "desc": "smiling, white fur, snowy background, fluffy cloud dog"},
    {"breed": "border collie", "desc": "herding sheep, green meadow, intelligent eyes, action"},
    {"breed": "labrador retriever", "desc": "swimming in lake, holding stick, splashing, summer"},
    {"breed": "dalmatian", "desc": "sitting by fire truck, spotted, proud, urban street"},
    {"breed": "akita inu", "desc": "sitting at train station, loyal, waiting, nostalgic"},
    {"breed": "maltese", "desc": "sitting on lap, white silky fur, indoor, pampered"},
    {"breed": "german shepherd", "desc": "standing guard, sunset field, strong, noble, alert"},
]

JOBS = []

for i, cat in enumerate(CATS):
    JOBS.append({
        "prompt": f"no humans, {cat['breed']}, {cat['desc']}, photorealistic, detailed fur, beautiful lighting, high detail",
        "name": f"cat_{i:02d}_{cat['breed'].replace(' ', '_')}",
    })

for i, dog in enumerate(DOGS):
    JOBS.append({
        "prompt": f"no humans, {dog['breed']}, {dog['desc']}, photorealistic, detailed fur, beautiful lighting, high detail",
        "name": f"dog_{i:02d}_{dog['breed'].replace(' ', '_')}",
    })

TOTAL = len(JOBS)


async def generate(client: httpx.AsyncClient, num: int, job: dict) -> bool:
    payload = {
        "prompt": f"{job['prompt']}, masterpiece, best quality, animal focus",
        "negative_prompt": "low quality, worst quality, blurry, human, 1girl, 1boy, anime girl, text, watermark, deformed",
        "width": 1024,
        "height": 1024,
        "provider": "nai",
        "model": "nai-diffusion-4-full",
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=120.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{num:02d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{num:02d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:60]}")
            return False
    except Exception as e:
        print(f"[{num:02d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    cat_count = sum(1 for j in JOBS if j["name"].startswith("cat"))
    dog_count = sum(1 for j in JOBS if j["name"].startswith("dog"))

    print(f"고양이 & 강아지 품종별 생성 - NAI full {TOTAL}장")
    print(f"  고양이: {cat_count}종 / 강아지: {dog_count}종")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(1.0)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
