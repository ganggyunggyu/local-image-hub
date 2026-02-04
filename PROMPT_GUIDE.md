# Animagine XL 4.0 프롬프트 가이드

## 기본 구조

```
[퀄리티 태그], [캐릭터 설명], [의상], [포즈/액션], [배경], [스타일]
```

## 퀄리티 태그 (필수)

### Positive (앞에 붙이기)
```
masterpiece, best quality, highres, absurdres
```

### Negative (항상 사용)
```
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name
```

---

## 캐릭터 기본

### 성별/나이
| 태그 | 설명 |
|------|------|
| `1girl` | 여성 1명 |
| `1boy` | 남성 1명 |
| `multiple girls` | 여러 여성 |
| `solo` | 혼자 (다른 캐릭터 없음) |

### 머리카락
| 태그 | 설명 |
|------|------|
| `long hair`, `short hair`, `medium hair` | 길이 |
| `black hair`, `blonde hair`, `blue hair`, `pink hair`, `white hair`, `silver hair` | 색상 |
| `twintails`, `ponytail`, `braid`, `bob cut`, `hime cut` | 스타일 |
| `hair ornament`, `hair ribbon`, `hairpin` | 장식 |

### 눈
| 태그 | 설명 |
|------|------|
| `blue eyes`, `red eyes`, `green eyes`, `golden eyes`, `heterochromia` | 색상 |
| `closed eyes`, `half-closed eyes` | 상태 |
| `sparkling eyes`, `glowing eyes` | 효과 |

### 표정
| 태그 | 설명 |
|------|------|
| `smile`, `grin`, `smirk` | 웃음 |
| `serious`, `expressionless`, `frown` | 진지 |
| `blush`, `embarrassed`, `shy` | 부끄러움 |
| `crying`, `tears`, `sad` | 슬픔 |
| `angry`, `annoyed` | 분노 |
| `surprised`, `shocked`, `open mouth` | 놀람 |

---

## 의상 카테고리

### 교복
```
school uniform, serafuku, sailor collar, pleated skirt, blazer, necktie, bow
```

### 사복/캐주얼
```
casual clothes, hoodie, t-shirt, jeans, shorts, skirt, dress, sweater, cardigan
```

### 판타지
```
armor, cape, cloak, robe, witch hat, crown, tiara, fantasy armor, knight
```

### 메이드/서비스
```
maid, maid headdress, apron, frills, waitress
```

### 수영복
```
swimsuit, bikini, one-piece swimsuit, school swimsuit
```

### 기타
```
kimono, yukata, chinese clothes, hanbok, gothic lolita, military uniform
```

---

## 포즈/액션

### 기본 포즈
| 태그 | 설명 |
|------|------|
| `standing`, `sitting`, `lying down` | 기본 자세 |
| `walking`, `running`, `jumping` | 동작 |
| `leaning forward`, `leaning back` | 기울기 |
| `kneeling`, `crouching`, `squatting` | 낮은 자세 |

### 손/팔 포즈
| 태그 | 설명 |
|------|------|
| `hands on hips`, `arms crossed` | 팔짱/허리 |
| `hand on chest`, `hand on face` | 손 위치 |
| `waving`, `peace sign`, `pointing` | 제스처 |
| `holding [물건]` | 물건 들기 |

### 시선/앵글
| 태그 | 설명 |
|------|------|
| `looking at viewer` | 정면 응시 |
| `looking away`, `looking to the side` | 시선 회피 |
| `from above`, `from below`, `from side` | 앵글 |
| `close-up`, `portrait`, `upper body`, `full body` | 구도 |

---

## 배경/환경

### 실내
```
indoors, classroom, bedroom, kitchen, bathroom, library, cafe, restaurant
```

### 실외
```
outdoors, street, park, beach, forest, mountain, city, rooftop, garden
```

### 시간/날씨
```
day, night, sunset, sunrise, cloudy, rainy, snowy, starry sky
```

### 특수 배경
```
simple background, white background, gradient background, blurred background
```

---

## 스타일/분위기

### 조명
```
soft lighting, dramatic lighting, backlighting, rim lighting, sunlight, moonlight
```

### 분위기
```
cinematic, atmospheric, ethereal, dreamy, dark, bright, colorful, monochrome
```

---

## 실전 프롬프트 예시

### 1. 교복 소녀 (기본)
```
Positive:
masterpiece, best quality, highres, 1girl, solo, school uniform, serafuku, pleated skirt, black hair, long hair, blue eyes, smile, looking at viewer, standing, classroom, sunlight, soft lighting

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

### 2. 판타지 마법사
```
Positive:
masterpiece, best quality, highres, 1girl, solo, witch, witch hat, long white hair, purple eyes, robe, cape, holding staff, magic, glowing, sparkles, dark forest, night, moonlight, mysterious, ethereal

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

### 3. 카페 일상
```
Positive:
masterpiece, best quality, highres, 1girl, solo, casual clothes, sweater, long brown hair, green eyes, smile, sitting, holding cup, coffee, cafe, window, warm lighting, cozy, relaxed

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

### 4. 사이버펑크
```
Positive:
masterpiece, best quality, highres, 1girl, solo, cyberpunk, neon lights, futuristic, short hair, blue hair, glowing eyes, jacket, headphones, city, night, rain, reflections, dramatic lighting

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

### 5. 꽃밭 소녀
```
Positive:
masterpiece, best quality, highres, 1girl, solo, white dress, long blonde hair, blue eyes, flower crown, standing, flower field, sunflowers, summer, blue sky, sunlight, peaceful, soft lighting

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

### 6. 전투 씬
```
Positive:
masterpiece, best quality, highres, 1girl, solo, armor, sword, long red hair, determined expression, battle stance, dynamic pose, action, wind, dramatic lighting, fire, sparks, intense

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

### 7. 겨울 일상
```
Positive:
masterpiece, best quality, highres, 1girl, solo, winter clothes, coat, scarf, mittens, black hair, red eyes, breath, snowing, street, night, city lights, warm, cozy

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

### 8. 아이돌/공연
```
Positive:
masterpiece, best quality, highres, 1girl, solo, idol, stage, microphone, pink hair, twintails, frilly dress, glowsticks, spotlight, concert, energetic, smile, wink, confetti

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

### 9. 고딕/다크
```
Positive:
masterpiece, best quality, highres, 1girl, solo, gothic lolita, black dress, long black hair, red eyes, pale skin, roses, thorns, dark, mansion, candles, mysterious, elegant

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

### 10. 해변/여름
```
Positive:
masterpiece, best quality, highres, 1girl, solo, bikini, long hair, wet hair, tanned skin, smile, beach, ocean, waves, summer, sunset, golden hour, sparkling water

Negative:
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```

---

## 팁

### 태그 순서
1. 퀄리티 태그
2. 캐릭터 수/성별
3. 외모 (머리, 눈)
4. 표정
5. 의상
6. 포즈/액션
7. 배경
8. 조명/분위기

### 가중치 조절
- `(tag:1.2)` - 강조 (1.1~1.5 권장)
- `(tag:0.8)` - 약화

### 주의사항
- 너무 많은 태그는 오히려 품질 저하
- 충돌하는 태그 피하기 (예: `day` + `night`)
- negative prompt는 항상 사용

---

## 권장 설정

| 항목 | 값 |
|------|-----|
| Steps | 28-35 |
| CFG | 5.0-7.0 |
| 해상도 | 832x1216 (세로), 1216x832 (가로), 1024x1024 (정사각) |
| Sampler | Euler a, DPM++ 2M Karras |
