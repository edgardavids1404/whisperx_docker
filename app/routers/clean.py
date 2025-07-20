# app/routers/pipeline.py
import asyncio

from fastapi import APIRouter
from pydantic import BaseModel

from app.services import clean_srv

router = APIRouter(tags=["clean"])


class TextInput(BaseModel):
    text: str


@router.post("/clean")
async def pipeline(text: TextInput):
    cleaned = await asyncio.get_event_loop().run_in_executor(
        None, clean_srv.clean_text, text.text
    )

    return {"cleaned_text": cleaned}
