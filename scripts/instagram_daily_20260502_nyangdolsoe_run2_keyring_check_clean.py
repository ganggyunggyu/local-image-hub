import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://127.0.0.1:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260502_instagram_daily_nyangdolsoe_run2_clean"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark navy short bob hair, amber eyes, sharp but kind eyes, "
    "small facial mole under one eye, compact adult AI assistant house steward, navy utility apron over pale sand work shirt, "
    "standing beside a narrow entryway shelf in soft late morning light, carefully checking a small brass key ring and tightening one loose split ring with tiny pliers, "
    "only plain brass keys with smooth blank heads, no tags, no cards, no labels, no paper, shallow ceramic dish, folded linen cloth, small unlabeled oil dropper bottle, smooth wall hooks, "
    "one hand holding the key ring steady and the other hand using the tiny pliers, practical focused expression with a faint smug smile, "
    "clear character focus, clean square composition, detailed natural hands, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "soft lacquered-ink anime illustration, muted teal, warm brass, and pale sand palette, crisp expressive linework, "
    "gentle morning doorway light, subtle paper fiber texture, tidy entryway maintenance ritual mood, polished high resolution rendering, "
    "small metal detail highlights, balanced negative space, calm domestic readiness atmosphere, natural standing pose, not chibi, not pop art, not poster design"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, "
        "text, readable text, unreadable text, pseudo text, letters, characters, glyphs, numbers, kanji, kana, alphabet, logo, watermark, signature, speech bubble, "
        "tag, tags, label, labels, paper tag, key tag, card, cards, note, notes, sticky note, hanging paper, writing, inscription, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, air purifier, filter, dust brush, apron mending, sewing needle, thread, tomato pincushion, shoes, boots, shoe rack, "
        "backup battery, battery dock, sunset balcony, rain gauge, rooftop, tea drawer, pantry drawer, parcel box, soldering iron, contact plate, cooling fan, "
        "cable tray, ethernet cables, constellation clock, quiet timer, prism archive, window sensor, rice cooker, vending machine, laundromat, coin changer, flower pot, "
        "photorealistic, gritty dark horror, plain white background, cluttered crowd, chibi proportions, super deformed, pixel art, low resolution pixels, "
        "asymmetrical eyes, distorted face, overexposed, muddy colors, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 5.15,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": None,
    "save_to_disk": True,
    "filename": "ig_20260502_run2_keyring_check_clean_fresh.webp",
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_keyring_check_clean_nai_{seed}.webp"
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
