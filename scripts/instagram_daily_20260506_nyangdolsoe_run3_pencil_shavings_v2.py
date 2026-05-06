import json
from base64 import b64decode
from pathlib import Path

import httpx
from PIL import Image

API_URL = "http://127.0.0.1:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260506_instagram_daily_nyangdolsoe_run3_pencil_shavings"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark navy short bob hair, amber eyes, sharp but kind eyes, mature adult face, "
    "small facial mole under one eye, compact clearly adult AI assistant house steward, navy utility apron over soft ivory rolled-sleeve shirt, modest outfit, "
    "sitting at a quiet wooden desk in late afternoon, holding a small manual pencil sharpener with its clear shavings drawer open, visible pale curled pencil shavings pouring into a tiny paper bin, "
    "obvious open pencil sharpener, curled pale cedar pencil shavings falling downward, a few short pencils, graphite dust on a plain cloth, tiny cleaning brush, neat practical stationery maintenance scene, "
    "focused grown-up caretaker expression, natural hand pose, clear character focus, clean square composition, no readable text, no labels, no signage, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "restrained monochrome graphite anime illustration with one warm amber accent color, thin precise linework, subtle halftone grain, "
    "soft matte shadows, tactile cedar shavings texture, calm editorial slice-of-life mood, uncluttered interior composition, polished high resolution rendering, "
    "not chibi, not poster design, not pop art, not watercolor, not ghibli"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, oversized breasts, cleavage, erotic, suggestive pose, "
        "text, readable text, unreadable text, pseudo text, letters, characters, glyphs, numbers, kanji, kana, alphabet, logo, watermark, signature, speech bubble, "
        "label, labels, tag, tags, paper tag, note, notes, sticky note, writing, inscription, multiple people, teenage, teen, child, loli, babyface, school uniform, nsfw, nude, "
        "ghibli, studio ghibli, hayao miyazaki, button tray, loose buttons, sewing, needle, thread, chair leg, felt pad, camera, lens, desiccant pouch, humidity card, door hinge, doorknob, coaster, cup, mug, water ring, eyeglasses, glasses screw, screwdriver, screw tray, "
        "router, vent, keyboard, keycap, cable, charger cable, drawer, umbrella, sink, cat water fountain, pump, terrarium, window track, key ring, keys, battery, battery dock, shoes, boots, parcel box, cooling fan, soldering iron, clock, timer, laundromat, vending machine, phone, flower pot, "
        "photorealistic, gritty dark horror, plain white background, cluttered crowd, super deformed, pixel art, low resolution pixels, asymmetrical eyes, distorted face, overexposed, muddy colors, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 5.0,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": None,
    "save_to_disk": True,
    "filename": "ig_20260506_run3_pencil_shavings_fresh_v2.webp",
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_pencil_shavings_v2_nai_{seed}.webp"
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
