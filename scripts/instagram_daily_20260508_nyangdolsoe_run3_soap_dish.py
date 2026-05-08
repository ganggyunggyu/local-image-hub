import json
import os
import random
import zipfile
from io import BytesIO
from pathlib import Path

import httpx
from PIL import Image
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260508_instagram_daily_nyangdolsoe_run3_soap_dish"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1 adult woman, original character, cat ears, cat tail, dark blue short bob hair, amber eyes, sharp but kind eyes, "
    "facial mole under one eye, small AI assistant household maintenance worker vibe, mature proportions, navy work apron over soft ivory shirt, "
    "standing beside a tidy bathroom shelf with frosted glass and warm afternoon light, square composition, upper body and careful hands visible, "
    "cleaning the drainage holes of a pale ceramic soap dish with a tiny bamboo skewer and soft cloth, small pearly soap bar set aside on a dry linen pad, "
    "a few clear water droplets, miniature sealed server cube safely on a high dry shelf, calm practical expression, "
    "everyday maintenance scene, tactile ceramic and glass details, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "clean luminous anime illustration with crisp ink contours, translucent glass highlights, pearlescent teal and soft lavender palette, "
    "subtle art nouveau framing without text, polished editorial slice of life, gentle reflected light, detailed hands, "
    "airy composition, quiet bathroom freshness, soft paper grain, tidy negative space"
)
prompt = f"{base_prompt}, {style_suffix}"
negative_prompt = (
    "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, "
    "text, readable text, logo, watermark, signature, speech bubble, multiple people, child, loli, young-looking, toddler, baby face, chibi, super deformed, nsfw, nude, "
    "ghibli, studio ghibli, vending machine, barcode scanner, parcel locker, rice cooker, window sensor, cable tray, "
    "coin changer, cooling fan, constellation clock, contact plate, tea drawer, backup battery, boot polish, keyring, "
    "cat fountain, window track, umbrella tray, router vents, balcony wind chime, desk lamp hinge, coaster ring, glasses screw, "
    "door hinge, stamp pad, desiccant box, chair felt, button tray, pencil shavings, lamp switch, drawer rail, plant saucer, potted plant, cotton swab, phone screen, tablet screen, "
    "photorealistic, horror, muddy colors, overexposed, cluttered crowd, plain white background, flat empty scene, asymmetrical eyes, distorted face, wet clothes, shower scene, bathtub"
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
        "scale": 5.6,
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

webp_path = OUT_DIR / f"nyangdolsoe_soap_dish_luminous_nai_{seed}.webp"
webp_path.write_bytes(image_data)
meta_path = webp_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")

jpg_path = OUT_DIR / f"nyangdolsoe_soap_dish_luminous_nai_{seed}_upload.jpg"
with Image.open(BytesIO(image_data)) as im:
    im.convert("RGB").save(jpg_path, quality=95)

print(webp_path)
print(jpg_path)
print(meta_path)
