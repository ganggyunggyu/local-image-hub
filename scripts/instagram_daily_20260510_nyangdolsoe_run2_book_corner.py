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
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260510_instagram_daily_nyangdolsoe_run2_book_corner"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1 mature adult woman in her late twenties, original character, subtle cat ears, cat tail, dark blue short bob hair, amber eyes, sharp but kind mature eyes, facial mole under one eye, "
    "small AI assistant household maintenance worker vibe, mature proportions, navy work apron over a soft ivory shirt, "
    "sitting at a tidy wooden desk in soft late-morning window light, square composition, upper body and careful adult hands visible, "
    "repairing a curled plain notebook corner with a small strip of transparent archival repair tape and a smooth bone folder, "
    "one hand holds the blank cover flat while the other presses the corner edge neatly, tiny scissors, linen cloth, and a small unlabeled parts tray nearby, "
    "miniature sealed server cube on the back shelf with no markings, calm focused expression, everyday paper maintenance scene, tactile paper fibers and translucent tape detail, "
    "no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "warm gouache and papercut collage anime illustration, soft sage green, ochre, cream, dusty blue, and deep navy palette, "
    "subtle paper grain, clean ink edges, gentle window shadows, practical slice of life mood, editorial square poster composition without text, "
    "crisp adult hand details, tidy negative space, handmade stationery repair aesthetic"
)
prompt = f"{base_prompt}, {style_suffix}"
negative_prompt = (
    "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, text, readable text, letters, handwriting, logo, watermark, signature, speech bubble, "
    "multiple people, child, loli, young-looking, teen, schoolgirl, toddler, baby face, chibi, super deformed, tiny body, oversized head, cute child face, nsfw, nude, ghibli, studio ghibli, "
    "vending machine, barcode scanner, parcel locker, rice cooker, window sensor, cable tray, coin changer, cooling fan, constellation clock, contact plate, tea drawer, backup battery, "
    "boot polish, keyring, cat fountain, window track, umbrella tray, router vents, balcony wind chime, desk lamp hinge, coaster ring, glasses screw, door hinge, stamp pad, desiccant box, "
    "chair felt, button tray, pencil shavings, lamp switch, drawer rail, plant saucer, potted plant, soap dish, fridge gasket, refrigerator, power strip, outlet, remote control, battery compartment, "
    "mouse wheel, mouse pad, laundry lint filter, washing machine, iron, placemat, phone screen, tablet screen, keyboard, monitor with text, vacuum cleaner, brush roll, blind slats, window blinds, "
    "shoelace, zipper, shoes, jacket, book title, readable book cover, photorealistic, horror, muddy colors, overexposed, cluttered crowd, plain white background, flat empty scene, asymmetrical eyes, distorted face"
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
        "scale": 5.4,
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
    image_data = zf.read(zf.namelist()[0])
webp_path = OUT_DIR / f"nyangdolsoe_book_corner_gouache_papercut_nai_{seed}.webp"
webp_path.write_bytes(image_data)
meta_path = webp_path.with_suffix(".json")
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "file": str(webp_path)}, ensure_ascii=False, indent=2), encoding="utf-8")
jpg_path = OUT_DIR / f"nyangdolsoe_book_corner_gouache_papercut_nai_{seed}_upload.jpg"
with Image.open(BytesIO(image_data)) as im:
    im.convert("RGB").save(jpg_path, quality=95)
print(webp_path)
print(jpg_path)
print(meta_path)
