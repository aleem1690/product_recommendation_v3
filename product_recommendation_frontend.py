

import streamlit as st
from audio_recorder_streamlit import audio_recorder
import modal
import json
import os
import whisper



def main():
    # Enthusiastic welcome message
    st.title("Welcome to the Product Needs Portal!")
    st.write("Hello there! 🌟 We're excited to hear about your product needs. You can share your thoughts with us through text or voice!")

    # Radio button to select input type
    input_type = st.radio("Select input type:", ["Text", "Voice"])

    # Initialize variables
    product_needs_text = ""
    product_needs_audio = None

    #setting whisper model
    model = whisper.load_model("base")
    

    if input_type == "Text":
        # Text box for sharing product needs
        user_input_text = st.text_area("What do you want to buy today? (text):", "")
    else:
        # Voice recording option
        st.write("We would love to hear from you!")
        audio_bytes = audio_recorder()
        product_needs_voice = st.audio(audio_bytes, format="audio/wav")
        user_input_text = model.transcribe("audio.mp3")

    if st.button("Submit"):
        if input_type == "Text" and user_input_text.strip() != "":
          st.success("🚀 Thanks for sharing your thoughts through text!")
          user_input = user_input_text
        elif input_type == "Voice" and user_input_voice is not None:
          st.success("🎤 Thanks for sharing your thoughts through voice!")
          user_input = user_input_text
        else:
          st.warning("Oops! Please share your product needs, either through text or voice recording.")
        
        result = request_summary(user_input_text)
        st.write("Results")
        st.write(result['product_name'])
        st.write(result['requirement_list'])

        #if user_input:


def request_summary(user_input):
    f = modal.Function.lookup("corise-prod_recommendation-project", "summary_breakdown")
    output = f.call(search_request)
    return output

if __name__ == '__main__':
    main()
