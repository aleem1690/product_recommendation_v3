

import streamlit as st
from audio_recorder_streamlit import audio_recorder
import modal
import json
import os
import whisper
import pandas as pd
# from st_draggable_list import DraggableList
import speech_recognition as sr
from audiorecorder import audiorecorder
import tempfile

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
    r = sr.Recognizer()

    
    if input_type == "Text":
        # Text box for sharing product needs
        user_input_text = st.text_area("What do you want to buy today?:", "")
    else:
        # Voice recording option
        st.write("We would love to hear from you!")
        # audio_bytes = audio_recorder()
        audio_bytes = audiorecorder("Click to record")
        if len(audio_bytes) > 0:
            # To play audio in frontend:
            st.audio(audio_bytes.tobytes())
            
            # To save audio to a file:
            # wav_file = tempfile.TemporaryFile()
            wav_file = open("audio_bytes.wav", "wb")
            wav_file.write(audio_bytes.tobytes())

            st.write(wav_file.name)

            audio_tbt = whisper.load_audio("35be1da269ee870eb1c2a9a759869f5155b3b63efa134bbb4e02c095.wav")
        
        # typ = type(audio_bytes)
        # st.write(typ)
        # product_needs_voice = st.audio(audio_bytes, format="audio/wav"

    if st.button("Submit"):
        if input_type == "Text" and user_input_text.strip() != "":
          st.success("🚀 Thanks for sharing your thoughts through text!")
          user_input = user_input_text
        elif input_type == "Voice" and user_input_voice is not None:
          csuccess("🎤 Thanks for sharing your thoughts through voice!")
          user_input = user_input_voice
        else:
          st.warning("Oops! Please share your product needs, either through text or voice recording.")
        
        
        result = request_summary(user_input)
        
        
        try:
            # check if the key exists in session state
            _ = st.session_state.result
        except AttributeError:
            # otherwise set it to false
            st.session_state.result = False

        # Display the product name and requirements from ML model
        st.success("Product Information from ML Model:")
        
        # Extract product name and requirements
        
        #result_df = pd.DataFrame(result)
        result_df = pd.DataFrame()

        for keys,values in result.items():
          s1 = pd.DataFrame(values)
          result_df = pd.concat([result_df,s1],axis=1)
        result_df.columns = result.keys()
        result_df.fillna('',inplace=True)

        st.write("Confirm if the details are correct")
        st.write("You are looking to buy: ",result_df["product_name"][0])
        

        st.write("Price Range: ",result_df["product_price"][0])

        st.write("These are your pririoties")
        st.write(result_df["product_needs"])
        st.write("If the details are correct, please click proceed")
        if 'product_name' not in st.session_state:
            st.session_state['product_name'] = result_df["product_name"][0]
        if 'product_needs' not in st.session_state:
            st.session_state['product_needs'] = result_df["product_needs"]
        if 'product_price' not in st.session_state and len(result_df["product_price"].unique())>0:
            st.session_state['product_price'] = result_df["product_price"][0]
    no_of_link = 2
    st.write(st.session_state['product_name'])
    st.write(st.session_state['product_price'])
    st.write(result_df['product_needs'])


    
    if st.button("Proceed"):
        final_product = final_recommendation(result_df,no_of_link)
        st.write(final_product)
        
        # data_prod_name = result_df["product_name"].drop_duplicates()
        # name_df = st.experimental_data_editor(data_prod_name, num_rows="dynamic")

        # st.write("Product Requirements:")
        # data_req_name = result_df["product_needs"]
        # data_req_name["Rank"] = ""
        # req_df = st.experimental_data_editor(data_req_name,num_rows="dynamic")
        # if st.button("Save Changes"):
        #     st.session_state.result["product_name"] = name_df
        #     st.session_state.result["requirements_list"] = req_df
        #     st.session_state.result = True
        #     st.success("Changes saved!")
            
        #     st.table(name_df,req_df)
            

def request_summary(user_input):
    f = modal.Function.lookup("corise-request_summary", "result_formatting")
    output = f.call(user_input)
    return output

def final_recommendation(summary_dict,no_of_link):
    g = modal.Function.lookup("corise-final_recommendation-project","final_product")
    output = g.call(summary_dict,no_of_link)
    return output

if __name__ == '__main__':
    main()
