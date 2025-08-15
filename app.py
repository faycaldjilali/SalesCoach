import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# ElevenLabs API endpoint
TTS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

st.set_page_config(page_title="AI Sales Coach Voice", page_icon="🎤")

st.title("🎤 AI Sales Coach - Voice Generator MVP")
st.write("Type your sales objection response and hear it in the founder's voice.")

# Text input
user_text = st.text_area("Enter text to convert to speech:", height=150)

if st.button("Generate Voice"):
    if not user_text.strip():
        st.warning("Please enter some text.")
    else:
        # Prepare API request
        headers = {
            "xi-api-key": ELEVEN_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": user_text,
            "voice_settings": {
                "stability": 0.7,
                "similarity_boost": 0.8
            }
        }

        # Call ElevenLabs API
        response = requests.post(TTS_URL, headers=headers, json=payload)

        if response.status_code == 200:
            # Save audio file
            audio_file = "output.mp3"
            with open(audio_file, "wb") as f:
                f.write(response.content)

            # Play audio in Streamlit
            st.audio(audio_file, format="audio/mp3")

            # Optional: Download link
            with open(audio_file, "rb") as f:
                st.download_button(
                    label="Download Audio",
                    data=f,
                    file_name="founder_voice.mp3",
                    mime="audio/mp3"
                )
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
