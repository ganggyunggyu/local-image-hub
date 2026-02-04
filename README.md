# Local Image LLM

로컬 이미지 생성 서버. Z-Image, FLUX, SDXL 등 여러 모델 지원.

## 요구사항

- Python 3.10+
- CUDA GPU (권장)
- 16GB+ VRAM (Z-Image full 모델 기준)

## 설치

```bash
# 가상환경 생성
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
```

## 실행

```bash
# 개발 모드
python -m app.main

# 또는
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

## API

### POST /api/generate

이미지 생성

```json
{
  "prompt": "anime girl, cherry blossom, masterpiece",
  "negative_prompt": "lowres, bad anatomy",
  "width": 1024,
  "height": 1024,
  "steps": 28,
  "guidance_scale": 4.0,
  "seed": null,
  "model": "z-image"
}
```

응답:

```json
{
  "success": true,
  "image_base64": "iVBORw0KGgo...",
  "seed": 12345678,
  "model": "z-image"
}
```

### GET /api/models

사용 가능한 모델 목록

### POST /api/models/{model_name}/load

모델 로드

### POST /api/models/unload

현재 모델 언로드

## 지원 모델

| 모델 | 설명 | VRAM |
|------|------|------|
| `z-image` | Tongyi Z-Image 고품질 | ~16GB |
| `z-image-turbo` | Z-Image 빠른 버전 (8 steps) | ~12GB |
| `flux-schnell` | FLUX.1 Schnell | ~12GB |
| `sdxl` | Stable Diffusion XL | ~8GB |

## x-bot 연동

x-bot에서 이 서버 호출:

```typescript
const response = await fetch('http://localhost:8002/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'anime girl',
    model: 'z-image'
  })
});

const { image_base64 } = await response.json();
const imageBuffer = Buffer.from(image_base64, 'base64');
```
# local-image-hub
