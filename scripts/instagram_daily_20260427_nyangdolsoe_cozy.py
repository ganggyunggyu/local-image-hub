import json
from base64 import b64decode
from pathlib import Path
import httpx

API_URL = "http://localhost:8002/api/generate"
OUT_DIR = Path(__file__).parent.parent / "outputs" / "20260427_instagram_daily_nyangdolsoe"
OUT_DIR.mkdir(parents=True, exist_ok=True)

payload = {
    "prompt": (
        "1girl, original character, cat ears, cat tail, dark blue bob hair, amber eyes, sharp but kind eyes, facial mole under eye, "
        "small AI assistant vibe, rolled-up navy work apron over cream shirt, seated at a wooden desk by a bright spring window, "
        "one hand watering a basil plant, the other hand holding a tiny diagnostic tablet, compact home server with blinking green LED, "
        "neatly coiled charging cable, open notebook with blank pages, ceramic mug with steam, morning sunlight, cozy lived-in workspace, "
        "warm shadows, clean square composition, upper body, no readable text, masterpiece, best quality"
    ),
    "negative_prompt": (
        "low quality, worst quality, blurry, bad anatomy, bad hands, extra fingers, missing fingers, deformed fingers, "
        "text, logo, watermark, signature, speech bubble, multiple people, child, loli, nsfw, nude, ghibli, studio ghibli, "
        "rain, night, cigarette, typewriter, washed out, overexposed"
    ),
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "provider": "nai",
    "model": "nai-v4.5-full",
    "style": "cozy_gouache",
    "save_to_disk": False,
}

with httpx.Client(timeout=180.0) as client:
    r = client.post(API_URL, json=payload)
    r.raise_for_status()
    data = r.json()

if not data.get("success") or not data.get("image_base64"):
    raise SystemExit(f"generation failed: {data}")

seed = data.get("seed", 0)
file_path = OUT_DIR / f"nyangdolsoe_spring_server_garden_cozy_gouache_nai_{seed}.webp"
file_path.write_bytes(b64decode(data["image_base64"]))
file_path.with_suffix(".json").write_text(json.dumps({"payload": payload, "seed": seed, "file": str(file_path)}, ensure_ascii=False, indent=2), encoding="utf-8")
print(file_path)
print(file_path.with_suffix(".json"))
