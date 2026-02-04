import json
import random
import time
import urllib.request

BASE = "http://localhost:8002/api"
TOTAL = 100

ANIMATION_PRESETS = {
    "kyoto_animation",
    "ufotable",
    "shinkai",
    "ghibli",
    "trigger",
    "mappa",
    "shaft",
    "monogatari",
    "genshin",
    "blue_archive",
    "arknights",
    "fate",
    "cyberpunk",
    "inuyasha",
    "pastel_soft",
}

SCENES = [
    "sunset rooftop, warm wind",
    "rainy city street, neon reflections",
    "quiet library, afternoon light",
    "forest path, dappled sunlight",
    "cozy cafe, steam from coffee",
    "school hallway, soft ambient light",
    "train platform, golden hour",
    "night sky, milky way",
    "seaside cliff, ocean breeze",
    "urban alley, cinematic lighting",
    "festival street, lantern glow",
    "snowy field, gentle snowfall",
]

CHARACTERS = [
    "1girl, short hair, calm expression",
    "1girl, long hair, gentle smile",
    "1girl, twin tails, cheerful",
    "1girl, glasses, thoughtful",
    "1girl, hoodie, casual",
]

NEGATIVE = "ugly, blurry, deformed, extra fingers, bad anatomy, low quality, watermark, text, signature"


def get_json(url: str):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read().decode("utf-8"))


def post_json(url: str, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    styles = get_json(f"{BASE}/styles").get("styles", [])
    style_names = [s["name"] for s in styles if "name" in s]
    presets = [s for s in style_names if s in ANIMATION_PRESETS]
    if not presets:
        presets = style_names

    models = get_json(f"{BASE}/models")
    current = models.get("current")
    available = models.get("available", [])
    model = current or (available[0]["name"] if available else "z-image-turbo")

    for i in range(1, TOTAL + 1):
        preset = random.choice(presets)
        scene = random.choice(SCENES)
        char = random.choice(CHARACTERS)
        prompt = f"anime character, {char}, {scene}, masterpiece, best quality"
        filename = f"anim_{preset}_{i:03d}"
        payload = {
            "prompt": prompt,
            "negative_prompt": NEGATIVE,
            "style": preset,
            "model": model,
            "width": 832,
            "height": 1216,
            "steps": 28,
            "guidance_scale": 4.5,
            "save_to_disk": True,
            "filename": filename,
        }
        try:
            res = post_json(f"{BASE}/generate", payload)
            ok = res.get("success")
            seed = res.get("seed")
            out = res.get("filename")
            if ok:
                print(f"[{i:03d}/{TOTAL}] OK [{preset}] seed={seed} file={out}")
            else:
                print(f"[{i:03d}/{TOTAL}] FAIL [{preset}] {res.get('error')}")
        except Exception as e:
            print(f"[{i:03d}/{TOTAL}] ERROR [{preset}] {e}")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
