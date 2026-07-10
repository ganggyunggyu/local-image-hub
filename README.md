# Image Gen Hub

로컬 GPU(diffusers)와 클라우드 API(NovelAI)를 하나의 FastAPI 서버 뒤에 묶어놓은 이미지 생성 허브다.

인스타그램 캐릭터 계정(냥냥돌쇠) 운영과 여러 애니메이션 캐릭터 팬아트 배치 생성을 하다 보니, 모델마다 다른 클라이언트/파라미터/후처리를 매번 따로 짜는 게 번거로웠다. SDXL 계열(animagine, noobai, pony, illustrious), Z-Image, FLUX 같은 로컬 모델과 NovelAI API를 같은 요청 스키마(`POST /api/generate`)로 호출하고, 스타일/캐릭터 프리셋으로 프롬프트를 재사용하고, 생성 결과를 나중에 검색할 수 있게 메타데이터까지 남기려고 만들었다.

## 주요 기능

- 로컬 GPU/MPS 모델과 NovelAI API를 동일한 요청 스키마로 호출 (`provider: "local" | "nai"`)
- SDXL, Z-Image, FLUX, NovelAI v3~v4.5 등 다양한 파이프라인을 모델 전환만으로 사용
- 프롬프트에 자동으로 적용되는 스타일 프리셋 43종 + 오리지널 캐릭터 프리셋
- LoRA 어댑터 로드/언로드 (`loras/*.safetensors`)
- SAQ + Redis 기반 비동기 작업 큐 (동기 호출이 부담스러운 배치 작업용)
- `outputs/` 폴더를 스캔해 SQLite로 메타데이터를 인덱싱하고 검색하는 갤러리 API
- 222개의 배치 생성 스크립트 (캐릭터 x 스타일 x 포즈 조합 대량 생성용)

## 기술 스택

- **Framework**: FastAPI, Uvicorn
- **ML**: PyTorch, Diffusers(HuggingFace 최신 git 버전), Transformers, Accelerate, Safetensors
- **Queue**: SAQ + Redis
- **HTTP Client**: httpx (NovelAI API 호출용)
- **Package Manager**: uv (pyproject.toml + uv.lock 기준), pip/requirements.txt도 지원
- **Lint/Test**: ruff, pytest (dev 의존성으로만 등록, 현재 테스트 코드는 없음)

## 아키텍처 / 폴더 구조

```
app/
├── main.py                 # FastAPI 엔트리포인트, CORS, lifespan에서 모델 언로드
├── gallery_store.py         # outputs/ 스캔 → SQLite 메타 인덱싱/검색
├── models/
│   └── manager.py           # 로컬 diffusers 파이프라인 로드/언로드/생성 (ModelManager)
├── providers/
│   └── nai.py                # NovelAI API 클라이언트 (v3~v4.5 payload 분기)
├── presets/
│   ├── styles.py              # 스타일 프리셋 43종
│   └── characters.py          # 오리지널 캐릭터 프리셋 (태그/네거티브/성격)
├── queue/
│   ├── jobs.py                 # SAQ 작업 핸들러 (동기 생성을 스레드풀에서 실행)
│   └── worker.py                # SAQ 워커 실행 엔트리포인트
├── routers/
│   ├── generate.py              # POST /api/generate, 모델/스타일 조회
│   ├── jobs.py                   # 비동기 작업 큐 API
│   └── gallery.py                 # 메타 인덱스 검색 API
└── schemas/                        # Pydantic 요청/응답 모델

scripts/    # 배치 생성 스크립트 (서버가 떠 있는 상태에서 httpx로 호출)
loras/      # LoRA 어댑터(.safetensors)
outputs/    # 생성 이미지 (날짜별 폴더) + metadata.sqlite
docs/       # NAI_PROMPT_GUIDE.md (NAI v4.5 프롬프트 가이드)
PROMPT_GUIDE.md  # Animagine XL 4.0 프롬프트 가이드
```

## 요구사항

- Python 3.10 이상
- CUDA GPU 또는 Apple Silicon (MPS). 로컬 모델을 안 쓰고 NovelAI만 쓸 거면 GPU 없이도 서버는 뜬다.
- VRAM: 8GB~ (SDXL 기준) / 16GB~ (Z-Image full)
- 비동기 작업 큐(`/api/jobs/*`)를 쓰려면 Redis 실행 필요

## 설치 및 실행

### 1. 저장소 클론 및 의존성 설치

```bash
git clone https://github.com/ganggyunggyu/local-image-hub.git
cd local-image-hub

# uv 사용 (권장, pyproject.toml + uv.lock 기준)
uv sync

# 또는 pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env.example`을 복사해서 `.env`를 만든다.

```bash
cp .env.example .env
```

```bash
# Server
PORT=8002
HOST=0.0.0.0

# HuggingFace (로컬 모델 다운로드용, private 모델 아니면 없어도 동작)
HF_TOKEN=your_huggingface_token

# Model Settings
DEFAULT_MODEL=animagine-xl-4
DEVICE=mps   # cuda / mps / cpu / auto

# Redis (SAQ Queue)
REDIS_URL=redis://localhost:6379/2
```

`.env.example`에는 없지만 `NAI_TOKEN` 값도 직접 추가해야 한다. `provider` 기본값이 `nai`라서(`app/schemas/__init__.py:13`), NovelAI 토큰 없이 `.env`만 복사해서 서버를 켜면 기본 요청부터 `NAI_TOKEN not set in environment` 에러가 난다(`app/providers/nai.py:22-24`). 로컬 모델만 쓸 거면 요청마다 `"provider": "local"`을 명시하면 된다.

```bash
# .env에 추가
NAI_TOKEN=your_novelai_token
```

### 3. 서버 실행

```bash
# API 서버만
make dev

# 비동기 워커만 (SAQ + Redis, Redis가 먼저 떠 있어야 함)
make worker

# 서버 + 워커 동시 실행
make dev-all
```

서버 주소: `http://localhost:8002`. `GET /health`로 기동 확인 가능.

### 4. 배치 스크립트 실행 (선택)

서버가 실행 중인 상태에서 `scripts/` 아래 스크립트를 그대로 실행하면 된다. 스크립트는 내부에서 `http://localhost:8002/api/generate`를 호출한다.

```bash
python scripts/pale_aqua_test.py
python scripts/zimage_anime.py
```

## 지원 모델

| 모델 | 파이프라인 | 설명 |
|------|-----------|------|
| `animagine-xl-4` | SDXL | 애니메이션 일러스트 특화 (로컬 기본값) |
| `noobai-xl` | SDXL | 캐릭터 인식 최강, 13M 학습 |
| `noobai-xl-vpred` | SDXL | v-prediction, 클린 출력 |
| `pony-diffusion-v6` | SDXL | 프롬프트 충실도 높음 |
| `illustrious-xl` | SDXL | 대규모 데이터셋 기반 |
| `z-image` | Z-Image | 고품질 다목적 |
| `z-image-turbo` | Z-Image | 빠른 생성 (8 steps) |
| `flux-schnell` | FLUX | 빠른 생성 (4 steps) |
| `flux-dev` | FLUX | 최고 품질 (비상업적) |
| `sdxl` | SDXL | 범용 기본 |
| `nai-v3` ~ `nai-v4.5-full` | NovelAI | `provider: "nai"`로 호출 (기본 provider) |

로컬 모델은 첫 요청 시 HuggingFace에서 자동 다운로드된다.

## 스타일 프리셋

`style` 파라미터로 프롬프트에 스타일을 자동 적용할 수 있다. 43개 중 일부:

| 프리셋 | 설명 |
|--------|------|
| `pale_aqua` | 투명 수채 + 연한 아쿠아톤 + 선명한 캐릭터 |
| `cozy_gouache` | 러프 스케치 + 과슈 워시 + 뮤트 색상 |
| `watercolor_sketch` | 극세선 + 탈색 수채화 |
| `kyoto_animation` | 섬세한 일상계, 부드러운 조명 |
| `monogatari` | 샤프트 연출, 와타나베 아키오 스타일 |
| `character_song_cover` | 미니멀 앨범커버 + 흰 배경 + 상반신 클로즈업 |
| `shinkai` | 배경 특화, 감성적인 하늘 |
| `ufotable` | 화려한 이펙트, 액션 |

전체 목록은 `GET /api/styles`로 확인.

## API

### `POST /api/generate`

이미지 생성.

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

### 그 외 엔드포인트

| 엔드포인트 | 설명 |
|-----------|------|
| `GET /api/models` | 로컬 + NAI 사용 가능 모델 목록 |
| `POST /api/models/{model_name}/load` | 모델 로드 |
| `POST /api/models/unload` | 현재 모델 언로드 |
| `GET /api/styles` | 스타일 프리셋 목록 |
| `POST /api/jobs` | 비동기 작업 제출 (Redis + SAQ) |
| `GET /api/jobs/{job_id}` | 작업 상태 조회 |
| `DELETE /api/jobs/{job_id}` | 작업 취소 |
| `POST /api/gallery/index` | `outputs/` 스캔해서 메타 인덱스 생성/갱신 |
| `GET /api/gallery` | 메타 인덱스 기반 이미지 검색 (`q`, `model`, `style`, `batch_name`, `limit`, `offset`) |
| `GET /api/gallery/stats` | 메타 통계 (전체 개수/용량, 모델별/배치별 카운트) |
| `GET /health` | 헬스 체크 |

## LoRA

`loras/` 폴더에 `.safetensors` 파일을 넣고 요청 시 `lora` 파라미터로 지정한다.

```json
{
  "prompt": "...",
  "lora": "ClearHandsXL-v2.safetensors",
  "lora_scale": 0.8
}
```

## Output 구조

생성된 이미지는 `outputs/` 폴더에 날짜별로 저장되고, `metadata.sqlite`에 인덱싱된다.

```
outputs/
├── 2026-02-04/
│   ├── animagine-xl-4_153012_1234567.webp
│   └── noobai-xl-vpred_160045_9876543.webp
├── 20260204_pale_aqua_v2/
│   └── v2_frieren_behind_1234567.webp
├── metadata.sqlite
└── ...
```

## 트러블슈팅

### NAI 미지원 모델을 요청하면 이미지 생성이 실패했다

`provider`를 `nai`로 호출할 때 `model` 값이 `NAIClient.MODELS`에 없는 로컬 전용 모델명(기본값 `animagine-xl-4` 등)으로 그대로 넘어오는 경우가 있었다. NovelAI API는 모르는 모델명을 그대로 거부하기 때문에 요청이 실패했다.

`app/routers/generate.py:76-77`에서 요청한 `model`이 NAI가 지원하는 목록에 없으면 `nai-v4.5-full`로 강제 폴백하도록 고쳤고, 동시에 `app/schemas/__init__.py:13`에서 기본 `provider`를 `local`에서 `nai`로 바꿨다. 로컬 GPU보다 NAI API 호출이 주력 경로가 되면서, 모델명을 명시하지 않은 요청도 안전하게 NAI로 흘러가게 맞춘 것이다.

```python
# app/routers/generate.py
nai_client = get_nai_client()
if request.model not in nai_client.MODELS:
    request.model = "nai-v4.5-full"
```

### `pale_aqua` 프리셋으로 생성한 캐릭터 피부가 파랗게 나왔다

`pale_aqua` 스타일의 `prompt_suffix`에 있던 `"pale blue tones"`라는 표현이 문제였다. 의도는 "은은한 블루톤 분위기"였는데, 모델은 이걸 "피부색 자체를 파랗게 칠하라"는 지시로 해석하는 경우가 많았다. 결과물의 캐릭터 얼굴/피부가 실제로 푸르스름하게 나오는 현상이 반복됐다.

`app/presets/styles.py`의 `pale_aqua` 항목에서 표현을 `"light aqua tint"`로 순화하고, positive 쪽에 `"sharp face details, clear eyes, defined features, natural skin tones"`를 추가했다. negative에는 `"blue skin, unnatural coloring, monochrome blue"`를 넣어 억제했고, `steps`는 32에서 28로, `guidance_scale`은 4.5에서 5.5로 조정해 프롬프트를 더 충실히 따르게 했다.

```python
# app/presets/styles.py, "pale_aqua"
"prompt_suffix": "... light aqua tint, ... sharp face details, clear eyes, defined features, natural skin tones",
"negative_suffix": "... blurry, out of focus, fuzzy, unfocused face, blue skin, unnatural coloring, monochrome blue, ...",
"recommended": {"steps": 28, "guidance_scale": 5.5},
```

같은 커밋에서 `chibi_sketch`, `cozy_gouache`, `split_sketch` 등 다른 프리셋도 결과물이 의도와 다르게 나오는 문제를 프롬프트 재작성으로 고쳤고, steps 값이 프리셋마다 28~35로 제각각이던 걸 28로 통일해서 생성 시간 편차를 줄였다.

### Apple Silicon(MPS)에서 모델마다 결과가 다르게 깨졌다

같은 파이프라인 로드 로직을 MPS 기기에 그대로 적용하면 모델 계열마다 다른 방식으로 문제가 생겼다. Z-Image의 VAE를 다른 가중치와 같이 float16으로 내리면 노이즈가 심하게 꼈고, 반대로 파이프라인 전체를 float32로 올리면 z-image(비-turbo)는 MPS 메모리를 넘겨서 죽었다. FLUX는 그 반대로 float32를 쓰면 속도가 크게 떨어졌다.

`app/models/manager.py`에서 디바이스/파이프라인 조합별로 분기 처리해 해결했다.

- FLUX는 MPS에서 `float16`, 나머지 파이프라인은 `float32`로 로드 (`app/models/manager.py:135-137`)
- MPS + non-FLUX 조합에서는 VAE만 따로 `float32`로 강제 캐스팅 (`app/models/manager.py:157-158`)
- `z-image`(non-turbo)는 float32 풀사이즈가 MPS 메모리를 초과해서 `enable_model_cpu_offload`로 전환 (`app/models/manager.py:160-170`)
- `z-image` 생성 시 `cfg_normalization=False`를 강제하지 않으면 결과물이 깨짐 (`app/models/manager.py:256-257`)

## 알려진 제약사항

- **`app/models/manager.py`가 git에 올라간 적이 없다.** `.gitignore`의 `models/` 규칙은 다운로드되는 모델 가중치 캐시 폴더를 무시하려던 의도였는데, 경로 깊이와 무관하게 매칭되는 바람에 `app/models/` 디렉터리(소스 코드 포함)까지 함께 가려버렸다. `git ls-files app/`로 확인하면 `app/models/manager.py`, `app/models/__init__.py`가 아예 빠져 있다. 이 저장소를 새로 클론하면 `app/main.py:21`, `app/routers/generate.py:10`, `app/queue/jobs.py:4`의 `from app.models.manager import model_manager`에서 바로 `ImportError`가 난다. `.gitignore`를 `/models/`처럼 루트 기준 절대 경로로 바꾸거나 `app/models/`를 예외 처리해야 한다.
- `.env.example`에 `HF_TOKEN`, `DEFAULT_MODEL` 항목이 있지만 실제 코드 어디에서도 읽지 않는다(죽은 설정값). 반대로 실제로 필요한 `NAI_TOKEN`은 `.env.example`에 없다.
- 테스트 코드가 없다. `pyproject.toml`에 `pytest`가 dev 의존성으로 등록만 되어 있고 테스트 파일은 존재하지 않는다.
- 비동기 큐(`/api/jobs/*`)와 워커는 이미지 생성 결과를 개별 job 상태로만 들고 있고, `outputs/` 메타 인덱스(`gallery_store.py`)에는 자동으로 반영되지 않는다. `/api/generate`(동기 경로)만 생성 시 메타데이터를 자동 기록한다.
- SAQ 워커는 GPU 특성상 `concurrency=1`로 고정되어 있어, 대량 배치는 순차 처리된다.
