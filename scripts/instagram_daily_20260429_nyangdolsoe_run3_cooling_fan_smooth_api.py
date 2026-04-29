import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260429_instagram_daily_nyangdolsoe_run3"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, "
    "small facial mole under one eye, petite adult AI assistant repair worker, navy work apron over soft ivory shirt, "
    "sitting cross-legged on a clean studio floor in a quiet late afternoon room, carefully oiling a tiny transparent cooling fan with a miniature glass dropper, "
    "disassembled small server cube beside her, tiny screws arranged in a shallow ceramic dish, blank masking tape labels with no writing, "
    "one soft mint status light reflecting on the floor, sheer cream curtains, floating dust motes, focused but faintly amused expression, "
    "detailed hands, practical maintenance mood, clean square composition, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "soft premium anime illustration, pale mint and warm cream color palette, crisp clean linework, smooth high resolution rendering, "
    "delicate cel shading with painterly highlights, subtle rim light, gentle afternoon atmosphere, soft bloom, polished character focus, "
    "cozy everyday tech-maintenance scene, tidy negative space, natural pose, not pixel art, not chibi, not pop art, not poster design"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, "
        "text, readable text, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, pop art, poster, comic panel, prism lantern, constellation clock, cable tray, ethernet cables, "
        "window sensor, rain, water droplets, washing machine, coin changer, barcode scanner, parcel locker, flower pot, cigarette, "
        "phone screen, tablet screen, photorealistic, gritty dark horror, plain white background, cluttered crowd, "
        "chibi proportions, super deformed, pixel art, low resolution pixels, mosaic, halftone, dithering, asymmetrical eyes, distorted face, overexposed, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 5.6,
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
webp_path = OUT_DIR / f"nyangdolsoe_cooling_fan_smooth_api_nai_{seed}.webp"
webp_path.write_bytes(b64decode(data["image_base64"]))
meta_path = webp_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")

jpg_path = webp_path.with_name(webp_path.stem + "_upload.jpg")
with Image.open(webp_path) as im:
    im.convert("RGB").save(jpg_path, "JPEG", quality=95)

print(webp_path)
print(jpg_path)
print(meta_path)
