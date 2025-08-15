import streamlit as st
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load keys
load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# ElevenLabs TTS URL
TTS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

st.set_page_config(page_title="AI Sales Coach Voice", page_icon="🎤")
st.title("🎤 AI Sales Coach - Objection Handler")

# Objection input
objection = st.text_input("Enter a sales objection:", placeholder="It's too expensive.")

if st.button("Generate AI Response & Voice"):
    if not objection.strip():
        st.warning("Please enter an objection.")
    else:
        with st.spinner("Generating AI sales response..."):
            # Step 1: Generate founder-style response with OpenAI
            prompt = f"""
            You are the founder of a fast-growing home services company.
            Respond to this objection in a confident, persuasive, and friendly tone,
            following the company's sales playbook. Use short, clear sentences.
            Objection: {objection}
            """
            ai_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            ).choices[0].message.content

        st.subheader("📝 AI Generated Response")
        st.write(ai_response)

        with st.spinner("Converting to voice..."):
            # Step 2: Convert AI text to speech via ElevenLabs
            headers = {
                "xi-api-key": ELEVEN_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {
                "text": ai_response,
                "voice_settings": {
                    "stability": 0.7,
                    "similarity_boost": 0.8
                }
            }
            response = requests.post(TTS_URL, headers=headers, json=payload)

            if response.status_code == 200:
                audio_file = "output.mp3"
                with open(audio_file, "wb") as f:
                    f.write(response.content)

                st.audio(audio_file, format="audio/mp3")

                with open(audio_file, "rb") as f:
                    st.download_button(
                        label="Download Voice",
                        data=f,
                        file_name="ai_sales_response.mp3",
                        mime="audio/mp3"
                    )
            else:
                st.error(f"Voice generation failed: {response.status_code} - {response.text}")
