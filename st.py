from tempfile import NamedTemporaryFile

import requests
import streamlit as st

API_BASE = "http://localhost:8502"

st.set_page_config(page_title="AV Pipeline", layout="centered")

st.title("🎙️ Audio/Video → Text → Cleaned Audio")

# Session state to share transcript between tabs
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

tab1, tab2 = st.tabs(["🔊 Transcription", "🧹 Text Cleaner"])

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
                    r = requests.post(f"{API_BASE}/transcribe", files=files)

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
    input_text = st.text_area(
        "Input text to clean", value=st.session_state.transcribed_text, height=300
    )

    if st.button("Clean Text"):
        with st.spinner("Cleaning..."):
            response = requests.post(f"{API_BASE}/clean", json={"text": input_text})
            if response.status_code == 200:
                cleaned = response.json().get("cleaned_text", "")
                st.subheader("✅ Cleaned Output")
                st.text_area("Cleaned Text", value=cleaned, height=300)
            else:
                st.error("Cleaning failed.")
