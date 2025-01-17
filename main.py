from dotenv import load_dotenv, find_dotenv
import requests
import os
import io
import streamlit as st
from PIL import Image
from datetime import datetime

# Load environment variables
load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def text2image(prompt: str):
    # API URL and headers
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer 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"}

    # Function to query the Hugging Face API
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None

    # Request the image
    image_bytes = query({"inputs": prompt})
    if image_bytes:
        try:
            # Open and save the image if the response is valid
            image = Image.open(io.BytesIO(image_bytes))
            filename = f"img.jpg"
            image.save(filename)
            return filename
        except Exception as e:
            st.error(f"Error opening image: {e}")
            return None
    else:
        return None

def main():
    st.set_page_config(page_title="Text2Image GenAI", page_icon="♦", layout="wide")
    st.title("Text To Image Generator")

    # Display a note for users about potential issues with model refresh
    st.info("Note: If the image generation doesn't work immediately, please try again after some time. The model may be refreshing or reloading.")

    with st.form(key="my-forms"):
        query = st.text_area(
            label="Enter Prompt for the Image...",
            help="Enter the prompt for the Image here....",
            key="query",
            max_chars=500)
        submit_button = st.form_submit_button(label="Generate")

    if query and submit_button:
        with st.spinner(text="Generating image in Progress..."):
            img_file = text2image(prompt=query)

        if img_file:
            st.subheader("Your Image")
            st.image(f"./{img_file}", caption=query)

    if os.path.exists("img.jpg"):
        os.remove("img.jpg")

    hide_stremlit_styles = """
        <style>
        #MainMenu{visibility:hidden;}
        header{visibility:hidden;}
        footer{visibility:hidden;}
        </style>
    """
    st.markdown(hide_stremlit_styles, unsafe_allow_html=True)

    st.write('<hr><center>Let Me Know if you liked it - hit the Name mention below </center>', unsafe_allow_html=True)
    st.markdown('<center><a href="https://www.instagram.com/suraj_nate/" target="_blank" style="color:white;text-decoration:none">@suraj_nate</a></center>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
