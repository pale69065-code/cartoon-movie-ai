
import os
import streamlit as st
from gtts import gTTS
import replicate

# Streamlit Page Config
st.set_page_config(page_title="AI Cartoon Studio", layout="wide")
st.title("🎬 AI Cartoon Video Studio")

st.sidebar.header("Settings")

# १. पहिले Render को Environment Variable बाट टोकन लिने
replicate_api = os.getenv("REPLICATE_API_TOKEN")

# २. यदि Render मा भेटिएन भने मात्र Sidebar को Input Box देखाउने
if not replicate_api:
    replicate_api = st.sidebar.text_input("Replicate API Token", type="password")

script = st.text_area(
    "Enter Animation Script:",
    "Hello! Welcome to AI Cartoon Studio."
)

if st.button("Generate Animation"):
    if not replicate_api:
        st.error("Please enter your Replicate API Token in the sidebar or set it in Render environment.")
    else:
        try:
            os.environ["REPLICATE_API_TOKEN"] = replicate_api
            
            # Audio Generation
            st.info("Generating Audio...")
            tts = gTTS(text=script, lang='en')
            audio_path = "generated_audio.mp3"
            tts.save(audio_path)
            st.audio(audio_path)

            # Animation Generation with Replicate
            st.info("Generating Animation with Replicate...")
            output = replicate.run(
                "lucataco/sadtalker:3aa3dac9353e1d611b763d421273934383416e0339906d2d488581e289f8164f",
                input={
                    "driven_audio": open(audio_path, "rb"),
                    "source_image": "https://replicate.delivery/pbxt/IJ3D8XqJ2zQ461P6yVjOQ11uO8u6R1S2v3p4m5n6/avatar.png",
                    "still": True,
                    "use_enhancer": True
                }
            )
            
            st.success("Animation Generated Successfully!")
            st.video(output)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
