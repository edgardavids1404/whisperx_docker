import yaml
from pathlib import Path

_config_cache = None

def get_config() -> dict:
    global _config_cache
    if _config_cache is None:
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        with open(config_path, "r") as f:
            _config_cache = yaml.safe_load(f)
    return _config_cache