import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"
DB_PATH = OUTPUTS_DIR / "metadata.sqlite"
IMAGE_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg"}


def _connect() -> sqlite3.Connection:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_db() -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS images (
                rel_path TEXT PRIMARY KEY,
                created_at TEXT,
                modified_at TEXT,
                file_size INTEGER,
                ext TEXT,
                model TEXT,
                seed INTEGER,
                style TEXT,
                provider TEXT,
                prompt TEXT,
                negative_prompt TEXT,
                width INTEGER,
                height INTEGER,
                steps INTEGER,
                guidance_scale REAL,
                lora TEXT,
                lora_scale REAL,
                batch_name TEXT,
                source_script TEXT,
                tags TEXT,
                meta_json TEXT
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_images_model ON images(model)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_images_style ON images(style)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_images_created_at ON images(created_at)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_images_batch ON images(batch_name)")
        conn.commit()
    finally:
        conn.close()


def _infer_basic(rel_path: str, image_path: Path) -> dict[str, Any]:
    name = image_path.stem
    stat = image_path.stat()

    model = None
    seed = None

    m = re.match(r"^(?P<model>.+?)_\d{6}_(?P<seed>\d+)$", name)
    if m:
        model = m.group("model")
        seed = int(m.group("seed"))
    else:
        m2 = re.match(r"^(?P<prefix>.+?)_(?P<seed>\d+)$", name)
        if m2:
            seed = int(m2.group("seed"))

    return {
        "rel_path": rel_path,
        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "file_size": stat.st_size,
        "ext": image_path.suffix.lower(),
        "model": model,
        "seed": seed,
        "batch_name": image_path.parent.name,
    }


def _read_sidecar(image_path: Path) -> dict[str, Any]:
    sidecar = image_path.with_suffix(image_path.suffix + ".json")
    if not sidecar.exists():
        return {}
    try:
        return json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception:
        return {}


def upsert_metadata(record: dict[str, Any]) -> None:
    ensure_db()
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT INTO images (
                rel_path, created_at, modified_at, file_size, ext,
                model, seed, style, provider, prompt, negative_prompt,
                width, height, steps, guidance_scale, lora, lora_scale,
                batch_name, source_script, tags, meta_json
            ) VALUES (
                :rel_path, :created_at, :modified_at, :file_size, :ext,
                :model, :seed, :style, :provider, :prompt, :negative_prompt,
                :width, :height, :steps, :guidance_scale, :lora, :lora_scale,
                :batch_name, :source_script, :tags, :meta_json
            )
            ON CONFLICT(rel_path) DO UPDATE SET
                created_at=excluded.created_at,
                modified_at=excluded.modified_at,
                file_size=excluded.file_size,
                ext=excluded.ext,
                model=excluded.model,
                seed=excluded.seed,
                style=excluded.style,
                provider=excluded.provider,
                prompt=excluded.prompt,
                negative_prompt=excluded.negative_prompt,
                width=excluded.width,
                height=excluded.height,
                steps=excluded.steps,
                guidance_scale=excluded.guidance_scale,
                lora=excluded.lora,
                lora_scale=excluded.lora_scale,
                batch_name=excluded.batch_name,
                source_script=excluded.source_script,
                tags=excluded.tags,
                meta_json=excluded.meta_json
            """,
            record,
        )
        conn.commit()
    finally:
        conn.close()


def index_outputs() -> dict[str, int]:
    ensure_db()
    indexed = 0
    failed = 0

    for image_path in OUTPUTS_DIR.rglob("*"):
        if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        rel_path = image_path.relative_to(OUTPUTS_DIR).as_posix()
        base = _infer_basic(rel_path, image_path)
        sidecar = _read_sidecar(image_path)

        tags = sidecar.get("tags")
        if isinstance(tags, list):
            tags_value = json.dumps(tags, ensure_ascii=False)
        elif isinstance(tags, str):
            tags_value = json.dumps([tags], ensure_ascii=False)
        else:
            tags_value = None

        record = {
            "rel_path": base["rel_path"],
            "created_at": sidecar.get("created_at", base["created_at"]),
            "modified_at": base["modified_at"],
            "file_size": base["file_size"],
            "ext": base["ext"],
            "model": sidecar.get("model", base.get("model")),
            "seed": sidecar.get("seed", base.get("seed")),
            "style": sidecar.get("style"),
            "provider": sidecar.get("provider"),
            "prompt": sidecar.get("prompt"),
            "negative_prompt": sidecar.get("negative_prompt"),
            "width": sidecar.get("width"),
            "height": sidecar.get("height"),
            "steps": sidecar.get("steps"),
            "guidance_scale": sidecar.get("guidance_scale"),
            "lora": sidecar.get("lora"),
            "lora_scale": sidecar.get("lora_scale"),
            "batch_name": sidecar.get("batch_name", base.get("batch_name")),
            "source_script": sidecar.get("source_script"),
            "tags": tags_value,
            "meta_json": json.dumps(sidecar, ensure_ascii=False) if sidecar else None,
        }

        try:
            upsert_metadata(record)
            indexed += 1
        except Exception:
            failed += 1

    return {"indexed": indexed, "failed": failed}


def search_images(
    q: str | None,
    model: str | None,
    style: str | None,
    batch_name: str | None,
    limit: int,
    offset: int,
) -> dict[str, Any]:
    ensure_db()
    where = []
    params: list[Any] = []

    if q:
        where.append("(rel_path LIKE ? OR prompt LIKE ? OR batch_name LIKE ?)")
        like = f"%{q}%"
        params.extend([like, like, like])
    if model:
        where.append("model = ?")
        params.append(model)
    if style:
        where.append("style = ?")
        params.append(style)
    if batch_name:
        where.append("batch_name = ?")
        params.append(batch_name)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    conn = _connect()
    try:
        total = conn.execute(
            f"SELECT COUNT(*) AS cnt FROM images {where_sql}",
            params,
        ).fetchone()["cnt"]

        rows = conn.execute(
            f"""
            SELECT rel_path, created_at, file_size, model, seed, style, provider, batch_name
            FROM images
            {where_sql}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            [*params, limit, offset],
        ).fetchall()

        items = [dict(r) for r in rows]
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": items,
        }
    finally:
        conn.close()


def stats() -> dict[str, Any]:
    ensure_db()
    conn = _connect()
    try:
        total = conn.execute("SELECT COUNT(*) AS cnt FROM images").fetchone()["cnt"]
        size = conn.execute("SELECT COALESCE(SUM(file_size),0) AS s FROM images").fetchone()["s"]
        by_model = [
            dict(r)
            for r in conn.execute(
                "SELECT COALESCE(model,'unknown') AS key, COUNT(*) AS count FROM images GROUP BY key ORDER BY count DESC LIMIT 20"
            ).fetchall()
        ]
        by_batch = [
            dict(r)
            for r in conn.execute(
                "SELECT COALESCE(batch_name,'unknown') AS key, COUNT(*) AS count FROM images GROUP BY key ORDER BY count DESC LIMIT 20"
            ).fetchall()
        ]
        return {
            "total_images": total,
            "total_size_mb": round(size / 1024 / 1024, 2),
            "by_model": by_model,
            "by_batch": by_batch,
            "db_path": str(DB_PATH),
        }
    finally:
        conn.close()
