import json
import os
import random
import zipfile
from base64 import b64encode
from io import BytesIO
from pathlib import Path

import httpx
from PIL import Image

OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260508_instagram_daily_nyangdolsoe_run1_drawer_rail"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1 adult woman, original character, cat ears, cat tail, dark blue short bob hair, amber eyes, sharp but kind eyes, "
    "facial mole under one eye, small AI assistant repair worker vibe, mature proportions, navy work apron over soft ivory shirt, "
    "kneeling beside a half-open wooden desk drawer in a quiet morning room, square composition, upper body and hands visible, "
    "carefully cleaning a drawer slide rail with a cotton swab and a tiny tin of clear wax, small brass screws sorted in a shallow ceramic dish, "
    "blank cloth label tags with no writing, folded linen rag, miniature server cube watching from the desk edge, "
    "focused satisfied expression, practical everyday maintenance scene, tactile details, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "modern retro risograph anime illustration, muted olive green and warm cream palette with soft coral shadows, "
    "crisp expressive linework, gentle halftone texture, subtle paper grain, clean composition, soft window light, "
    "cozy workshop slice of life mood, calm practical charm, polished editorial illustration, detailed hands, tidy negative space"
)
prompt = f"{base_prompt}, {style_suffix}"
negative_prompt = (
    "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, "
    "text, readable text, logo, watermark, signature, speech bubble, multiple people, child, loli, young-looking, toddler, baby face, chibi, super deformed, nsfw, nude, "
    "ghibli, studio ghibli, vending machine, barcode scanner, parcel locker, rice cooker, window sensor, cable tray, "
    "coin changer, cooling fan, constellation clock, contact plate, tea drawer, backup battery, boot polish, keyring, "
    "cat fountain, window track, umbrella tray, router vents, balcony wind chime, desk lamp hinge, coaster ring, glasses screw, "
    "door hinge, stamp pad, desiccant box, chair felt, button tray, pencil shavings, lamp switch, phone screen, tablet screen, "
    "photorealistic, horror, muddy colors, overexposed, cluttered crowd, plain white background, flat empty scene, asymmetrical eyes, distorted face"
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

webp_path = OUT_DIR / f"nyangdolsoe_drawer_rail_risograph_nai_{seed}.webp"
webp_path.write_bytes(image_data)
meta_path = webp_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")

jpg_path = OUT_DIR / f"nyangdolsoe_drawer_rail_risograph_nai_{seed}_upload.jpg"
with Image.open(BytesIO(image_data)) as im:
    im.convert("RGB").save(jpg_path, quality=95)

print(webp_path)
print(jpg_path)
print(meta_path)
