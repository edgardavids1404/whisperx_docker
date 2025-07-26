from tempfile import NamedTemporaryFile

import requests
import streamlit as st

API_BASE = "http://localhost:8502"

st.set_page_config(page_title="AV Pipeline", layout="centered")

st.title("🎙️ Audio/Video → Text → Cleaned Text → Summarization → Text-to-Speech")

# Session state to share transcript between tabs
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "cleaned_text" not in st.session_state:
    st.session_state.cleaned_text = ""
if "summarized_text" not in st.session_state:
    st.session_state.summarized_text = ""

tab1, tab2, tab3, tab4 = st.tabs([
        "🔊 Transcription", 
        "🧹  Text Cleaner", 
        "📋 Summarization", 
        "🔈  Text to Speech"
    ])

# --- Tab 1: Transcription ---
with tab1:
    uploaded_file = st.file_uploader(
        "Upload audio/video file", type=["mp4", "mp3", "wav"]
    )

    if uploaded_file:
        st.audio(uploaded_file, format="audio/wav")

        if st.button("Transcribe"):
            with st.spinner("Processing..."):
                # Save locally then send to FastAPI
                with NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                with open(tmp_path, "rb") as f:
                    files = {"file": (uploaded_file.name, f, uploaded_file.type)}
                    r = requests.post(f"{API_BASE}/transcribe", files=files, timeout=1200)

                if r.status_code != 200:
                    st.error("Pipeline failed!")
                else:
                    res = r.json()
                    st.subheader("💬 Transcript by Speaker")

                    full_text = ""
                    segments = res.get("segments", [])
                    if not segments:
                        st.warning("No segments returned.")
                    else:
                        for seg in segments:
                            start = seg.get("start", 0)
                            end = seg.get("end", 0)
                            speaker = seg.get("speaker", "Unknown")
                            text = seg.get("text", "")

                            # Format timestamps
                            start_ts = f"{int(start // 60):02}:{int(start % 60):02}"
                            end_ts = f"{int(end % 60):02}:{int(end % 60):02}"

                            st.markdown(
                                f"**[{start_ts} - {end_ts}] {speaker}:** {text}"
                            )
                            full_text += f"{speaker}: {text}\n"

                    # Save full text to session state for Tab 2
                    st.session_state.transcribed_text = full_text.strip()

# --- Tab 2: Text Cleaner ---
with tab2:
    st.subheader("🧼 Clean your Text")
    input_text_toclean = st.text_area(
        "Input text to clean", value=st.session_state.transcribed_text, height=300
    )

    if st.button("Clean Text"):
        with st.spinner("Cleaning..."):
            response = requests.post(f"{API_BASE}/clean", json={"text": input_text_toclean}, timeout=1200)
            if response.status_code == 200:
                cleaned = response.json().get("cleaned_text", "")
                st.session_state.cleaned_text = cleaned.strip()
                st.subheader("✅ Cleaned Output")
                st.text_area("Cleaned Text", value=cleaned, height=300)
            else:
                st.error("Cleaning failed.")

# --- Tab 3: Text Summarization ---
with tab3:
    st.subheader("📋Summarize your Text")
    input_text_tosummarize = st.text_area(
        "Input text to summarize", value=st.session_state.cleaned_text, height=300
    )

    if st.button("Summarize Text"):
        with st.spinner("Summarizing..."):
            response = requests.post(f"{API_BASE}/summarize", json={"text": input_text_tosummarize}, timeout=1200)
            if response.status_code == 200:
                summarized = response.json().get("summarized_text", "")
                st.session_state.summarized_text = summarized.strip()
                st.subheader("✅Summarized Output")
                st.text_area("Summarized Text", value=summarized, height=300)
            else:
                st.error("Summarization failed.")

# --- Tab 4: Text-to-speech ---
with tab4:
    st.subheader("🗣️ Convert your Text to Speech")

    input_text_tospeak = st.text_area(
        "Input text to speak", value=st.session_state.summarized_text, height=300
    )

    if st.button("Text-to-speech"):
        with st.spinner("Speaking..."):
            response = requests.post(f"{API_BASE}/tts", json={"text": input_text_tospeak}, timeout=1200)
            if response.status_code == 200:
                audio_bytes = response.content
                st.audio(audio_bytes, format="audio/wav")
            else:
                st.error(f"Failed to generate speech. Status code: {response.status_code}")





