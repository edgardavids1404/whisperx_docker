from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import convert, transcribe, tts, pipeline
from app.utils.config_loader import get_config

app = FastAPI(title="AV Pipeline API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

app.mount("/media", StaticFiles(directory=get_config()["tmp_dir"]), name="static_audio")

app.include_router(convert.router)
app.include_router(transcribe.router)
app.include_router(tts.router)
app.include_router(pipeline.router)
