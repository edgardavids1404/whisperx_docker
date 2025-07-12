# app/routers/convert.py
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from app.services import media
from app.utils.config_loader import get_config
import asyncio
import pathlib

router = APIRouter(tags=["convert"], prefix="/media")

@router.post("/convert")
async def convert_media(
    bg: BackgroundTasks,
    file: UploadFile = File(...)
):
    src = media.save_upload(file)
    wav = await asyncio.get_event_loop().run_in_executor(None, media.convert_to_wav, src)
    bg.add_task(lambda p: pathlib.Path(p).unlink(missing_ok=True), src)  # clean tmp src
    return FileResponse(wav, media_type="audio/wav", filename="converted.wav")

@router.get("/media/{filename}")
async def get_media(filename: str):
    path = pathlib.Path(get_config()["tmp_dir"]) / filename
    if path.exists():
        return FileResponse(path.as_posix(), media_type="audio/wav")
    return {"error": "File not found"}
