import subprocess
import whisperx
from app.utils.config_loader import get_config

print("Warming up: Downloading WhisperX model...")
config = get_config()
_ = whisperx.load_model(
    config["whisperx"]["model"],
    config["whisperx"]["device"],
    compute_type=config["whisperx"]["compute"]
)
print("Model downloaded successfully.")

piper_model = config["piper"]["voice"]

print(f"Warming up: Running Piper TTS with model {piper_model}...")
try:
    subprocess.run(
        ["bash", "-c", f"echo 'hello' | piper --model {piper_model} --output_file /tmp/smth.wav"],
        check=True
    )
    print("Piper TTS command completed.")
except subprocess.CalledProcessError as e:
    print(f"Error running Piper TTS: {e}")