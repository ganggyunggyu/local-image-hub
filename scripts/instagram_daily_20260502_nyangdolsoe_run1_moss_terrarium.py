import json
from base64 import b64decode
from pathlib import Path
import httpx
from PIL import Image

API_URL = "http://127.0.0.1:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260502_instagram_daily_nyangdolsoe_run1_moss_terrarium"
OUT_DIR.mkdir(parents=True, exist_ok=True)

base_prompt = (
    "1girl, original character, cat ears, cat tail, dark navy short bob hair, amber eyes, sharp but kind eyes, "
    "small facial mole under one eye, compact adult AI assistant house steward, navy utility apron over pale sand work shirt, "
    "sitting beside a small round table in quiet late morning window light, carefully checking a tiny glass moss terrarium with a clear water dropper, "
    "one hand holding the glass lid slightly open and the other hand adding a single water droplet, miniature moss hill, small smooth stones, tiny fern sprouts, "
    "plain ceramic saucer, folded linen cloth, hygrometer-like blank brass dial with no numbers or letters, calm focused expression, faint smug smile, "
    "clear character focus, cozy domestic maintenance ritual, clean square composition, detailed natural hands, no readable text, no logo, no watermark, masterpiece, best quality"
)
style_suffix = (
    "luminous soft anime illustration with delicate ink lines, pearly moss green, warm cream, pale aqua glass reflections, "
    "subtle paper grain, shallow depth of field, gentle sunbeam dust motes, crisp small-object details, refined high resolution rendering, "
    "quiet botanical caretaker mood, balanced negative space, natural seated pose, not chibi, not poster design, not pop art"
)

payload = {
    "prompt": f"{base_prompt}, {style_suffix}",
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, fused fingers, "
        "text, readable text, unreadable text, pseudo text, letters, characters, glyphs, numbers, kanji, kana, alphabet, logo, watermark, signature, speech bubble, "
        "label, labels, tag, tags, paper tag, note, notes, sticky note, writing, inscription, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, cigarette, smoking, key ring, keys, pliers, entryway shelf, apron mending, sewing needle, thread, air purifier, filter, dust brush, "
        "tea drawer, pantry drawer, backup battery, battery dock, shoes, boots, shoe rack, parcel box, cooling fan, soldering iron, constellation clock, quiet timer, "
        "rain gauge, rooftop, laundromat, vending machine, phone, telephone, box, flower pot, photorealistic, gritty dark horror, plain white background, cluttered crowd, "
        "chibi proportions, super deformed, pixel art, low resolution pixels, asymmetrical eyes, distorted face, overexposed, muddy colors, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance_scale": 5.1,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": None,
    "save_to_disk": True,
    "filename": "ig_20260502_run1_moss_terrarium_fresh.webp",
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
webp_path = OUT_DIR / f"nyangdolsoe_moss_terrarium_nai_{seed}.webp"
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
