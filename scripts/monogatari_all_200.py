"""모노가타리 시리즈 전 캐릭터 x 전 프리셋 + 투샷/단체샷 200장"""

import asyncio
import httpx
import random
from datetime import datetime
from pathlib import Path
from base64 import b64decode

API_URL = "http://localhost:8002/api/generate"

TODAY = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / f"{TODAY}_monogatari_all"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 전체 프리셋
STYLES = [
    "pale_aqua", "mono_halftone", "chibi_sketch", "cozy_gouache",
    "watercolor_sketch", "kyoto_animation", "ufotable", "shinkai",
    "ghibli", "trigger", "mappa", "shaft", "monogatari",
    "genshin", "blue_archive", "arknights", "fate", "cyberpunk",
    "pastel_soft", "inuyasha", "sepia_backlit", "mono_accent",
    "sketch_colorpop", "pop_fanart", "split_sketch", "waterful",
    "bold_pop", "retro_glitch",
]

# 모노가타리 전 캐릭터
CHARS = {
    "hitagi": "senjougahara hitagi, monogatari, long purple hair, sharp eyes, tsundere",
    "hanekawa": "hanekawa tsubasa, monogatari, black hair, braids, glasses, gentle",
    "black_hanekawa": "black hanekawa, monogatari, white hair, cat ears, golden eyes, seductive",
    "shinobu": "oshino shinobu, monogatari, blonde hair, golden eyes, vampire, loli",
    "nadeko": "sengoku nadeko, monogatari, orange hair, bangs, shy, cute",
    "kanbaru": "kanbaru suruga, monogatari, short dark hair, athletic, tomboy",
    "hachikuji": "hachikuji mayoi, monogatari, twintails, backpack, ghost girl",
    "karen": "araragi karen, monogatari, long black hair, ponytail, tall, martial arts, tomboy",
    "tsukihi": "araragi tsukihi, monogatari, short black hair, kimono, cute, phoenix",
    "sodachi": "oikura sodachi, monogatari, light brown hair, twintails, sharp eyes, angry",
    "ougi": "oshino ougi, monogatari, short black hair, mysterious, dark outfit, enigmatic",
    "gaen": "gaen izuko, monogatari, short hair, cigarette, confident, mature",
    "yotsugi": "ononoki yotsugi, monogatari, green hair, hat, expressionless, doll",
    "araragi": "1boy, araragi koyomi, monogatari, black hair, ahoge, school uniform",
}

# 포즈 풀
POSES = [
    "head tilt, looking at viewer, upper body",
    "close up face, intense eyes",
    "side profile, elegant, upper body",
    "from below, looking down, confident",
    "back view, looking over shoulder",
    "sitting, crossed legs, relaxed",
    "lying down, looking at viewer",
    "dutch angle, dramatic, artistic",
    "wind, hair flowing, emotional",
    "night, moonlight, mysterious",
    "smirk, confident, cool",
    "gentle smile, warm lighting",
    "serious expression, dramatic shadow",
    "leaning, wall, casual, cool",
    "reading, focused, peaceful",
    "window, rain, melancholic",
    "sunset, silhouette, atmospheric",
    "walking, full body, dynamic",
]

JOBS = []

# 1. 각 캐릭터 x 랜덤 프리셋 (14캐릭터 x 4프리셋 = 56장)
for char_key, char_prompt in CHARS.items():
    selected_styles = random.sample(STYLES, 4)
    for style in selected_styles:
        pose = random.choice(POSES)
        is_boy = "1boy" in char_prompt
        prefix = char_prompt if is_boy else f"1girl, {char_prompt}"
        JOBS.append({
            "prompt": f"{prefix}, {pose}",
            "style": style,
            "name": f"{char_key}_{style}",
        })

# 2. 히타기 전 프리셋 (28장)
for style in STYLES:
    pose = random.choice(POSES)
    JOBS.append({
        "prompt": f"1girl, {CHARS['hitagi']}, {pose}",
        "style": style,
        "name": f"hitagi_full_{style}",
    })

# 3. 하네카와 전 프리셋 (28장)
for style in STYLES:
    pose = random.choice(POSES)
    JOBS.append({
        "prompt": f"1girl, {CHARS['hanekawa']}, {pose}",
        "style": style,
        "name": f"hanekawa_full_{style}",
    })

# 4. 투샷 (40장)
PAIRS = [
    ("hitagi", "araragi", "couple, romantic tension"),
    ("hanekawa", "araragi", "close, gentle, nostalgic"),
    ("shinobu", "araragi", "partners, back to back, bond"),
    ("nadeko", "araragi", "shy girl, blushing, one sided love"),
    ("kanbaru", "araragi", "playful, energetic, teasing"),
    ("karen", "araragi", "siblings, sparring, energetic"),
    ("tsukihi", "araragi", "siblings, peaceful, home"),
    ("karen", "tsukihi", "fire sisters, siblings, together, confident"),
    ("hitagi", "hanekawa", "rivals, friends, contrast, elegant"),
    ("hitagi", "kanbaru", "senpai kouhai, contrast"),
    ("hanekawa", "black_hanekawa", "same person, dual personality, mirror"),
    ("shinobu", "yotsugi", "supernatural, loli duo, contrast"),
    ("ougi", "araragi", "mysterious, dark, tension"),
    ("hachikuji", "araragi", "playful, comedy, greeting"),
    ("sodachi", "araragi", "intense, emotional, confrontation"),
    ("hitagi", "nadeko", "tension, jealousy, contrast"),
    ("karen", "kanbaru", "athletic, sporty, energetic"),
    ("gaen", "shinobu", "knowing, mysterious, supernatural"),
    ("hanekawa", "shinobu", "calm, bond, trust"),
    ("hitagi", "shinobu", "queen and princess, elegant"),
]

two_shot_styles = random.sample(STYLES, len(PAIRS))
for i, (c1, c2, mood) in enumerate(PAIRS):
    is_boy_1 = "1boy" in CHARS[c1]
    is_boy_2 = "1boy" in CHARS[c2]
    tag1 = CHARS[c1] if is_boy_1 else CHARS[c1]
    tag2 = CHARS[c2] if is_boy_2 else CHARS[c2]

    count_girls = sum(1 for c in [c1, c2] if "1boy" not in CHARS[c])
    count_boys = sum(1 for c in [c1, c2] if "1boy" in CHARS[c])
    prefix_parts = []
    if count_girls: prefix_parts.append(f"{count_girls}girls" if count_girls > 1 else "1girl")
    if count_boys: prefix_parts.append(f"{count_boys}boys" if count_boys > 1 else "1boy")
    prefix = ", ".join(prefix_parts)

    clean1 = tag1.replace("1boy, ", "")
    clean2 = tag2.replace("1boy, ", "")

    style = two_shot_styles[i % len(two_shot_styles)]
    JOBS.append({
        "prompt": f"{prefix}, {clean1}, {clean2}, {mood}, upper body",
        "style": style,
        "name": f"2shot_{c1}_{c2}_{style}",
    })

# 투샷 추가 20장 (인기 커플 다른 프리셋)
extra_pairs = [
    ("hitagi", "araragi"), ("hanekawa", "araragi"), ("shinobu", "araragi"),
    ("karen", "tsukihi"), ("hitagi", "hanekawa"), ("nadeko", "araragi"),
    ("kanbaru", "hitagi"), ("ougi", "araragi"), ("karen", "araragi"),
    ("hachikuji", "araragi"), ("hitagi", "shinobu"), ("hanekawa", "black_hanekawa"),
    ("shinobu", "yotsugi"), ("sodachi", "araragi"), ("karen", "kanbaru"),
    ("tsukihi", "araragi"), ("nadeko", "shinobu"), ("gaen", "ougi"),
    ("hitagi", "karen"), ("hanekawa", "nadeko"),
]
MOODS = ["emotional", "dramatic", "peaceful", "playful", "intense", "gentle", "mysterious", "nostalgic"]
for c1, c2 in extra_pairs:
    is_boy_1 = "1boy" in CHARS[c1]
    is_boy_2 = "1boy" in CHARS[c2]
    count_girls = sum(1 for c in [c1, c2] if "1boy" not in CHARS[c])
    count_boys = sum(1 for c in [c1, c2] if "1boy" in CHARS[c])
    prefix_parts = []
    if count_girls: prefix_parts.append(f"{count_girls}girls" if count_girls > 1 else "1girl")
    if count_boys: prefix_parts.append(f"{count_boys}boys" if count_boys > 1 else "1boy")
    prefix = ", ".join(prefix_parts)
    clean1 = CHARS[c1].replace("1boy, ", "")
    clean2 = CHARS[c2].replace("1boy, ", "")
    mood = random.choice(MOODS)
    style = random.choice(STYLES)
    JOBS.append({
        "prompt": f"{prefix}, {clean1}, {clean2}, {mood}, upper body",
        "style": style,
        "name": f"2shot_ex_{c1}_{c2}_{style}",
    })

# 5. 단체샷 (28장)
GROUP_SHOTS = [
    # 파이어 시스터즈
    {"prompt": "3people, 1boy 2girls, araragi koyomi, araragi karen, araragi tsukihi, monogatari, siblings, family, together, home", "name": "araragi_siblings"},
    {"prompt": "2girls, araragi karen, araragi tsukihi, monogatari, fire sisters, fighting pose, back to back, confident", "name": "fire_sisters_fight"},
    {"prompt": "2girls, araragi karen, araragi tsukihi, monogatari, fire sisters, casual, matching outfits, cute", "name": "fire_sisters_casual"},

    # 메인 히로인즈
    {"prompt": "3girls, senjougahara hitagi, hanekawa tsubasa, kanbaru suruga, monogatari, school friends, together", "name": "main_trio"},
    {"prompt": "5girls, senjougahara hitagi, hanekawa tsubasa, sengoku nadeko, kanbaru suruga, hachikuji mayoi, monogatari, heroines, group", "name": "main_heroines"},

    # 초자연 존재들
    {"prompt": "3girls, oshino shinobu, ononoki yotsugi, oshino ougi, monogatari, supernatural beings, mysterious, dark", "name": "supernatural_trio"},
    {"prompt": "2girls, oshino shinobu, ononoki yotsugi, monogatari, loli duo, contrast, supernatural", "name": "loli_duo"},

    # 전투 그룹
    {"prompt": "2girls, araragi karen, kanbaru suruga, monogatari, athletic, martial arts, sparring, dynamic", "name": "athletic_duo"},

    # 학교 그룹
    {"prompt": "3girls, senjougahara hitagi, hanekawa tsubasa, oikura sodachi, monogatari, classmates, school uniform, classroom", "name": "classmates"},

    # 뱀파이어 그룹
    {"prompt": "1girl 1boy, oshino shinobu, araragi koyomi, monogatari, vampire pair, moonlight, dramatic", "name": "vampire_pair"},

    # 대비샷
    {"prompt": "2girls, senjougahara hitagi, sengoku nadeko, monogatari, love rivals, tension, dramatic", "name": "rivals"},
    {"prompt": "2girls, hanekawa tsubasa, black hanekawa, monogatari, dual personality, mirror image, contrast", "name": "hanekawa_dual"},
]

for gs in GROUP_SHOTS:
    style = random.choice(STYLES)
    JOBS.append({
        "prompt": gs["prompt"],
        "style": style,
        "name": f"group_{gs['name']}_{style}",
    })

# 단체샷 다른 프리셋으로 추가
for gs in GROUP_SHOTS:
    style = random.choice(STYLES)
    JOBS.append({
        "prompt": gs["prompt"],
        "style": style,
        "name": f"group2_{gs['name']}_{style}",
    })

# 단체 추가 4장
EXTRA_GROUPS = [
    {"prompt": "6girls, senjougahara, hanekawa, shinobu, nadeko, kanbaru, karen, monogatari, all heroines, lineup, colorful", "name": "all_girls_lineup"},
    {"prompt": "3girls, senjougahara hitagi, hanekawa tsubasa, oshino shinobu, monogatari, top 3 heroines, elegant, dramatic", "name": "top3_heroines"},
    {"prompt": "2girls, oshino ougi, senjougahara hitagi, monogatari, mysterious, dark, confrontation", "name": "ougi_hitagi"},
    {"prompt": "4girls, karen, tsukihi, nadeko, hachikuji, monogatari, younger girls, cute, playful", "name": "younger_group"},
]
for eg in EXTRA_GROUPS:
    style = random.choice(STYLES)
    JOBS.append({
        "prompt": eg["prompt"],
        "style": style,
        "name": f"group3_{eg['name']}_{style}",
    })

# 200장으로 맞추기
JOBS = JOBS[:200]
TOTAL = len(JOBS)


async def generate(client, idx, job):
    payload = {
        "prompt": f"{job['prompt']}, masterpiece",
        "negative_prompt": "low quality, worst quality",
        "width": 832,
        "height": 1024,
        "steps": 28,
        "provider": "nai",
        "model": "nai-v4.5-full",
        "style": job["style"],
        "save_to_disk": False,
    }

    try:
        r = await client.post(API_URL, json=payload, timeout=180.0)
        data = r.json()
        if data.get("success") and data.get("image_base64"):
            seed = data.get("seed", 0)
            fp = OUTPUT_DIR / f"{idx:03d}_{job['name']}_{seed}.webp"
            fp.write_bytes(b64decode(data["image_base64"]))
            print(f"[{idx:03d}/{TOTAL}] OK {job['name']}")
            return True
        else:
            print(f"[{idx:03d}/{TOTAL}] FAIL {job['name']}: {data.get('error', '?')[:50]}")
            return False
    except Exception as e:
        print(f"[{idx:03d}/{TOTAL}] ERROR {job['name']}: {e}")
        return False


async def main():
    ok = fail = 0
    print(f"모노가타리 전 캐릭터 x 전 프리셋 {TOTAL}장")
    print(f"솔로: {14*4 + 28 + 28}장 / 투샷: {20+20}장 / 단체: {12*2+4}장")
    print(f"저장: {OUTPUT_DIR}")
    print("=" * 60)

    async with httpx.AsyncClient() as client:
        for i, job in enumerate(JOBS, 1):
            if await generate(client, i, job):
                ok += 1
            else:
                fail += 1
            await asyncio.sleep(0.3)

    print("=" * 60)
    print(f"완료! 성공: {ok}, 실패: {fail}")


if __name__ == "__main__":
    asyncio.run(main())
