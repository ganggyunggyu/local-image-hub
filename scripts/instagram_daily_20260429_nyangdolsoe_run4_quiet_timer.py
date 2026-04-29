import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260429_instagram_daily_nyangdolsoe_run4"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, "
    "small facial mole under one eye, petite adult AI assistant caretaker, navy work apron over soft ivory shirt, "
    "sitting at a low walnut worktable in a quiet blue-hour attic studio, gently adjusting a tiny brass mechanical egg timer with one hand, "
    "three small translucent memory pebbles lined up on a dark felt mat, a compact server cube sleeping nearby with one dim teal status light, "
    "warm tea cup with a thin curl of steam, folded cleaning cloth, tiny screwdriver, moonlight through round window, "
    "focused calm expression with a faint smug smile, detailed hands, clean square composition, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "soft premium anime illustration, blue-hour navy and warm amber color palette, crisp clean linework, smooth high resolution rendering, "
    "delicate cel shading with painterly highlights, subtle rim light, cozy quiet maintenance mood, soft bloom, polished character focus, "
    "tidy negative space, natural pose, elegant small-object detail, not pixel art, not chibi, not pop art, not poster design"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, "
        "text, readable text, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, pop art, poster, comic panel, halftone, prism lantern, constellation clock, cooling fan, cable tray, ethernet cables, "
        "window sensor, rain, water droplets, washing machine, coin changer, barcode scanner, parcel locker, flower pot, cigarette, "
        "phone screen, tablet screen, photorealistic, gritty dark horror, plain white background, cluttered crowd, "
        "chibi proportions, super deformed, pixel art, low resolution pixels, mosaic, asymmetrical eyes, distorted face, overexposed, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 5.4,
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
webp_path = OUT_DIR / f"nyangdolsoe_quiet_timer_nai_{seed}.webp"
webp_path.write_bytes(b64decode(data["image_base64"]))
meta_path = webp_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")

jpg_path = webp_path.with_name(webp_path.stem + "_upload.jpg")
with Image.open(webp_path) as im:
    im.convert("RGB").save(jpg_path, "JPEG", quality=95)

print(webp_path)
print(jpg_path)
print(meta_path)
