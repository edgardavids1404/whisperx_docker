import subprocess, uuid, pathlib
from app.utils.config_loader import get_config

def text_to_speech(text: str) -> str:
    config = get_config() 
    dst = pathlib.Path(config["tmp_dir"]) / f"{uuid.uuid4()}.wav"
    cmd = [
        "piper",
        "--model", config["piper"]["voice"],
        "--output_file", dst.as_posix()
    ]
    proc = subprocess.run(cmd, input=text.encode(), check=True, capture_output=True)
    return dst.as_posix()