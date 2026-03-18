from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="이미지 생성 프롬프트")
    negative_prompt: str = Field(default="", description="네거티브 프롬프트")
    width: int = Field(default=1024, ge=256, le=2048)
    height: int = Field(default=1024, ge=256, le=2048)
    steps: int = Field(default=28, ge=1, le=100)
    guidance_scale: float = Field(default=4.0, ge=0.0, le=20.0)
    seed: int | None = Field(default=None, description="시드 값 (None이면 랜덤)")
    model: str = Field(default="animagine-xl-4", description="사용할 모델")
    provider: str = Field(default="nai", description="local, nai")
    style: str | None = Field(default=None, description="스타일 프리셋 (watercolor_sketch, kyoto_animation, etc.)")
    lora: str | None = Field(default=None, description="LoRA 파일명 (loras/ 폴더 기준, 확장자 포함)")
    lora_scale: float = Field(default=1.0, ge=0.0, le=5.0, description="LoRA 적용 강도")
    save_to_disk: bool = Field(default=True, description="outputs 폴더에 자동 저장")
    filename: str | None = Field(default=None, description="저장할 파일명 (확장자 제외, 키워드 기반)")


class GenerateResponse(BaseModel):
    success: bool
    image_base64: str | None = None
    seed: int
    model: str
    provider: str
    filename: str | None = None
    error: str | None = None


class ModelInfo(BaseModel):
    name: str
    loaded: bool = False
    description: str
    provider: str = "local"


class ModelsResponse(BaseModel):
    available: list[ModelInfo]
    current: str | None
