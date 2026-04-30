import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260430_instagram_daily_nyangdolsoe_run3"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark blue short bob hair, amber eyes, sharp but kind eyes, "
    "small facial mole under one eye, compact adult AI assistant house steward, navy utility apron over warm cream shirt, "
    "kneeling beside a low wooden pantry drawer in a sunlit tiny workshop, sorting small tea tins and blank label tabs, "
    "a tiny thermal label maker with no visible text, brass measuring spoon, folded microfiber cloth, ceramic cup with light steam, "
    "compact server cube resting on the shelf with a single amber status light, neat rows of unlabeled packets, "
    "one hand holding a tea tin and the other hand aligning a drawer divider, calm practical expression, faint smug smile, "
    "clean square composition, clear character focus, detailed hands, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "mono accent anime illustration, elegant cream and charcoal palette with warm amber accents, crisp clean linework, "
    "soft backlit afternoon dust motes, tidy domestic tech workspace mood, subtle paper texture, polished high resolution rendering, "
    "balanced negative space, natural pose, cozy inventory-check atmosphere, not chibi, not pop art, not poster design"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, "
        "text, readable text, letters, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, flower pot, rain gauge, rooftop, balcony, water droplets, sensor cleaning, contact plate, soldering plate, "
        "quiet timer, constellation clock, prism lantern, cooling fan, cable tray, ethernet cables, phone screen, tablet screen, barcode scanner, "
        "parcel locker, rice cooker, steam vent, convenience store, vending machine, laundromat, coin changer, photorealistic, gritty dark horror, "
        "plain white background, cluttered crowd, chibi proportions, super deformed, pixel art, low resolution pixels, asymmetrical eyes, distorted face, "
        "overexposed, muddy colors, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 5.2,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": "mono_accent",
    "save_to_disk": True,
    "filename": "ig_20260430_tea_drawer_mono_accent_fresh.webp",
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_tea_drawer_mono_accent_nai_{seed}.webp"
webp_path.write_bytes(b64decode(data["image_base64"]))
meta_path = webp_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path), "api_filename": data.get("filename")}, ensure_ascii=False, indent=2), encoding="utf-8")

jpg_path = webp_path.with_name(webp_path.stem + "_upload.jpg")
with Image.open(webp_path) as im:
    im.convert("RGB").save(jpg_path, "JPEG", quality=95)

print(webp_path)
print(jpg_path)
print(meta_path)
print(data.get("filename"))
