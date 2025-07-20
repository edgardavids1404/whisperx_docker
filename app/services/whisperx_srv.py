import whisperx, logging, torch, os
from app.utils.config_loader import get_config

# get configs
log = logging.getLogger(__name__)
config = get_config()

# GPU specific configs
gpu_mem = 0
if torch.cuda.is_available():
    gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
batch_size = 16 if gpu_mem > 8 else 2

# load models
_model = whisperx.load_model(
    config["whisperx"]["model_dir"],
    config["whisperx"]["device"],
    compute_type=config["whisperx"]["compute"]
)

def transcribe(wav_path: str) -> dict:

    # Step 1: load the audio
    audio = whisperx.load_audio(wav_path)

    # Step 2: transcribe the audio using faster-whisper model
    result = _model.transcribe(audio, batch_size=batch_size)

    # Step 3: align the segments
    _model_align, metadata = whisperx.load_align_model(
        language_code=config["language"],
        device=config["whisperx"]["device"]
        # model_name=config["whisperx"]["model_align_name"],
        # model_dir=config["whisperx"]["model_align_dir"]
    )

    result = whisperx.align(
        result["segments"],
        _model_align,
        metadata,
        audio,
        device=config["whisperx"]["device"],
        return_char_alignments=False
    )

    # Step 4: empty the torch cache
    torch.cuda.empty_cache()
    del _model_align

    # Step 5: Assign speakers
    _diarize_model = whisperx.diarize.DiarizationPipeline(
        # model_name=config["whisperx"]["model_diarization_name"],
        use_auth_token="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",
        device=config["whisperx"]["device"]
    )

    diarize_segments = _diarize_model(audio)
    result = whisperx.assign_word_speakers(diarize_segments, result)

    return result
