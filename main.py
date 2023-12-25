from dotenv import load_dotenv, find_dotenv
import requests
import os
import io
import streamlit as st
from PIL import Image
from datetime import datetime

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def text2image(prompt: str):

    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    image_bytes = query({
        "inputs": prompt,
    })

    # You can access the image with PIL.Image for example
    image = Image.open(io.BytesIO(image_bytes))

    filename = f"img.jpg"

    image.save(filename)
    return filename

def main():
    st.set_page_config(page_title="Text2Image GenAI", page_icon="♦",layout="wide")
    st.title("Text To Image Generator")

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
    st.markdown(hide_stremlit_styles,unsafe_allow_html=True)

    st.markdown('<hr><center><a href="https://www.instagram.com/suraj_nate/" target="_blank" style="color:white;text-decoration:none">@suraj_nate</a></center>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
