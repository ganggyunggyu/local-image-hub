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
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260514_instagram_daily_nyangdolsoe_run1_shelf_pin_level"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1 mature adult woman in her early thirties, original character, subtle cat ears, cat tail, dark navy short bob hair, amber eyes, sharp but kind mature eyes, small facial mole under one eye, "
    "small AI assistant household maintenance worker vibe, mature proportions, slate blue work apron over a soft oatmeal ribbed knit shirt, "
    "quiet study room shelf corner, square composition, upper body and careful adult hands clearly visible, practical tiny maintenance close-up, "
    "leveling a slightly wobbly wooden bookshelf shelf by moving a small metal shelf pin into a cleaner hole and adding one tiny transparent rubber bumper pad, "
    "a pocket bubble level with no numbers or readable markings, a shallow dish with spare shelf pins, folded dust cloth, pencil eraser crumb, "
    "miniature sealed server cube glowing softly on the desk nearby with no markings, focused quietly satisfied expression, calm household problem-solving routine, "
    "plain book spines turned away with no readable titles, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "colored pencil and lacquered flat anime illustration, crisp economical linework, dusty rose, slate blue, walnut brown, warm oatmeal, and small translucent teal accents, "
    "soft crosshatch texture, gentle paper grain, tidy editorial square poster composition without text, cozy practical slice of life mood, "
    "detailed adult hands, tactile wood grain and tiny hardware, balanced negative space"
)
prompt = f"{base_prompt}, {style_suffix}"
negative_prompt = (
    "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, text, readable text, letters, numbers, digits, handwriting, logo, watermark, signature, speech bubble, "
    "multiple people, child, loli, young-looking, teen, schoolgirl, toddler, baby face, chibi, super deformed, tiny body, oversized head, cute child face, nsfw, nude, ghibli, studio ghibli, "
    "weapon, knife, scissors, sharp blade, blood, injury, horror, threatening pose, "
    "cabinet magnetic latch, toothbrush holder, jar lid thread, caster wheel, rolling cart, air purifier, filter, humidifier, float valve, laundry drying rack, hinge, refrigerator, fridge gasket, rubber gasket, prefilter, washing machine, vacuum cleaner, blind slats, window blinds, umbrella tray, router vents, cable tray, "
    "drawer knob, drawer rail, screwdriver, brass screw, remote control, battery compartment, book corner, notebook corner, shoelace, zipper, shoes, jacket, glasses screw, eyeglasses, nose pads, lamp hinge, coaster ring, plant saucer, potted plant, soap dish, "
    "phone screen, tablet screen, keyboard, monitor with text, barcode, label, price tag, readable book cover, photorealistic, horror, muddy colors, overexposed, cluttered crowd, plain white background, flat empty scene, asymmetrical eyes, distorted face"
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
        "scale": 5.35,
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
        webp_path = OUT_DIR / f"nyangdolsoe_shelf_pin_level_colored_pencil_nai_{seed}_{i}.webp"
        webp_path.write_bytes(image_data)
        jpg_path = OUT_DIR / f"nyangdolsoe_shelf_pin_level_colored_pencil_nai_{seed}_{i}_upload.jpg"
        with Image.open(BytesIO(image_data)) as im:
            im.convert("RGB").save(jpg_path, quality=95)
        outputs.append({"webp": str(webp_path), "jpg": str(jpg_path)})

meta_path = OUT_DIR / f"nyangdolsoe_shelf_pin_level_colored_pencil_nai_{seed}.json"
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "outputs": outputs}, ensure_ascii=False, indent=2), encoding="utf-8")
for item in outputs:
    print(item["webp"])
    print(item["jpg"])
print(meta_path)
