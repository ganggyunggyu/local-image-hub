import json
from base64 import b64decode
from datetime import datetime
from pathlib import Path

import httpx

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260427_instagram_daily_nyangdolsoe"
OUT_DIR.mkdir(parents=True, exist_ok=True)

payload = {
    "prompt": (
        "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, "
        "small AI assistant vibe, light cream cardigan over navy work apron, tiny brass bell accessory, "
        "standing beside a sunny windowsill herb garden and a compact server box, watering a small basil pot with one hand, "
        "sticky notes and neatly coiled charging cables on the desk, spring morning light, dust motes, calm focused expression, "
        "gentle smile, cozy workspace, clean composition, upper body, no text, masterpiece, best quality"
    ),
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, "
        "text, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, ghibli, studio ghibli, "
        "rain, night, cigarette, typewriter"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 28,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": "opal_bloom",
    "save_to_disk": False,
}

with httpx.Client(timeout=180.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
file_path = OUT_DIR / f"nyangdolsoe_spring_windowsill_opal_bloom_nai_{seed}.webp"
file_path.write_bytes(b64decode(data["image_base64"]))
meta_path = file_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(file_path)}, ensure_ascii=False, indent=2), encoding="utf-8")
print(file_path)
print(meta_path)
