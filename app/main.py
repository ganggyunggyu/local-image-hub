import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv(Path(__file__).parent.parent / ".env")
from fastapi.middleware.cors import CORSMiddleware

from app.routers.generate import router as generate_router
from app.routers.jobs import router as jobs_router
from app.routers.gallery import router as gallery_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Local Image LLM Server starting...")
    yield
    print("👋 Server shutting down...")
    from app.models.manager import model_manager
    model_manager.unload_model()


app = FastAPI(
    title="Image Gen Hub",
    description="통합 이미지 생성 API - 로컬 모델 + 클라우드 API (NAI 등)",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_router)
app.include_router(jobs_router)
app.include_router(gallery_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import multiprocessing
    import uvicorn

    multiprocessing.set_start_method("fork", force=True)

    port = int(os.getenv("PORT", "8002"))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run("app.main:app", host=host, port=port, reload=True)
