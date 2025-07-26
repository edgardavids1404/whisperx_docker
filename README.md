# WhisperX STT + Text-cleaning + Summarization + PiperTTS

This project is a full-stack application providing a frontend in **Streamlit** and a **FastAPI** backend.

## Features

- Audio/Video to `.wav` format conversion.
- Audio file transcription using **WhisperX**.
- Text cleaning and summarization using **local ollama network**.
- Text-to-speech synthesis using **PiperTTS**.
- **FastAPI** backend for programmatic access.
- **Streamlit** frontend for easy user interaction.
- **Dockerfile** for ease of use.

## How to Use

1. In order to use the speaker-diarziation models, you need to accept user terms on the following links:
    - https://huggingface.co/pyannote/speaker-diarization-3.1
    - https://huggingface.co/pyannote/segmentation-3.0
2. Copy your huggingface access token.
3. Use the following command to build the docker image:
```
docker build -t stt-image .
```
OR, pull from dockerhub (if it exists):
```
docker pull edgardavids1404/whisperx_docker:latest && docker tag edgardavids1404/whisperx_docker:latest stt-image:latest
```
4. Use the following command. **Dont forget to paste your huggingface access token.**
```
docker run --name stt-container \
    --network ollama-network \
    -p 8501:8501 -p 8502:8502 \
    --gpus all \
    -e HF_TOKEN=your_huggingface_token \
    stt-image:latest
```

**NOTE:** 
- The network `ollama-network` assumes you have ollama running on another docker container, connected to a network called such.
- The port `8501` is the one used for streamlit and `8502` is the one used for FastAPI.
- You can edit the models used for inference in the `config.yaml` file.

## Backend FastAPI

This backend exposes several RESTful API endpoints.

### 🔄 `POST /media/convert`

Converts uploaded audio/video file to `.wav` format.

- Form Data:
    - `file`: audio file
- Response:
    - Returns `audio/wav` file named `converted.wav`.

### 🔊 `POST /transcribe`

Transcribes an uploaded audio file into text using WhisperX.

- Form Data:
    - `file`: audio file (e.g., `.mp3`, `.wav`)
- Response:
```json
{
    "text": "Full Transcript",
    "segments": [
        {
            "start": 0.0,
            "end": 3.2,
            "text": "First segment..."
        },
        ...
    ]
}
```

### 🧹 `POST /clean`

Cleans raw input text using LLM on local ollama server.

- Request Body:
```json
{
    "text": "Raw text input"
}
```
- Response:
```json
{
    "cleaned_text": "Cleaned version of the input"
}
```

### 📄 `POST /summarize`

Summarizes raw input text using LLM on local ollama server.

- Request Body:
```json
{
    "text": "Long text to be summarized"
}
```
- Response:
```json
{
    "summarized_text": "Shortened summary"
}
```
### 🗣️ `POST /tts`

Converts text into speech (TTS) and returns WAV file.

- Request Body:
```json
{
    "text": "This will be spoken"
}
```


