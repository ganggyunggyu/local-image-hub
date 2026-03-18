# Image Gen Hub

로컬 GPU 또는 클라우드 API(NovelAI)로 이미지를 생성하는 통합 API 서버.
FastAPI 기반이며, 모델 전환/스타일 프리셋/LoRA/비동기 큐를 지원한다.

## 요구사항

- Python 3.10+
- CUDA GPU 또는 Apple Silicon (MPS)
- VRAM: 8GB~ (SDXL 기준) / 16GB~ (Z-Image full)

## 설치

```bash
# uv 사용 (권장)
uv sync

# 또는 pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 실행

```bash
# API 서버
make dev

# 비동기 워커 (SAQ + Redis)
make worker

# 서버 + 워커 동시 실행
make dev-all
```

서버 주소: `http://localhost:8002`

## 지원 모델

| 모델 | 파이프라인 | 설명 |
|------|-----------|------|
| `animagine-xl-4` | SDXL | 애니메이션 일러스트 특화 (기본값) |
| `noobai-xl` | SDXL | 캐릭터 인식 최강, 13M 학습 |
| `noobai-xl-vpred` | SDXL | v-prediction, 클린 출력 |
| `pony-diffusion-v6` | SDXL | 프롬프트 충실도 높음 |
| `illustrious-xl` | SDXL | 대규모 데이터셋 기반 |
| `z-image` | Z-Image | 고품질 다목적 |
| `z-image-turbo` | Z-Image | 빠른 생성 (8 steps) |
| `flux-schnell` | FLUX | 빠른 생성 (4 steps) |
| `flux-dev` | FLUX | 최고 품질 (비상업적) |
| `sdxl` | SDXL | 범용 기본 |

모델은 첫 요청 시 HuggingFace에서 자동 다운로드된다.

## 스타일 프리셋

`style` 파라미터로 프롬프트에 스타일을 자동 적용할 수 있다.

| 프리셋 | 설명 |
|--------|------|
| `pale_aqua` | 투명 수채 + 연한 블루톤 + 깔끔한 선화 |
| `cozy_gouache` | 러프 스케치 + 과슈 워시 + 뮤트 색상 |
| `watercolor_sketch` | 극세선 + 탈색 수채화 |
| `kyoto_animation` | 섬세한 일상계, 부드러운 조명 |
| `monogatari` | 샤프트 연출, 와타나베 아키오 스타일 |
| `zutomayo` | 몽환적 도시감 + 상징 소품 + 레이어드 콜라주형 J-pop MV 무드 |
| `prism_arcana` | 보라-분홍 발광 무대 + 음악선 같은 마법 궤적 + 손 뻗는 퍼포먼스 구도 |
| `opal_bloom` | 진주광 파스텔 + 투명 프릴/리본 + 로맨틱 블룸 무드 |
| `igeol_real` | 카톡 리액션 스티커풍 + 큰 둥근 얼굴 + 작은 O자 입 + 상단 글씨 자리 |
| `shinkai` | 배경 특화, 감성적인 하늘 |
| `ufotable` | 화려한 이펙트, 액션 |

외 18개 프리셋 추가 지원. `GET /api/styles`로 전체 목록 확인 가능.

## API

### `POST /api/generate`

이미지 생성

```json
{
  "prompt": "1girl, frieren, white hair, elf ears, mage robe",
  "negative_prompt": "lowres, bad anatomy",
  "width": 832,
  "height": 1216,
  "steps": 28,
  "guidance_scale": 4.0,
  "seed": null,
  "model": "animagine-xl-4",
  "provider": "local",
  "style": "pale_aqua",
  "lora": null,
  "lora_scale": 1.0,
  "save_to_disk": true,
  "filename": null
}
```

응답:

```json
{
  "success": true,
  "image_base64": "...",
  "seed": 12345678,
  "model": "animagine-xl-4",
  "provider": "local",
  "filename": "2026-02-04/animagine-xl-4_153012_12345678.webp"
}
```

### `GET /api/models`

사용 가능한 모델 목록

### `POST /api/models/{model_name}/load`

모델 로드

### `POST /api/models/unload`

현재 모델 언로드

### `GET /api/styles`

스타일 프리셋 목록

### `POST /api/jobs/submit`

비동기 작업 제출 (Redis + SAQ)

### `GET /api/jobs/{job_id}`

작업 상태 조회

### `GET /health`

헬스 체크

### `POST /api/gallery/index`

`outputs/` 폴더를 스캔해서 `outputs/metadata.sqlite` 메타 인덱스 생성/갱신

### `GET /api/gallery`

메타 인덱스 기반 이미지 검색

Query:
- `q` (파일경로/프롬프트/배치명 LIKE 검색)
- `model`, `style`, `batch_name`
- `limit` (기본 50), `offset`

### `GET /api/gallery/stats`

메타 통계 (전체 개수/용량, 모델별/배치별 카운트)

## LoRA

`loras/` 폴더에 `.safetensors` 파일을 넣고 요청 시 `lora` 파라미터로 지정.

```json
{
  "prompt": "...",
  "lora": "ClearHandsXL-v2.safetensors",
  "lora_scale": 0.8
}
```

## 배치 스크립트

`scripts/` 폴더에 배치 생성 스크립트가 있다. 서버가 실행 중인 상태에서 사용.

```bash
python scripts/pale_aqua_test.py
python scripts/zimage_anime.py
```

## Output 구조

생성된 이미지는 `outputs/` 폴더에 날짜별로 저장된다.

```
outputs/
├── 2026-02-04/
│   ├── animagine-xl-4_153012_1234567.webp
│   └── noobai-xl-vpred_160045_9876543.webp
├── 20260204_pale_aqua_v2/
│   └── v2_frieren_behind_1234567.webp
└── ...
```

## 프로젝트 구조

```
app/
├── main.py              # FastAPI 엔트리포인트
├── models/
│   └── manager.py       # 모델 로드/생성 관리
├── providers/
│   └── nai.py           # NovelAI API 클라이언트
├── presets/
│   └── styles.py        # 스타일 프리셋 (23개+)
├── queue/
│   ├── jobs.py          # 비동기 작업 핸들러
│   └── worker.py        # SAQ 워커
├── routers/
│   ├── generate.py      # 이미지 생성 엔드포인트
│   └── jobs.py          # 비동기 작업 큐 엔드포인트
└── schemas/
    └── __init__.py      # Pydantic 모델
scripts/                 # 배치 생성 스크립트
loras/                   # LoRA 어댑터
outputs/                 # 생성 이미지 저장
```

## 기술 스택

- **Framework**: FastAPI + Uvicorn
- **ML**: PyTorch, Diffusers, Transformers, Accelerate
- **Queue**: SAQ + Redis
- **Package Manager**: uv
