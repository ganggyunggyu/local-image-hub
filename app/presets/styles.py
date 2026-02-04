"""
이미지 생성 스타일 프리셋
- 각 프롬프트는 CLIP 77토큰 제한을 고려하여 간결하게 작성
"""

STYLES = {
    "pale_aqua": {
        "name": "페일 아쿠아",
        "description": "투명 수채 + 연한 블루톤 + 깔끔한 선화 + 소프트 하이라이트",
        "prompt_suffix": "soft illustration, clean thin lineart, pale blue tones, light pastel colors, transparent watercolor shading, soft highlights, luminous skin, airy atmosphere, simple gradient background, delicate coloring, white and blue palette",
        "negative_suffix": "dark, gritty, harsh shadows, oversaturated, thick outlines, heavy shading, rough sketch, muddy colors, complex background, extra fingers, missing fingers, fused fingers, too many fingers, deformed hands, bad hands, malformed hands, wrong number of fingers, mutated hands, poorly drawn hands, six fingers",
        "recommended": {
            "steps": 32,
            "guidance_scale": 4.5,
        },
    },
    "cozy_gouache": {
        "name": "코지 과슈",
        "description": "러프 스케치 + 과슈 워시 + 뮤트 색상 + 따뜻한 분위기",
        "prompt_suffix": "rough sketch, gouache wash, muted colors, paper texture, cozy atmosphere, warm tones, visible brushstrokes",
        "negative_suffix": "clean lineart, digital, glossy, saturated, neon",
        "recommended": {
            "steps": 32,
            "guidance_scale": 5.0,
        },
    },
    "watercolor_sketch": {
        "name": "수채화 스케치",
        "description": "극세선 + 탈색 수채화 + 감성적",
        "prompt_suffix": "ultra fine lines, barely visible sketch, faint grey pencil, pale watercolor wash, washed out colors, desaturated, paper texture, melancholic, nostalgic atmosphere, soft diffused light, ethereal",
        "negative_suffix": "thick lines, bold outlines, heavy lineart, vibrant colors, saturated, high contrast, sharp, 3d, digital, text, signature",
        "recommended": {
            "steps": 35,
            "guidance_scale": 4.0,
        },
    },
    "kyoto_animation": {
        "name": "교토 애니메이션",
        "description": "섬세한 일상계, 부드러운 조명",
        "prompt_suffix": "kyoto animation, soft lighting, warm colors, gentle, detailed background",
        "negative_suffix": "harsh lighting, dark, gritty",
        "recommended": {
            "steps": 28,
            "guidance_scale": 5.0,
        },
    },
    "ufotable": {
        "name": "유포테이블",
        "description": "화려한 이펙트, 액션",
        "prompt_suffix": "ufotable, dynamic pose, glowing effects, dramatic lighting",
        "negative_suffix": "static, flat lighting",
        "recommended": {
            "steps": 30,
            "guidance_scale": 6.0,
        },
    },
    "shinkai": {
        "name": "신카이 마코토",
        "description": "배경 특화, 감성적인 하늘",
        "prompt_suffix": "makoto shinkai, beautiful sky, lens flare, atmospheric, cinematic",
        "negative_suffix": "simple background, flat colors",
        "recommended": {
            "steps": 32,
            "guidance_scale": 5.5,
        },
    },
    "ghibli": {
        "name": "지브리",
        "description": "따뜻한 색감, 자연, 노스탤지어",
        "prompt_suffix": "studio ghibli, warm colors, peaceful, nostalgic, nature",
        "negative_suffix": "dark, gritty, cyberpunk",
        "recommended": {
            "steps": 30,
            "guidance_scale": 5.0,
        },
    },
    "trigger": {
        "name": "트리거",
        "description": "과장된 액션, 화려한 색감",
        "prompt_suffix": "trigger style, dynamic angle, speed lines, colorful, energetic",
        "negative_suffix": "static, muted colors",
        "recommended": {
            "steps": 28,
            "guidance_scale": 6.0,
        },
    },
    "mappa": {
        "name": "맙파",
        "description": "다이나믹, 다크한 분위기",
        "prompt_suffix": "mappa style, cinematic lighting, dark atmosphere, intense",
        "negative_suffix": "bright, cheerful, flat",
        "recommended": {
            "steps": 30,
            "guidance_scale": 5.5,
        },
    },
    "shaft": {
        "name": "샤프트",
        "description": "독특한 연출, 기하학적 배경",
        "prompt_suffix": "shaft style, head tilt, abstract background, high contrast, artistic",
        "negative_suffix": "realistic background",
        "recommended": {
            "steps": 30,
            "guidance_scale": 6.0,
        },
    },
    "monogatari": {
        "name": "모노가타리 시리즈",
        "description": "샤프트 연출, 와타나베 아키오 스타일",
        "prompt_suffix": "monogatari series, shaft animation, full color, soft colors, clean lineart, head tilt, large expressive eyes, sharp eye highlights, flat color background",
        "negative_suffix": "sketch, lineart only, monochrome, greyscale, unfinished, rough, multiple views, 4koma, gradient background, oversaturated",
        "recommended": {
            "steps": 28,
            "guidance_scale": 5.5,
        },
    },
    "genshin": {
        "name": "원신",
        "description": "판타지, 원소 마법",
        "prompt_suffix": "genshin impact, fantasy, elemental magic, glowing, detailed outfit",
        "negative_suffix": "modern clothes, realistic",
        "recommended": {
            "steps": 28,
            "guidance_scale": 5.0,
        },
    },
    "blue_archive": {
        "name": "블루 아카이브",
        "description": "밝은 색감, 헤일로, 현대적",
        "prompt_suffix": "blue archive, halo, bright, cheerful, school, clean lines",
        "negative_suffix": "dark, gritty, fantasy",
        "recommended": {
            "steps": 28,
            "guidance_scale": 5.0,
        },
    },
    "arknights": {
        "name": "명일방주",
        "description": "디스토피아, 전술적",
        "prompt_suffix": "arknights, dystopian, industrial, dark atmosphere",
        "negative_suffix": "bright, cheerful",
        "recommended": {
            "steps": 30,
            "guidance_scale": 5.5,
        },
    },
    "fate": {
        "name": "페이트 시리즈",
        "description": "고귀함, 역사 판타지",
        "prompt_suffix": "fate series, noble, elegant, dramatic, historical fantasy",
        "negative_suffix": "modern, casual",
        "recommended": {
            "steps": 30,
            "guidance_scale": 5.5,
        },
    },
    "cyberpunk": {
        "name": "사이버펑크",
        "description": "네온, 미래적, 비오는 밤",
        "prompt_suffix": "cyberpunk, neon lights, futuristic, night, rain, high tech",
        "negative_suffix": "daytime, nature, fantasy",
        "recommended": {
            "steps": 30,
            "guidance_scale": 6.0,
        },
    },
    "pastel_soft": {
        "name": "파스텔 소프트",
        "description": "부드러운 파스텔, 몽글몽글",
        "prompt_suffix": "soft pastel colors, dreamy, soft shading, gentle, delicate",
        "negative_suffix": "harsh colors, high contrast, dark",
        "recommended": {
            "steps": 28,
            "guidance_scale": 5.0,
        },
    },
    "inuyasha": {
        "name": "이누야샤",
        "description": "90년대 레트로 애니, 몽환적이고 감성적인 분위기",
        "prompt_suffix": "90s anime aesthetic, inuyasha style, cel shaded, nostalgic, dreamy atmosphere, soft diffused lighting, feudal japan, hand-drawn feel, warm earthy tones, film grain",
        "negative_suffix": "modern anime, clean digital, 3d, photorealistic, neon colors, sharp lines",
        "recommended": {
            "steps": 32,
            "guidance_scale": 5.0,
        },
    },
    "sepia_backlit": {
        "name": "세피아 역광",
        "description": "연필 스케치 + 연한 수채화 + 세피아톤 + 역광",
        "prompt_suffix": "pencil sketch, light watercolor wash, sepia tones, backlit, soft glow, dreamy, paper texture, faded colors",
        "negative_suffix": "digital, saturated colors, dark, harsh shadows, clean lineart",
        "recommended": {
            "steps": 32,
            "guidance_scale": 5.0,
        },
    },
    "mono_accent": {
        "name": "모노톤 악센트",
        "description": "단색 모노톤 + 포인트 컬러 악센트",
        "prompt_suffix": "monochrome with color accent, limited palette, rough sketch, cyan tones, red accent, loose lineart, stylish",
        "negative_suffix": "full color, realistic, detailed shading, soft",
        "recommended": {
            "steps": 28,
            "guidance_scale": 6.0,
        },
    },
    "sketch_colorpop": {
        "name": "스케치 컬러팝",
        "description": "흑백 펜 스케치 + 컬러 악센트 + 해칭",
        "prompt_suffix": "black and white sketch, pen drawing, hatching, color pop accent, yellow highlight, rough lines, unfinished feel",
        "negative_suffix": "full color, clean lineart, digital, soft shading, polished",
        "recommended": {
            "steps": 28,
            "guidance_scale": 5.5,
        },
    },
    "pop_fanart": {
        "name": "팝 팬아트",
        "description": "굵은 선화 + 플랫 컬러 + 볼 홍조 + 심플 배경",
        "prompt_suffix": "bold outlines, flat coloring, vivid colors, blush on cheeks, nose highlight, simple white background, pop art style, clean",
        "negative_suffix": "sketch, rough, watercolor, gradient shading, complex background, realistic",
        "recommended": {
            "steps": 28,
            "guidance_scale": 5.5,
        },
    },
    "gyaru_peace": {
        "name": "갸루피스",
        "description": "갸루피스 포즈 특화, 손가락 품질 강화",
        "prompt_suffix": "close-up, upper body, bright lighting, cute, cheerful",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "double_peace": {
        "name": "더블피스",
        "description": "양손 피스, W피스 포즈",
        "prompt_suffix": "close-up, upper body, bright lighting, cheerful, energetic",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "ura_peace": {
        "name": "뒤집은 피스",
        "description": "裏ピース, 손등 보이는 피스",
        "prompt_suffix": "close-up, upper body, bright, cool",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "face_peace": {
        "name": "얼굴 가리기 피스",
        "description": "피스로 얼굴 일부 가리기",
        "prompt_suffix": "close-up, upper body, bright, cute, soft lighting",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "cheek_peace": {
        "name": "볼 피스",
        "description": "쭈키쭈키 포즈, 볼에 피스 대기",
        "prompt_suffix": "close-up, upper body, bright, cute, adorable",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "heart_hands": {
        "name": "하트 손",
        "description": "양손으로 하트 모양, 손가락 맞닿는 포즈",
        "prompt_suffix": "close-up, upper body, bright, soft lighting",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "cheek_heart": {
        "name": "볼하트",
        "description": "루다하트, 볼에 하트 만들기",
        "prompt_suffix": "close-up, upper body, bright, cute, lovely",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "finger_gun": {
        "name": "핑거건",
        "description": "손가락 총 포즈, 검지+엄지 강조",
        "prompt_suffix": "close-up, upper body, cool lighting, confident",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "cat_paw": {
        "name": "고양이 손",
        "description": "고양이 손 포즈, 구부린 손가락",
        "prompt_suffix": "close-up, upper body, cute, playful, bright",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "thumbs_up": {
        "name": "엄지척",
        "description": "엄지 올리기 포즈",
        "prompt_suffix": "close-up, upper body, bright, energetic",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
    "hand_wave": {
        "name": "손 흔들기",
        "description": "손 흔들며 인사, 펼친 손바닥",
        "prompt_suffix": "close-up, upper body, bright, friendly, warm",
        "negative_suffix": "extra fingers, missing fingers, fused fingers, deformed hands, bad hands, poorly drawn hands, wrong number of fingers, six fingers, mutated hands, malformed hands, twisted fingers",
        "recommended": {
            "steps": 35,
            "guidance_scale": 5.5,
        },
    },
}


def get_style(style_name: str) -> dict | None:
    """스타일 프리셋 가져오기"""
    return STYLES.get(style_name)


def list_styles() -> list[dict]:
    """모든 스타일 목록"""
    return [
        {"name": k, "display_name": v["name"], "description": v["description"]}
        for k, v in STYLES.items()
    ]


COMMON_NEGATIVE = (
    "extra fingers, fused fingers, deformed hands, poorly drawn hands, bad anatomy"
)


def apply_style(
    prompt: str, negative_prompt: str, style_name: str
) -> tuple[str, str, dict]:
    """프롬프트에 스타일 적용"""
    style = STYLES.get(style_name)
    if not style:
        return prompt, negative_prompt, {}

    styled_prompt = f"{prompt}, {style['prompt_suffix']}"

    negative_parts = [
        p for p in [negative_prompt, style["negative_suffix"], COMMON_NEGATIVE] if p
    ]
    styled_negative = ", ".join(negative_parts)

    return styled_prompt, styled_negative, style.get("recommended", {})
