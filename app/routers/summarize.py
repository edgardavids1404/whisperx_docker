# app/routers/pipeline.py
import asyncio

from fastapi import APIRouter
from pydantic import BaseModel

from app.services import summarize_srv

router = APIRouter(tags=["summarize"])


class TextInput(BaseModel):
    text: str

@router.post("/summarize")
async def summarize(text: TextInput):
    summarized = await asyncio.get_event_loop().run_in_executor(
        None, summarize_srv.summarize_text, text.text
    )

    return {"summarized_text": summarized}
