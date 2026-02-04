import os
import zipfile
from io import BytesIO
from base64 import b64encode
import random

import httpx


class NAIClient:
    BASE_URL = "https://image.novelai.net"

    MODELS = {
        "nai-v3": "nai-diffusion-3",
        "nai-v4": "nai-diffusion-4-curated-preview",
    }

    def __init__(self):
        self.token = os.getenv("NAI_TOKEN")
        if not self.token:
            raise ValueError("NAI_TOKEN not set in environment")

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 28,
        guidance_scale: float = 5.0,
        seed: int | None = None,
        model: str = "nai-v3",
    ) -> tuple[str, int]:
        if seed is None:
            seed = random.randint(0, 2147483647)

        model_name = self.MODELS.get(model, model)

        payload = {
            "input": prompt,
            "model": model_name,
            "action": "generate",
            "parameters": {
                "width": width,
                "height": height,
                "scale": guidance_scale,
                "sampler": "k_euler_ancestral",
                "steps": steps,
                "seed": seed,
                "n_samples": 1,
                "negative_prompt": negative_prompt,
                "qualityToggle": True,
                "ucPreset": 0,
            },
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.BASE_URL}/ai/generate-image",
                headers=self._get_headers(),
                json=payload,
            )
            response.raise_for_status()

            zip_data = BytesIO(response.content)
            with zipfile.ZipFile(zip_data, "r") as zf:
                image_name = zf.namelist()[0]
                image_data = zf.read(image_name)
                image_base64 = b64encode(image_data).decode("utf-8")

            return image_base64, seed

    def get_available_models(self) -> list[dict]:
        return [
            {"name": "nai-v3", "description": "NovelAI Diffusion V3"},
            {"name": "nai-v4", "description": "NovelAI Diffusion V4 (Preview)"},
        ]


nai_client: NAIClient | None = None


def get_nai_client() -> NAIClient:
    global nai_client
    if nai_client is None:
        nai_client = NAIClient()
    return nai_client
