import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://127.0.0.1:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260503_instagram_daily_nyangdolsoe_run1_keyboard_dust"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark navy short bob hair, amber eyes, sharp but kind eyes, "
    "small facial mole under one eye, compact adult AI assistant house steward, navy utility apron over soft cream long sleeve shirt, "
    "sitting at a small wooden desk in quiet sunday morning light, gently cleaning dust between mechanical keyboard keycaps with a tiny soft brush, "
    "one removed keycap in a small ceramic saucer, microfiber cloth folded nearby, tiny dust specks caught in a sunbeam, "
    "steaming mug without any logo, tidy cable coil, low plant shadow on the wall, calm practical caretaker expression, "
    "clear character focus, clean square composition, detailed natural hands, cozy maintenance diary mood, no readable text, no labels, no signage, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "muted lavender gray and warm cream anime illustration, thin precise ink linework, soft colored pencil and gouache texture, "
    "delicate morning dust particles, tactile desk grain and brush fibers, polished high resolution rendering, natural seated pose, "
    "quiet tool-care ritual, not chibi, not pop art, not poster design"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, "
        "text, readable text, unreadable text, pseudo text, letters, characters, glyphs, numbers, kanji, kana, alphabet, logo, watermark, signature, speech bubble, "
        "label, labels, tag, tags, paper tag, note, notes, sticky note, writing, inscription, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, umbrella, umbrella stand, drip tray, bath robe, wash basin, sink, cat water fountain, pump, moss terrarium, fern, glass terrarium, window track, window rail, cotton swab, key ring, keys, cigarette, smoking, apron mending, sewing needle, thread, "
        "air purifier, filter, tea drawer, pantry drawer, backup battery, battery dock, shoes, boots, shoe rack, parcel box, cooling fan, soldering iron, constellation clock, quiet timer, "
        "rain gauge, rooftop, laundromat, vending machine, phone, telephone, flower pot, photorealistic, gritty dark horror, "
        "plain white background, cluttered crowd, chibi proportions, super deformed, pixel art, low resolution pixels, asymmetrical eyes, distorted face, "
        "overexposed, muddy colors, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 5.0,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": None,
    "save_to_disk": True,
    "filename": "ig_20260503_run1_keyboard_dust_fresh.webp",
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_keyboard_dust_nai_{seed}.webp"
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
