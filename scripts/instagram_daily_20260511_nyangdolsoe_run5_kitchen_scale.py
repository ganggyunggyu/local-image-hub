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
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260511_instagram_daily_nyangdolsoe_run5_kitchen_scale"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1 mature adult woman in her late twenties, original character, subtle cat ears, cat tail, dark navy short bob hair, amber eyes, sharp but kind mature eyes, small facial mole under one eye, "
    "small AI assistant household operations worker vibe, mature proportions, dusty lavender utility apron over a soft cream shirt, "
    "standing at a quiet wooden kitchen workbench late at night, square composition, upper body and careful adult hands visible, macro close-up on the tabletop work area, "
    "checking the zero point of a compact unbranded kitchen scale with a tiny brass calibration weight and a shallow ceramic dish of coffee beans, scale display intentionally blank with no digits, "
    "one hand lightly steadies the dish while the other places the small brass weight, folded lint-free cloth and a tiny brush nearby, miniature sealed server cube glowing softly on a back shelf with no markings, focused practical expression, "
    "quiet calibration routine, warm under-cabinet light, soft window reflection without readable shapes, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "dusty lavender, cream, coffee brown, muted copper, and deep navy cel shaded anime illustration with crisp fine linework, "
    "soft gouache wash texture, subtle paper grain, clean editorial square poster composition without text, calm midnight kitchen shadows, practical slice of life mood, tidy negative space, detailed adult hands"
)
prompt = f"{base_prompt}, {style_suffix}"
negative_prompt = (
    "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, text, readable text, letters, numbers, digits, handwriting, logo, watermark, signature, speech bubble, "
    "multiple people, child, loli, young-looking, teen, schoolgirl, toddler, baby face, chibi, super deformed, tiny body, oversized head, cute child face, nsfw, nude, ghibli, studio ghibli, "
    "vending machine, barcode scanner, parcel locker, rice cooker, window sensor, cable tray, coin changer, cooling fan, constellation clock, contact plate, tea drawer, backup battery, "
    "boot polish, keyring, cat fountain, window track, umbrella tray, router vents, balcony wind chime, desk lamp hinge, coaster ring, glasses screw, eyeglasses, nose pads, door hinge, stamp pad, desiccant box, "
    "chair felt, button tray, pencil shavings, mechanical pencil, graphite pencil, lamp switch, drawer rail, plant saucer, potted plant, soap dish, fridge gasket, refrigerator, power strip, outlet, remote control, battery compartment, "
    "mouse wheel, mouse pad, laundry lint filter, washing machine, iron, placemat, phone screen, tablet screen, keyboard, monitor with text, vacuum cleaner, brush roll, blind slats, window blinds, "
    "shoelace, zipper, shoes, jacket, book corner, notebook corner, book title, readable book cover, tumbler, gasket, silicone ring, lid, tape dispenser, stapler, spatula, earbud, earphone, charging case, wristwatch, watch strap, clasp, drawer knob, screwdriver, brass screw, humidifier, water tank, float valve, cotton swab, vinegar bowl, "
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
        "scale": 5.1,
        "sampler": "k_euler_ancestral",
        "steps": 30,
        "seed": seed,
        "n_samples": 2,
        "ucPreset": 0,
        "qualityToggle": True,
        "characterPrompts": [],
        "v4_prompt": {"caption": {"base_caption": prompt, "char_captions": []}, "use_coords": False, "use_order": True},
        "v4_negative_prompt": {"caption": {"base_caption": negative_prompt, "char_captions": []}},
    },
}
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
with httpx.Client(timeout=240.0) as client:
    r = client.post("https://image.novelai.net/ai/generate-image", headers=headers, json=payload)
    r.raise_for_status()

outputs = []
with zipfile.ZipFile(BytesIO(r.content), "r") as zf:
    for i, name in enumerate(zf.namelist(), start=1):
        image_data = zf.read(name)
        webp_path = OUT_DIR / f"nyangdolsoe_kitchen_scale_lavender_copper_nai_{seed}_{i}.webp"
        webp_path.write_bytes(image_data)
        jpg_path = OUT_DIR / f"nyangdolsoe_kitchen_scale_lavender_copper_nai_{seed}_{i}_upload.jpg"
        with Image.open(BytesIO(image_data)) as im:
            im.convert("RGB").save(jpg_path, quality=95)
        outputs.append({"webp": str(webp_path), "jpg": str(jpg_path)})

meta_path = OUT_DIR / f"nyangdolsoe_kitchen_scale_lavender_copper_nai_{seed}.json"
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "outputs": outputs}, ensure_ascii=False, indent=2), encoding="utf-8")
for item in outputs:
    print(item["webp"])
    print(item["jpg"])
print(meta_path)
