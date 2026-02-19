import asyncio
import os
from base64 import b64decode
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.schemas import GenerateRequest, GenerateResponse, ModelsResponse, ModelInfo
from app.models.manager import model_manager
from app.presets import apply_style, list_styles
from app.gallery_store import upsert_metadata

router = APIRouter(prefix="/api", tags=["generate"])

OUTPUTS_DIR = Path(__file__).parent.parent.parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def save_image(image_base64: str, seed: int, model: str, custom_filename: str | None = None) -> tuple[str, Path]:
    """이미지를 outputs/YYYY-MM-DD 폴더에 저장하고 (상대경로, 절대경로) 반환"""
    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = OUTPUTS_DIR / today
    day_dir.mkdir(exist_ok=True)

    if custom_filename:
        filename = f"{custom_filename}_{seed}.webp"
    else:
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{model}_{timestamp}_{seed}.webp"
    filepath = day_dir / filename

    img_data = b64decode(image_base64)
    filepath.write_bytes(img_data)

    return f"{today}/{filename}", filepath


async def generate_with_nai(request: GenerateRequest) -> tuple[str, int]:
    from app.providers.nai import get_nai_client

    client = get_nai_client()
    return await client.generate(
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        width=request.width,
        height=request.height,
        steps=request.steps,
        guidance_scale=request.guidance_scale,
        seed=request.seed,
        model=request.model,
    )


@router.post("/generate", response_model=GenerateResponse)
async def generate_image(request: GenerateRequest) -> GenerateResponse:
    try:
        prompt = request.prompt
        negative_prompt = request.negative_prompt
        steps = request.steps
        guidance_scale = request.guidance_scale

        # 스타일 적용
        if request.style:
            prompt, negative_prompt, recommended = apply_style(
                prompt, negative_prompt, request.style
            )
            if recommended:
                steps = recommended.get("steps", steps)
                guidance_scale = recommended.get("guidance_scale", guidance_scale)

        if request.provider == "nai":
            from app.providers.nai import get_nai_client

            nai_client = get_nai_client()
            image_base64, seed = await nai_client.generate(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=request.width,
                height=request.height,
                steps=steps,
                guidance_scale=guidance_scale,
                seed=request.seed,
                model=request.model,
            )
        else:
            image_base64, seed = await asyncio.to_thread(
                model_manager.generate,
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=request.width,
                height=request.height,
                steps=steps,
                guidance_scale=guidance_scale,
                seed=request.seed,
                model=request.model,
                lora=request.lora,
                lora_scale=request.lora_scale,
            )

        filename = None
        if request.save_to_disk:
            filename, saved_path = save_image(image_base64, seed, request.model, request.filename)
            try:
                metadata = {
                    "rel_path": filename,
                    "created_at": datetime.now().isoformat(),
                    "modified_at": datetime.now().isoformat(),
                    "file_size": saved_path.stat().st_size,
                    "ext": saved_path.suffix.lower(),
                    "model": request.model,
                    "seed": seed,
                    "style": request.style,
                    "provider": request.provider,
                    "prompt": request.prompt,
                    "negative_prompt": request.negative_prompt,
                    "width": request.width,
                    "height": request.height,
                    "steps": steps,
                    "guidance_scale": guidance_scale,
                    "lora": request.lora,
                    "lora_scale": request.lora_scale,
                    "batch_name": Path(filename).parent.as_posix(),
                    "source_script": None,
                    "tags": None,
                    "meta_json": None,
                }
                upsert_metadata(metadata)
            except Exception:
                pass

        return GenerateResponse(
            success=True,
            image_base64=image_base64,
            seed=seed,
            model=request.model,
            provider=request.provider,
            filename=filename,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        return GenerateResponse(
            success=False,
            image_base64=None,
            seed=request.seed or 0,
            model=request.model,
            provider=request.provider,
            error=str(e),
        )


@router.get("/models", response_model=ModelsResponse)
async def get_models() -> ModelsResponse:
    local_models = model_manager.get_available_models()
    models = [ModelInfo(**m, provider="local") for m in local_models]

    try:
        from app.providers.nai import get_nai_client

        nai = get_nai_client()
        for m in nai.get_available_models():
            models.append(ModelInfo(**m, provider="nai"))
    except ValueError:
        pass

    return ModelsResponse(
        available=models,
        current=model_manager.current_model,
    )


@router.post("/models/{model_name}/load")
async def load_model(model_name: str) -> dict:
    try:
        model_manager.load_model(model_name)
        return {"success": True, "model": model_name}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/unload")
async def unload_model() -> dict:
    model_manager.unload_model()
    return {"success": True}


@router.get("/styles")
async def get_styles() -> dict:
    """사용 가능한 스타일 프리셋 목록"""
    return {"styles": list_styles()}
