import json
from base64 import b64decode
from pathlib import Path
import httpx

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260428_instagram_daily_nyangdolsoe_run1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

payload = {
    "prompt": (
        "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, facial mole under eye, "
        "small AI assistant repair worker vibe, navy work apron over cream shirt, crouching in front of an apartment parcel locker control panel, "
        "tiny label printer with blank labels, relay board with one pink indicator LED, screwdriver, neatly bundled cable, metal locker doors, "
        "quiet basement utility room, monochrome halftone poster look with a single pink accent light, bold clean silhouette, square composition, "
        "no readable text, no logo, no watermark, masterpiece, best quality"
    ),
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, "
        "text, readable text, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, "
        "ghibli, studio ghibli, washing machine, coin changer, barcode scanner, rooftop, flower pot, cigarette, typewriter, rain, "
        "overexposed, cluttered composition"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": "mono_halftone",
    "save_to_disk": False,
}

with httpx.Client(timeout=240.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
file_path = OUT_DIR / f"nyangdolsoe_parcel_locker_mono_halftone_nai_{seed}.webp"
file_path.write_bytes(b64decode(data["image_base64"]))
file_path.with_suffix(".json").write_text(json.dumps({"payload": payload, "seed": seed, "file": str(file_path)}, ensure_ascii=False, indent=2), encoding="utf-8")
print(file_path)
print(file_path.with_suffix(".json"))
