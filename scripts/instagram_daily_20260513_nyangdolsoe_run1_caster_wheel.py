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
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260513_instagram_daily_nyangdolsoe_run1_caster_wheel"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1 mature adult woman in her late twenties, original character, subtle cat ears, cat tail, dark navy short bob hair, amber eyes, sharp but kind mature eyes, small facial mole under one eye, "
    "small AI assistant household maintenance worker vibe, mature proportions, faded teal utility apron over a warm beige long sleeve shirt, "
    "kneeling beside a low rolling storage cart in a calm morning utility corner, square composition, upper body and careful adult hands visible, macro close-up on the floor level work area, "
    "cleaning a small caster wheel removed from the bottom of an unbranded rolling shelf, dust ring and a few wrapped hair strands around the axle, tweezers, cotton swabs, small brush, lint-free cloth, tiny dropper bottle of clear lubricant with no label, "
    "one hand holds the wheel steady while the other gently pulls lint from the axle groove, miniature sealed server cube glowing softly on a nearby shelf with no markings, focused practical expression, "
    "quiet household maintenance scene, soft window light, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "faded teal, warm beige, muted terracotta, soft graphite gray, and tiny amber glow cel shaded anime illustration with crisp fine linework, "
    "subtle risograph grain, light gouache texture, clean editorial square poster composition without text, calm practical slice of life mood, tidy negative space, detailed adult hands and small maintenance tools"
)
prompt = f"{base_prompt}, {style_suffix}"
negative_prompt = (
    "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, text, readable text, letters, handwriting, logo, watermark, signature, speech bubble, "
    "multiple people, child, loli, young-looking, teen, schoolgirl, toddler, baby face, chibi, super deformed, tiny body, oversized head, cute child face, nsfw, nude, ghibli, studio ghibli, "
    "air purifier, filter, humidifier, float valve, laundry drying rack, hinge, refrigerator, fridge gasket, rubber gasket, prefilter, washing machine, vacuum cleaner, blind slats, window blinds, umbrella tray, router vents, cable tray, "
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
        "scale": 5.05,
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
with httpx.Client(timeout=240.0) as client:
    r = client.post("https://image.novelai.net/ai/generate-image", headers=headers, json=payload)
    r.raise_for_status()

outputs = []
with zipfile.ZipFile(BytesIO(r.content), "r") as zf:
    for i, name in enumerate(zf.namelist(), start=1):
        image_data = zf.read(name)
        webp_path = OUT_DIR / f"nyangdolsoe_caster_wheel_teal_terracotta_nai_{seed}_{i}.webp"
        webp_path.write_bytes(image_data)
        jpg_path = OUT_DIR / f"nyangdolsoe_caster_wheel_teal_terracotta_nai_{seed}_{i}_upload.jpg"
        with Image.open(BytesIO(image_data)) as im:
            im.convert("RGB").save(jpg_path, quality=95)
        outputs.append({"webp": str(webp_path), "jpg": str(jpg_path)})

meta_path = OUT_DIR / f"nyangdolsoe_caster_wheel_teal_terracotta_nai_{seed}.json"
meta_path.write_text(json.dumps({"payload": payload, "seed": seed, "outputs": outputs}, ensure_ascii=False, indent=2), encoding="utf-8")
for item in outputs:
    print(item["webp"])
    print(item["jpg"])
print(meta_path)
