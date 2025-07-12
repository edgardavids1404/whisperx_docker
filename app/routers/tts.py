# app/routers/tts.py
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import FileResponse
from app.services import tts_srv
import asyncio

router = APIRouter(tags=["tts"])

class TextIn(BaseModel):
    text: str

@router.post("/tts")
async def tts_endpoint(body: TextIn):
    wav = await asyncio.get_event_loop().run_in_executor(None, tts_srv.text_to_speech, body.text)
    return FileResponse(wav, media_type="audio/wav", filename="speech.wav")
