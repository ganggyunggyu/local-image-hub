"""Z-Image 풀 모델 테스트 (50 steps, cfg=4.0)"""

import httpx
from base64 import b64decode
from pathlib import Path
from datetime import datetime

API_URL = "http://localhost:8002/api/generate"
TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_zimage_full"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

payload = {
    "prompt": "japanese spitz puppy sitting on grass, fluffy white fur, golden hour, photorealistic, high quality",
    "negative_prompt": "cartoon, anime, ugly, blurry, deformed",
    "width": 1024,
    "height": 1024,
    "steps": 50,
    "guidance_scale": 4.0,
    "model": "z-image",
    "save_to_disk": False,
}

print("Z-Image 풀 모델 테스트 시작 (최초 실행 시 45GB 다운로드)")
print("=" * 60)

try:
    r = httpx.post(API_URL, json=payload, timeout=1800.0)
    data = r.json()
    if data.get("success") and data.get("image_base64"):
        seed = data.get("seed", 0)
        fp = OUTPUT_DIR / f"zimage_full_spitz_{seed}.webp"
        fp.write_bytes(b64decode(data["image_base64"]))
        print(f"OK! seed: {seed}")
        print(f"저장: {fp}")
    else:
        print(f"FAIL: {data.get('error', data)}")
except Exception as e:
    print(f"ERROR: {e}")
