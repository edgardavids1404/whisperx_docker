import uuid, pathlib
import wave
from app.utils.config_loader import get_config
from piper import PiperVoice

def text_to_speech(text: str) -> str:
    config = get_config() 
    dst = pathlib.Path(config["tmp_dir"]) / f"{uuid.uuid4()}.wav"
    voice = PiperVoice.load(config["piper"]["voice_path"])
    with open(dst, "wb") as f:
        with wave.open(f, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)
    return dst.as_posix()
