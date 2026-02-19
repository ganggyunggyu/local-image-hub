"""cozy_gouache 버전 비교 테스트"""
import asyncio
import httpx
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "cozy_compare"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_PROMPT = "1girl, frieren, sousou no frieren, white hair, elf ears, classroom, sitting at desk, sunset light through window, peaceful, masterpiece"

VERSIONS = [
    {
        "name": "gouache_texture",
        "suffix": "gouache texture, traditional media, bold ink strokes, watercolor wash, paper texture, expressive brushwork, muted tones"
    },
    {
        "name": "traditional_media",
        "suffix": "traditional media, gouache painting, visible brushstrokes, paper texture, warm tones, hand painted feel, textured surface"
    },
    {
        "name": "ink_gouache",
        "suffix": "ink and gouache, bold outlines, watercolor texture, rough paper, painted look, visible brush texture"
    },
]

async def generate(client, version):
    payload = {
        "prompt": f"{BASE_PROMPT}, {version['suffix']}",
        "negative_prompt": "low quality, worst quality, clean lineart, digital, glossy, neon, sharp edges, flat color",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "guidance_scale": 5.5,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "save_to_disk": False,
    }

    r = await client.post(API_URL, json=payload, timeout=180.0)
    data = r.json()
    if data.get("success") and data.get("image_base64"):
        seed = data.get("seed", 0)
        fp = OUTPUT_DIR / f"{version['name']}_{seed}.webp"
        fp.write_bytes(b64decode(data["image_base64"]))
        print(f"OK {version['name']}: {fp.name}")
    else:
        print(f"FAIL {version['name']}")

async def main():
    print("cozy 버전 비교 테스트")
    print("=" * 40)
    async with httpx.AsyncClient() as client:
        for v in VERSIONS:
            await generate(client, v)
            await asyncio.sleep(0.3)
    print("=" * 40)
    print(f"저장: {OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
