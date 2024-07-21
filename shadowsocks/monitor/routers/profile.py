import os
from pathlib import Path
from typing import Iterator
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import FileResponse, StreamingResponse

router = APIRouter()


@router.get("/profile/assets/{image_name}")
async def assets_png(image_name: str):
    try:
        p = Path(f"profile/assets/{image_name}")
        with open(str(p), "rb") as f:
            return Response(f.read(), media_type=f"image/{p.suffix[1:]}")
    except:
        raise HTTPException(404, detail=f"File not found {image_name}")


@router.get("/profile/download_resume")
async def download_pdf():
    resume_path = Path("profile/Otto_Resume2024.pdf")
    if not resume_path.is_file():
        raise HTTPException(404, detail=f"File not found {resume_path.name}")
    return FileResponse(
        str(resume_path),
        media_type="application/pdf",
        filename=resume_path.name,
    )


def iter_file(file_path: str, chunk_size: int = 1024 * 1024) -> Iterator[bytes]:
    with open(file_path, mode="rb") as file_like:
        while data := file_like.read(chunk_size):
            yield data


@router.get("/profile/media")
async def video_stream(request: Request, filename: str):
    file_path = f"profile/media/{filename}"
    p = Path(f"profile/media/{filename}")

    if not p.exists():
        raise HTTPException(404, detail="Video file not found")

    # 获取HTTP Range请求头
    range_header = request.headers.get("range")

    # 如果存在Range请求头，则进行部分内容响应
    if range_header:
        range_value = range_header.strip().strip("bytes=")
        range_start, range_end = range_value.split("-")
        range_start = int(range_start)
        range_end = int(range_end) if range_end else os.path.getsize(file_path) - 1

        chunk_size = range_end - range_start + 1
        with open(file_path, "rb") as f:
            f.seek(range_start)
            data = f.read(chunk_size)

        headers = {
            "Content-Range": f"bytes {range_start}-{range_end}/{os.path.getsize(file_path)}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(chunk_size),
            "Content-Type": f"video/{p.suffix[1:]}",
        }

        return Response(content=data, status_code=206, headers=headers)

    return StreamingResponse(iter_file(file_path), media_type=f"video/{p.suffix[1:]}")
