"""pop_fanart 프리셋 테스트 - 다양한 캐릭터 10장"""
import sys
sys.path.insert(0, "/Users/ganggyunggyu/Programing/local-image-llm")

from pathlib import Path
from base64 import b64decode
from app.models.manager import model_manager
from app.presets.styles import apply_style

OUTPUTS_DIR = Path("/Users/ganggyunggyu/Programing/local-image-llm/outputs")

CHARACTERS = [
    {"name": "pop_yui_guitar", "prompt": "1girl, solo, hirasawa yui, k-on!, brown hair, short hair, brown eyes, school uniform, holding guitar, smile, upper body"},
    {"name": "pop_miku_twintails", "prompt": "1girl, solo, hatsune miku, vocaloid, aqua twintails, aqua eyes, detached sleeves, headset, smile, upper body"},
    {"name": "pop_rem_maid", "prompt": "1girl, solo, rem, re:zero, blue hair, short hair, blue eyes, maid outfit, hair ribbon, upper body"},
    {"name": "pop_zero_two", "prompt": "1girl, solo, zero two, darling in the franxx, pink hair, long hair, green eyes, red uniform, horns, upper body, smile"},
    {"name": "pop_asuka_plugsuit", "prompt": "1girl, solo, asuka langley, neon genesis evangelion, orange hair, blue eyes, red plugsuit, confident expression, upper body"},
    {"name": "pop_chika_bow", "prompt": "1girl, solo, fujiwara chika, kaguya-sama, pink hair, blue eyes, school uniform, red bow, cheerful, upper body"},
    {"name": "pop_anya_smile", "prompt": "1girl, solo, anya forger, spy x family, pink hair, green eyes, school uniform, grin, upper body"},
    {"name": "pop_makima_tie", "prompt": "1girl, solo, makima, chainsaw man, red hair, long braids, ringed eyes, business suit, necktie, calm expression, upper body"},
    {"name": "pop_power_horns", "prompt": "1girl, solo, power, chainsaw man, blonde hair, long hair, yellow eyes, horns, sharp teeth, grin, upper body"},
    {"name": "pop_marin_gyaru", "prompt": "1girl, solo, kitagawa marin, sono bisque doll, blonde hair, long hair, blue eyes, gyaru, casual clothes, cheerful, upper body"},
]

NEGATIVE = "lowres, nsfw, bad anatomy"

def main():
    print("모델 로딩...")
    model_manager.load_model("animagine-xl-4")
    print("로드 완료!\n")

    for i, char in enumerate(CHARACTERS, 1):
        styled, neg, rec = apply_style(char["prompt"], NEGATIVE, "pop_fanart")
        print(f"[{i}/10] {char['name']}")

        img, seed = model_manager.generate(
            prompt=styled,
            negative_prompt=neg,
            width=1024,
            height=1024,
            steps=rec["steps"],
            guidance_scale=rec["guidance_scale"],
            model="animagine-xl-4",
        )

        filepath = OUTPUTS_DIR / f"{char['name']}_{seed}.webp"
        filepath.write_bytes(b64decode(img))
        print(f"  저장: {filepath.name}\n")

    print("10장 완료!")
    model_manager.unload_model()

if __name__ == "__main__":
    main()
