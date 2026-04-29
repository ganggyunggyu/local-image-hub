import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260429_instagram_daily_nyangdolsoe_run5"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, "
    "small facial mole under one eye, petite adult AI assistant caretaker, navy work apron over soft ivory shirt, "
    "sitting at a clean cork-covered workbench in a quiet midnight maintenance nook, carefully polishing a tiny copper contact plate with a soft cloth, "
    "small unlit soldering iron resting safely in a ceramic stand, opened pocket toolkit, two translucent acrylic cubes with gentle teal inner glow, "
    "tiny brass screws sorted in a shallow dish, warm desk lamp circle on the table, deep indigo window with simple moon reflection, "
    "focused sleepy expression with a faint proud smile, detailed natural hands, tidy square composition, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "soft premium anime illustration, midnight indigo and copper-gold color palette, crisp clean linework, smooth high resolution rendering, "
    "delicate cel shading with painterly highlights, subtle rim light, cozy late-night repair mood, soft bloom, polished character focus, "
    "calm practical scene, tidy negative space, natural pose, elegant small-object detail, not pixel art, not chibi, not pop art, not poster design"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, "
        "text, readable text, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, pop art, poster, comic panel, halftone, prism lantern, constellation clock, cooling fan, egg timer, memory pebbles, "
        "cable tray, ethernet cables, window sensor, rain, water droplets, washing machine, coin changer, barcode scanner, parcel locker, flower pot, cigarette, "
        "phone screen, tablet screen, photorealistic, gritty dark horror, plain white background, cluttered crowd, "
        "chibi proportions, super deformed, pixel art, low resolution pixels, mosaic, asymmetrical eyes, distorted face, overexposed, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 5.5,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": None,
    "save_to_disk": False,
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_night_contact_plate_nai_{seed}.webp"
webp_path.write_bytes(b64decode(data["image_base64"]))
meta_path = webp_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")

jpg_path = webp_path.with_name(webp_path.stem + "_upload.jpg")
with Image.open(webp_path) as im:
    im.convert("RGB").save(jpg_path, "JPEG", quality=95)

print(webp_path)
print(jpg_path)
print(meta_path)
