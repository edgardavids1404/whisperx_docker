# app/routers/transcribe.py
import asyncio
import pathlib

from app.services import media, whisperx_srv
from fastapi import APIRouter, BackgroundTasks, File, UploadFile

router = APIRouter(tags=["transcribe"])


@router.post("/transcribe")
async def transcribe(bg: BackgroundTasks, file: UploadFile = File(...)):
    src = media.save_upload(file)
    wav = await asyncio.get_event_loop().run_in_executor(
        None, media.convert_to_wav, src
    )
    result = await asyncio.get_event_loop().run_in_executor(
        None, whisperx_srv.transcribe, wav
    )
    bg.add_task(lambda p: pathlib.Path(p).unlink(missing_ok=True), src)
    bg.add_task(lambda p: pathlib.Path(p).unlink(missing_ok=True), wav)
    return {
        "text": " ".join(seg["text"] for seg in result["segments"]),
        "segments": result["segments"],
    }
