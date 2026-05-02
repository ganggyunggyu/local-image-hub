import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://127.0.0.1:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260502_instagram_daily_nyangdolsoe_run3_cat_fountain"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark navy short bob hair, amber eyes, sharp but kind eyes, "
    "small facial mole under one eye, compact adult AI assistant house steward, navy utility apron over pale oatmeal work shirt, "
    "kneeling beside a low tiled washstand in soft afternoon window light, carefully cleaning a small ceramic cat water fountain pump, "
    "one hand holding a tiny transparent pump part and the other hand using a fine soft brush, clear water droplets, white ceramic basin, "
    "folded microfiber cloth, small unlabeled glass bowl, smooth river pebbles, no labels, no markings, no text anywhere, "
    "practical focused expression with a faint smug smile, clear character focus, clean square composition, detailed natural hands, "
    "cozy domestic maintenance ritual, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "cool aqua and warm ivory anime illustration, refined ink linework with soft watercolor wash, subtle ceramic glaze highlights, "
    "gentle afternoon light, tiny water sparkle details, balanced negative space, calm caretaker mood, polished high resolution rendering, "
    "natural kneeling pose, tactile brush and water textures, not chibi, not pop art, not poster design"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, "
        "text, readable text, unreadable text, pseudo text, letters, characters, glyphs, numbers, kanji, kana, alphabet, logo, watermark, signature, speech bubble, "
        "label, labels, tag, tags, paper tag, note, notes, sticky note, writing, inscription, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, key ring, keys, pliers, moss terrarium, fern, glass terrarium, apron mending, sewing needle, thread, air purifier, filter, dust brush, "
        "tea drawer, pantry drawer, backup battery, battery dock, shoes, boots, shoe rack, parcel box, cooling fan, soldering iron, constellation clock, quiet timer, "
        "rain gauge, rooftop, laundromat, vending machine, phone, telephone, box, flower pot, cigarette, smoking, photorealistic, gritty dark horror, "
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
    "filename": "ig_20260502_run3_cat_fountain_pump_fresh.webp",
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_cat_fountain_pump_nai_{seed}.webp"
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
