import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260427_instagram_daily_nyangdolsoe_run5"
OUT_DIR.mkdir(parents=True, exist_ok=True)

payload = {
    "prompt": (
        "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, facial mole under eye, "
        "small AI assistant vibe, navy work apron over cream shirt, late-night self-service laundromat maintenance corner, "
        "kneeling beside an opened coin changer panel with simple blank metal slots, holding a tiny flashlight and a screwdriver, "
        "round washing machines glowing teal in the background, magenta vending machine light reflection, scattered blank maintenance tags with no letters, "
        "orange cat-shaped keychain on a tool pouch, quiet urban interior, practical tidy mood, calm focused expression, "
        "clean square composition, upper body, no readable text, masterpiece, best quality"
    ),
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, "
        "text, logo, watermark, signature, speech bubble, letters, numbers, readable writing, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, flower pot, basil plant, rooftop, weather sensor, server rack, telephone, cigarette, typewriter, "
        "barcode scanner, receipt printer, bucket, sharpener, spatula, overexposed, washed out"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 28,
    "guidance_scale": 5.9,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": "zutomayo",
    "save_to_disk": False,
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_laundromat_coin_changer_zutomayo_nai_{seed}.webp"
webp_path.write_bytes(b64decode(data["image_base64"]))
json_path = webp_path.with_suffix(".json")
json_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")

jpg_path = webp_path.with_suffix(".upload.jpg")
with Image.open(webp_path) as im:
    im.convert("RGB").save(jpg_path, "JPEG", quality=94, optimize=True)

print(webp_path)
print(jpg_path)
print(json_path)
