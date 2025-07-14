import subprocess
from app.utils.config_loader import get_config

config = get_config()
subprocess.run(["git", "clone", config["whisperx"]["model_url"]], check=True)
print('model downloaded')
subprocess.run(["python3", "-m", "piper.download_voices", config["piper"]["voice"]], check=True)
print('voice downloaded')

