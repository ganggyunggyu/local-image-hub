import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260428_instagram_daily_nyangdolsoe_run4"
OUT_DIR.mkdir(parents=True, exist_ok=True)

payload = {
    "prompt": (
        "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, facial mole under eye, "
        "small AI assistant repair worker vibe, navy work apron over soft cream shirt, kneeling beside an open under-desk cable tray, "
        "gently untangling translucent blue ethernet cables like tiny water streams, small portable diagnostic tablet with blank screen, "
        "one warm green status LED, clear parts box with screws, soft evening desk lamp, clean wooden floor, quiet office nook, "
        "calm focused expression, practical and cozy mood, square composition, no readable text, no logo, no watermark, masterpiece, best quality"
    ),
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, "
        "text, readable text, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, parcel locker, cache cards, herb garden, flower pot, cigarette, typewriter, rooftop, rain, washing machine, "
        "overexposed, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": "waterful",
    "save_to_disk": False,
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_cable_tray_waterful_nai_{seed}.webp"
webp_path.write_bytes(b64decode(data["image_base64"]))
meta_path = webp_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")
# Instagram upload fallback prefers jpg in this environment
jpg_path = webp_path.with_name(webp_path.stem + "_upload.jpg")
with Image.open(webp_path) as im:
    im.convert("RGB").save(jpg_path, "JPEG", quality=95)
print(webp_path)
print(jpg_path)
print(meta_path)
