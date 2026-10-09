
import streamlit as st
from gtts import gTTS
import os
import replicate

st.set_page_config(page_title="AI Cartoon Studio", layout="wide")

st.title("🎬 AI Cartoon Video Studio")

st.sidebar.header("Settings")
replicate_api = st.sidebar.text_input("Replicate API Token", type="password")

script = st.text_area("Enter Animation Script:", "Hello! Welcome to AI Cartoon Studio.")

if st.button("Generate Animation"):
    if not replicate_api:
        st.error("Please enter your Replicate API Token in the sidebar.")
    else:
        try:
            os.environ["REPLICATE_API_TOKEN"] = replicate_api
            
            st.info("Generating Audio...")
            tts = gTTS(text=script, lang='en')
            audio_path = "voice.mp3"
            tts.save(audio_path)
            st.audio(audio_path)

            st.info("Generating Animation with Replicate...")
            with open(audio_path, "rb") as audio_file:
                output = replicate.run(
                    "cjwbw/sadtalker:3aa35132c1012399081216968032501062b0c2514123b03698642a8b94f92329",
                    input={
                        "driven_audio": audio_file,
                        "source_image": "https://raw.githubusercontent.com/pale69065-code/cartoon-movie-ai/main/character.jpg"
                    }
                )
            
            if output:
                st.success("Animation Generated Successfully!")
                st.video(output)
            else:
                st.error("Failed to generate video.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
