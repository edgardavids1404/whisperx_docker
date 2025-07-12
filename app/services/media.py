import subprocess, uuid, pathlib, shutil
from app.utils.config_loader import get_config

def convert_to_wav(src_path: str, *, sr: int = 16000) -> str:
    config = get_config()
    dst = pathlib.Path(config["tmp_dir"]) / f"{uuid.uuid4()}.wav"
    cmd = [
        "ffmpeg", "-y", "-i", src_path,
        "-acodec", "pcm_s16le", "-ar", str(sr), "-ac", "1",
        dst.as_posix()
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return dst.as_posix()

def save_upload(upload_file) -> str:
    config = get_config()
    dst = pathlib.Path(config["tmp_dir"]) / f"{uuid.uuid4()}_{upload_file.filename}"
    with dst.open("wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return dst.as_posix()
