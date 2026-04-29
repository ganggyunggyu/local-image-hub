import json
import os
import random
import zipfile
from base64 import b64encode
from io import BytesIO
from pathlib import Path

import httpx
from PIL import Image

OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260429_instagram_daily_nyangdolsoe_run1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, "
    "facial mole under one eye, small AI assistant repair worker vibe, navy work apron over soft ivory shirt, "
    "standing in a tiny night archive room, adjusting a floating prism notification lantern with a miniature screwdriver, "
    "blank index cards, tidy cable loops, small server cube, dust motes in violet and pink light, gentle focused expression, "
    "one hand reaching toward the glowing prism, magical circuit lines, clean square composition, no readable text, no logo, "
    "no watermark, masterpiece, best quality"
)
style_suffix = (
    "high-energy anime performance illustration, luminous magenta and violet glow, pink prism lighting, "
    "musical light trails swirling in the air, sparkles and floating particles, dramatic reach-toward-camera perspective, "
    "playful confident expression, glossy hair with cool blue shadows, crisp cel shading, soft bloom, bright rim light, "
    "layered magical backdrop, stylish motion, polished character focus"
)
prompt = f"{base_prompt}, {style_suffix}"
negative_prompt = (
    "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, "
    "text, readable text, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, "
    "ghibli, studio ghibli, washing machine, coin changer, barcode scanner, parcel locker, flower pot, cigarette, typewriter, "
    "rice cooker, window sensor, cable tray, vending machine, phone screen, tablet screen, photorealistic, gritty dark horror, "
    "muted flat lighting, plain white background, static standing pose, cluttered crowd, chibi proportions, asymmetrical eyes, "
    "distorted face, washed-out neon, muddy colors, overexposed, cluttered composition"
)

token = os.getenv("NAI_TOKEN")
if not token:
    raise SystemExit("NAI_TOKEN not set")

seed = random.randint(0, 2147483647)
payload = {
    "input": prompt,
    "model": "nai-diffusion-4-5-full",
    "action": "generate",
    "parameters": {
        "params_version": 3,
        "width": 1024,
        "height": 1024,
        "scale": 5.8,
        "sampler": "k_euler_ancestral",
        "steps": 30,
        "seed": seed,
        "n_samples": 1,
        "ucPreset": 0,
        "qualityToggle": True,
        "characterPrompts": [],
        "v4_prompt": {"caption": {"base_caption": prompt, "char_captions": []}, "use_coords": False, "use_order": True},
        "v4_negative_prompt": {"caption": {"base_caption": negative_prompt, "char_captions": []}},
    },
}

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
with httpx.Client(timeout=180.0) as client:
    r = client.post("https://image.novelai.net/ai/generate-image", headers=headers, json=payload)
    r.raise_for_status()

with zipfile.ZipFile(BytesIO(r.content), "r") as zf:
    name = zf.namelist()[0]
    image_data = zf.read(name)

webp_path = OUT_DIR / f"nyangdolsoe_prism_archive_nai_{seed}.webp"
webp_path.write_bytes(image_data)
meta_path = webp_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")

jpg_path = OUT_DIR / f"nyangdolsoe_prism_archive_nai_{seed}_upload.jpg"
with Image.open(BytesIO(image_data)) as im:
    im.convert("RGB").save(jpg_path, quality=95)

print(webp_path)
print(jpg_path)
print(meta_path)
