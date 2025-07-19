# app/routers/pipeline.py
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from app.services import clean_srv
import asyncio, pathlib

router = APIRouter(tags=["clean"])

@router.post("/clean")
async def pipeline(
    bg: BackgroundTasks,
    file: UploadFile = File(...)
):
    src = media.save_upload(file)
    wav = await asyncio.get_event_loop().run_in_executor(None, media.convert_to_wav, src)
    asr = await asyncio.get_event_loop().run_in_executor(None, whisperx_srv.transcribe, wav)
    cleaned = await asyncio.get_event_loop().run_in_executor(None, clean_srv.clean_text, " ".join(s["text"] for s in asr["segments"]))
    tts_wav = await asyncio.get_event_loop().run_in_executor(None, tts_srv.text_to_speech, cleaned)

    # clean temps afterwards
    bg.add_task(lambda p: pathlib.Path(p).unlink(missing_ok=True), src)
    bg.add_task(lambda p: pathlib.Path(p).unlink(missing_ok=True), wav)

    return {
            "cleaned_text": cleaned,
            "audio_path": str(tts_wav)
    }
