from dotenv import load_dotenv

load_dotenv() ##load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Pro Vision
model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##Initialize our streamlit app

st.set_page_config(page_title="Caption Generator")
st.header("Caption Generator")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image or pdf....",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded image", use_column_width=True)

submit1=st.button("Provide me caption for Linkedin post")

submit2=st.button("Provide me caption for Instagram post")

input_prompt1="""
You are an expert in generating professional captions for any achievement to share on Linkedin. We will upload a image that could be either certificates, or anything else. You have to read text from that image and then generate the proper postable captions to post on Linkiedin.
Starting should be like this

Hello #connections

and then content for the post

and at the end of content give minimum 5 and maximum 15 hashtags related to content
"""

input_prompt2="""
Generate a captivating Instagram caption for the uploaded image. Whether it's a moment of joy, an achievement, a beautiful scenery, or anything else, create a versatile caption that suits various types of photos. Make it engaging, authentic, and suitable for sharing with your Instagram followers.Moreove take it from input that whether user wants short or long captions
"""
#if submit button is clicked
if submit1:
    if uploaded_file is not None:
        image_data=input_image_details(uploaded_file)
        response=get_gemini_response(input_prompt1,image_data,input)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the image")

elif submit2:
    if uploaded_file is not None:
        image_data=input_image_details(uploaded_file)
        response=get_gemini_response(input_prompt2,image_data,input)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the image")

