# Image Gen Hub - 개발 가이드

## 프로젝트 개요

- **타입**: Python FastAPI REST API
- **용도**: 통합 이미지 생성 API (로컬 모델 + 클라우드 API)
- **패키지 매니저**: uv (pyproject.toml 기반)
- **Python 버전**: 3.10+

## 디렉토리 구조

```
app/
├── __init__.py
├── main.py              # FastAPI 앱 진입점
├── routers/
│   ├── __init__.py
│   └── generate.py      # API 라우터
├── models/
│   ├── __init__.py
│   └── manager.py       # 로컬 모델 매니저 (싱글톤)
├── providers/
│   ├── __init__.py
│   └── nai.py           # NovelAI API 클라이언트
└── schemas/
    └── __init__.py      # Pydantic 스키마
```

## Provider 시스템

| Provider | 설명 | 모델 |
|----------|------|------|
| `local` | 로컬 GPU/MPS 실행 | z-image, flux-schnell, sdxl |
| `nai` | NovelAI API | nai-v3, nai-v4 |

## 기술 스택

### 필수

- FastAPI 0.109+
- PyTorch 2.0+
- Diffusers 0.27+
- Transformers 4.38+
- Pydantic (스키마 검증)

### 개발 도구

- Ruff (린터/포매터)
- Pytest (테스트)

## 지원 모델

### 애니메이션/일러스트 특화 (추천)

| 모델                | Pipeline                    | VRAM   | 설명 |
| ------------------- | --------------------------- | ------ | ---- |
| `animagine-xl-4`    | StableDiffusionXLPipeline   | ~10GB  | 애니메이션 일러스트 특화, 태그 기반 |
| `pony-diffusion-v6` | StableDiffusionXLPipeline   | ~10GB  | 프롬프트 충실도 높음 |
| `illustrious-xl`    | StableDiffusionXLPipeline   | ~10GB  | 대규모 데이터셋 |

### 범용

| 모델              | Pipeline                    | VRAM   |
| ----------------- | --------------------------- | ------ |
| `z-image`         | ZImagePipeline              | ~16GB  |
| `z-image-turbo`   | ZImagePipeline              | ~12GB  |
| `flux-schnell`    | FluxPipeline                | ~12GB  |
| `sdxl`            | StableDiffusionXLPipeline   | ~8GB   |

## API 엔드포인트

- `POST /api/generate` - 이미지 생성
- `GET /api/models` - 모델 목록
- `POST /api/models/{name}/load` - 모델 로드
- `POST /api/models/unload` - 모델 언로드
- `GET /health` - 헬스 체크

## 개발 규칙

### Python 스타일

- Type hints 사용
- Pydantic BaseModel로 스키마 정의
- 구조분해할당 선호 (가능한 경우)

### API 규칙

- FastAPI Router로 엔드포인트 분리
- Pydantic Field로 검증 규칙 정의
- HTTPException으로 에러 처리

### 린팅

- Ruff 사용 (line-length: 100)
- select: E, F, I, W

## 실행 명령어

```bash
# 개발 서버
python -m app.main

# 또는
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

# 린트
ruff check .

# 포맷
ruff format .
```

## 환경 변수

- `PORT` - 서버 포트 (기본: 8002)
- `HOST` - 서버 호스트 (기본: 0.0.0.0)
- `HF_TOKEN` - HuggingFace 토큰
- `NAI_TOKEN` - NovelAI API 토큰
- `DEFAULT_MODEL` - 기본 모델
- `DEVICE` - 장치 (cuda/mps/cpu)

## 주의사항

- GPU VRAM 부족 시 모델 로드 실패 가능
- 모델은 한 번에 하나만 로드됨 (메모리 절약)
- CORS 전체 허용 상태 (개발용)
