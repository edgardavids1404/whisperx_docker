import streamlit as st
import requests
from tempfile import NamedTemporaryFile

API_BASE = "http://localhost:8502"

st.set_page_config(page_title="AV Pipeline", layout="centered")

st.title("🎙️ Audio/Video → Text → Cleaned Audio")
uploaded_file = st.file_uploader("Upload audio/video file", type=["mp4", "mp3", "wav"])

if uploaded_file:
    st.audio(uploaded_file, format='audio/wav')

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
                        end_ts = f"{int(end // 60):02}:{int(end % 60):02}"

                        st.markdown(
                            f"**[{start_ts} - {end_ts}] {speaker}:** {text}"
                        )
                # st.text_area("📝 Cleaned Text", res["cleaned_text"], height=250)
                #
                # audio_url = f"{API_BASE}/media/{res['audio_path'].split('/')[-1]}"
                # audio_req = requests.get(audio_url)
                #
                # if audio_req.status_code == 200:
                #     st.audio(audio_req.content, format="audio/wav")
                # else:
                #     st.warning("Could not load generated audio.")
