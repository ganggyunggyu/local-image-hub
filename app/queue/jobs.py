import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.models.manager import model_manager

executor = ThreadPoolExecutor(max_workers=1)


def _generate_sync(
    prompt: str,
    negative_prompt: str,
    width: int,
    height: int,
    steps: int,
    guidance_scale: float,
    seed: int | None,
    model: str,
) -> tuple[str, int]:
    """동기 이미지 생성 (ThreadPool에서 실행)"""
    return model_manager.generate(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        steps=steps,
        guidance_scale=guidance_scale,
        seed=seed,
        model=model,
    )


async def generate_image_job(ctx: dict, params: dict) -> dict:
    """SAQ 작업: 이미지 생성"""
    loop = asyncio.get_event_loop()

    image_base64, seed = await loop.run_in_executor(
        executor,
        _generate_sync,
        params["prompt"],
        params.get("negative_prompt", ""),
        params.get("width", 1024),
        params.get("height", 1024),
        params.get("steps", 28),
        params.get("guidance_scale", 4.0),
        params.get("seed"),
        params.get("model", "animagine-xl-4"),
    )

    result = {
        "success": True,
        "image_base64": image_base64,
        "seed": seed,
        "model": params.get("model", "animagine-xl-4"),
    }

    # 디스크 저장
    if params.get("save_to_disk", True):
        from base64 import b64decode
        from datetime import datetime
        from pathlib import Path

        outputs_dir = Path(__file__).parent.parent.parent / "outputs"
        outputs_dir.mkdir(exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        day_dir = outputs_dir / today
        day_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{params.get('model', 'animagine-xl-4')}_{timestamp}_{seed}.webp"
        filepath = day_dir / filename

        img_data = b64decode(image_base64)
        filepath.write_bytes(img_data)

        result["filename"] = f"{today}/{filename}"

    return result
