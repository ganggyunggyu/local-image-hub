# NAI V4.5 프롬프트 가이드

## 태그 순서 (권장)
1. 인물 수/종류 (1girl, 2boys, solo)
2. 캐릭터/작품명 (frieren, sousou no frieren)
3. 작가 태그 (artist:mika pikazo)
4. 품질/미학 태그 (masterpiece, very aesthetic)
5. 아트 스타일/매체 (watercolor, sketch)
6. 구도/카메라 (upper body, from above)
7. 배경/장소 (forest, indoor)
8. 인물 외형 (white hair, green eyes)
9. 의상 (school uniform, dress)
10. 자세/표정 (sitting, smile)
11. 기타 디테일

## 가중치 문법
```
# 강조 (1.0 이상)
1.5::rain, night::

# 약화 (1.0 미만)
0.5::coat::

# 음수 가중치 (개념 제거/반전)
-1::monochrome::  # 색상 되살리기
-2::flat color::   # 디테일 추가
-1::hat::          # 모자 제거
```

## 다중 인물 상호작용
```
# A가 B를 껴안음
캐릭터 A: source#hug
캐릭터 B: target#hug

# 서로 껴안음
캐릭터 A: mutual#hug
캐릭터 B: mutual#hug
```

## 권장 설정
- Guidance: 5-6 (V4.5는 낮은 값 권장)
- Steps: 28
- Normal Size: 832x1216 이하 (Opus 무료)

## 잘 뽑히는 스타일 프리셋 (메모)
- `monogatari`
- `blue_archive`
- `kyoto_animation`
- `chibi_sketch`
- `mono_halftone`

## 네거티브 프롬프트 필수
```
low quality, worst quality, bad anatomy, deformed hands, blurry
```

## 프롬프트 예시

### Before (비효율적)
```
3girls, multiple series crossover, lead guitarists gathering, music studio, electric guitars, (hirasawa yui, k-on!, brown hair), masterpiece, best quality
```

### After (최적화)
```
3girls, hirasawa yui, gotoh hitori, kawaragi momoka, masterpiece, very aesthetic, music studio, 1.2::electric guitars::, brown hair, pink hair, silver hair, sitting
```
