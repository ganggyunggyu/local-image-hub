"""2010년대 쿄애니 스타일 캐릭터 5장 생성"""
import sys
sys.path.insert(0, "/Users/ganggyunggyu/Programing/local-image-llm")

from pathlib import Path
from base64 import b64decode
from app.models.manager import model_manager

OUTPUTS_DIR = Path("/Users/ganggyunggyu/Programing/local-image-llm/outputs/kyoani_2010")
OUTPUTS_DIR.mkdir(exist_ok=True)

KYOANI_BASE = """masterpiece, best quality, absurdres,
kyoto animation style, 2010s anime style,
soft lighting, warm colors, detailed eyes,
soft shading, gentle atmosphere, school setting"""

NEGATIVE = """lowres, bad anatomy, bad hands, text, error,
missing fingers, extra digit, fewer digits, cropped,
worst quality, low quality, normal quality, jpeg artifacts,
signature, watermark, username, blurry, nsfw"""

CHARACTERS = [
    {
        "name": "01_keion_style_guitarist",
        "prompt": f"{KYOANI_BASE}, 1girl, brown hair, short hair with bangs, amber eyes, school uniform, holding guitar, music room, cheerful expression, looking at viewer",
    },
    {
        "name": "02_hyouka_style_detective",
        "prompt": f"{KYOANI_BASE}, 1girl, long black hair, purple eyes, glasses, school uniform, library background, intelligent expression, holding book, elegant pose",
    },
    {
        "name": "03_clannad_style_gentle",
        "prompt": f"{KYOANI_BASE}, 1girl, long blonde hair, blue eyes, school uniform, cherry blossom background, gentle smile, wind blowing hair, spring atmosphere",
    },
    {
        "name": "04_kyoukai_style_megane",
        "prompt": f"{KYOANI_BASE}, 1girl, short pink hair, red eyes, red glasses, cardigan, rooftop background, sunset lighting, determined expression, dramatic lighting",
    },
    {
        "name": "05_tamako_style_cheerful",
        "prompt": f"{KYOANI_BASE}, 1girl, long purple hair in twintails, green eyes, casual clothes, shopping district background, happy expression, colorful scene, afternoon lighting",
    },
]

def main():
    print("Animagine XL 4.0 로딩 중...")
    model_manager.load_model("animagine-xl-4")
    print("모델 로드 완료!\n")

    for i, char in enumerate(CHARACTERS, 1):
        print(f"[{i}/5] {char['name']} 생성 중...")

        image_b64, seed = model_manager.generate(
            prompt=char["prompt"],
            negative_prompt=NEGATIVE,
            width=832,
            height=1216,
            steps=28,
            guidance_scale=5.0,
            model="animagine-xl-4",
        )

        filepath = OUTPUTS_DIR / f"{char['name']}_{seed}.png"
        filepath.write_bytes(b64decode(image_b64))
        print(f"  저장: {filepath.name}\n")

    print("완료!")
    model_manager.unload_model()

if __name__ == "__main__":
    main()
