import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://127.0.0.1:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260430_instagram_daily_nyangdolsoe_run5"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark navy short bob hair, amber eyes, sharp but kind eyes, "
    "small facial mole under one eye, compact adult AI assistant house steward, navy utility apron over oatmeal knit shirt, "
    "kneeling in a tiny apartment entryway at night, calmly polishing a pair of small worn robot boots beside a low wooden shoe rack, "
    "soft round lamp on the floor, neat brush kit, folded cream cloth, tiny brass bell, two blank ceramic shoe horns with absolutely no writing, "
    "one hand holding a polishing brush and the other steadying a boot, practical focused expression, faint tired smile, "
    "clean square composition, clear character focus, detailed natural hands, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "quiet midnight anime illustration, muted plum and warm cream palette, soft risograph grain, crisp elegant linework, "
    "gentle floor-level lighting, cozy domestic maintenance mood, tasteful negative space, small-object detail, "
    "polished high resolution rendering, natural kneeling pose, subtle dust motes, not chibi, not pop art, not poster design"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, "
        "text, readable text, letters, numbers, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, flower pot, rain gauge, rooftop, balcony, water droplets, tea drawer, pantry drawer, label maker, parcel box, "
        "soldering iron, contact plate, cooling fan, cable tray, ethernet cables, constellation clock, quiet timer, backup battery, battery dock, "
        "phone screen, tablet screen, barcode scanner, rice cooker, vending machine, laundromat, coin changer, photorealistic, gritty dark horror, "
        "plain white background, cluttered crowd, chibi proportions, super deformed, pixel art, low resolution pixels, asymmetrical eyes, distorted face, "
        "overexposed, muddy colors, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 5.2,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": None,
    "save_to_disk": True,
    "filename": "ig_20260430_run5_entryway_boots_fresh.webp",
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_entryway_boot_polish_nai_{seed}.webp"
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
