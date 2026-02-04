from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from saq import Queue

from app.queue import REDIS_URL
from app.queue.jobs import generate_image_job

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


class JobRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    negative_prompt: str = Field(default="")
    width: int = Field(default=1024, ge=256, le=2048)
    height: int = Field(default=1024, ge=256, le=2048)
    steps: int = Field(default=28, ge=1, le=100)
    guidance_scale: float = Field(default=4.0, ge=1.0, le=20.0)
    seed: int | None = Field(default=None)
    model: str = Field(default="animagine-xl-4")
    save_to_disk: bool = Field(default=True)


class JobResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: dict | None = None
    error: str | None = None


async def get_queue() -> Queue:
    queue = Queue.from_url(REDIS_URL)
    await queue.connect()
    return queue


@router.post("", response_model=JobResponse)
async def create_job(request: JobRequest) -> JobResponse:
    """비동기 이미지 생성 작업 생성"""
    queue = await get_queue()

    job = await queue.enqueue(
        generate_image_job.__name__,
        params=request.model_dump(),
    )

    await queue.disconnect()

    return JobResponse(
        job_id=job.id,
        status="queued",
    )


@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str) -> JobStatusResponse:
    """작업 상태 조회"""
    queue = await get_queue()

    job = await queue.job(job_id)
    await queue.disconnect()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    status_map = {
        "queued": "queued",
        "active": "processing",
        "complete": "completed",
        "failed": "failed",
        "aborted": "aborted",
    }

    return JobStatusResponse(
        job_id=job_id,
        status=status_map.get(job.status, job.status),
        result=job.result if job.status == "complete" else None,
        error=str(job.error) if job.error else None,
    )


@router.get("")
async def list_jobs():
    """큐 상태 조회"""
    queue = await get_queue()

    info = await queue.info()
    await queue.disconnect()

    return {
        "queue": info.get("name", "default"),
        "workers": info.get("workers", {}),
        "queued": info.get("queued", 0),
        "active": info.get("active", 0),
        "complete": info.get("complete", 0),
        "failed": info.get("failed", 0),
    }


@router.delete("/{job_id}")
async def cancel_job(job_id: str):
    """작업 취소"""
    queue = await get_queue()

    try:
        await queue.abort(job_id, error="Cancelled by user")
    except Exception as e:
        await queue.disconnect()
        raise HTTPException(status_code=404, detail=f"Job not found or cannot be cancelled: {e}")

    await queue.disconnect()

    return {"success": True, "job_id": job_id}
