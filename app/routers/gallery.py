from fastapi import APIRouter, Query

from app.gallery_store import index_outputs, search_images, stats

router = APIRouter(prefix="/api/gallery", tags=["gallery"])


@router.post("/index")
async def run_index() -> dict:
    return {"success": True, **index_outputs()}


@router.get("")
async def list_gallery(
    q: str | None = Query(default=None),
    model: str | None = Query(default=None),
    style: str | None = Query(default=None),
    batch_name: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> dict:
    return search_images(q=q, model=model, style=style, batch_name=batch_name, limit=limit, offset=offset)


@router.get("/stats")
async def gallery_stats() -> dict:
    return stats()
