import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260427_instagram_daily_nyangdolsoe_run4"
OUT_DIR.mkdir(parents=True, exist_ok=True)

payload = {
    "prompt": (
        "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, facial mole under eye, "
        "small AI assistant vibe, rolled-up navy work apron over cream shirt, crouching in a quiet convenience store back room at dusk, "
        "checking a handheld barcode scanner and a tiny receipt printer on a stainless counter, replacing a small thermal paper roll, "
        "open maintenance notebook with completely blank pages, colored cable labels as simple abstract blocks with no letters, "
        "orange cat-shaped cable clip, small toolbox, soft fluorescent light, tidy practical workspace, calm after-hours mood, "
        "clean square composition, upper body, no readable text, masterpiece, best quality"
    ),
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, "
        "text, logo, watermark, signature, speech bubble, letters, numbers, readable writing, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, flower pot, basil plant, rooftop, weather sensor, cigarette, telephone, typewriter, server rack, "
        "rainy night, overexposed, washed out"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 4.0,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": "kyoto_animation",
    "save_to_disk": False,
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_convenience_scanner_kyoto_nai_{seed}.webp"
webp_path.write_bytes(b64decode(data["image_base64"]))
json_path = webp_path.with_suffix(".json")
json_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")

jpg_path = webp_path.with_suffix(".upload.jpg")
with Image.open(webp_path) as im:
    im.convert("RGB").save(jpg_path, "JPEG", quality=94, optimize=True)

print(webp_path)
print(jpg_path)
print(json_path)
