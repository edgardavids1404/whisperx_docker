import subprocess

from app.utils.config_loader import get_config

config = get_config()

subprocess.run(["git", "clone", config["whisperx"]["model_url"]], check=True)
print("model downloaded")

# subprocess.run(["git", "clone", config["whisperx"]["model_align_url"]], check=True)
# print('alignment model downloaded')
#
# repo_url = config["whisperx"]["model_diarization_url"]
# hf_token = config["hf_token"]
# model_diarization_url = repo_url.replace("https://", f"https://user:{hf_token}@")
# subprocess.run(["git", "clone", config["whisperx"]["model_diarization_url"]], check=True)
# print('diaraziton model downloaded')
#
subprocess.run(
    ["python3", "-m", "piper.download_voices", config["piper"]["voice"]], check=True
)
print("voice downloaded")
