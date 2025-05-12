from dotenv import load_dotenv
load_dotenv()

import json
import requests
import streamlit as st
import os
import re
import google.generativeai as genai
from PIL import Image
from streamlit_lottie import st_lottie

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

def get_gemini_response(input_text, image):
    if input_text:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content([image])
    return response.text

# Load Lottie animations safely with UTF-8 encoding
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning(f"Lottie file not found: {filepath}")
        return None
    except json.JSONDecodeError:
        st.error(f"Invalid JSON format in: {filepath}")
        return None
    except UnicodeDecodeError:
        st.error(f"Encoding error in: {filepath}. Make sure the file is UTF-8 encoded.")
        return None

# Page config
st.set_page_config(page_title="GEN Vision AI Assistant")

# Load animations
lottie_coding = load_lottiefile("coding.json")
lottie_spinner = load_lottiefile("spinner.json")
lottie_balloon = load_lottiefile("balloon.json")

# Title and animations
st.title("GEN Vision AI Assistant")
st.subheader("See the better future with GEN-Vision")

if lottie_coding:
    st_lottie(lottie_coding, speed=0.1, loop=True, height=100, width=100, key="coding_lottie")

# Styling
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        height: 60px;
        font-size: 18px;
        padding: 8px;
        border-radius: 8px;
    }
    div.stFileUploader > div {
        background-color: #3CE37C;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    div.stFileUploader > div:hover {
        background-color: #732d91;
    }
    div.stButton > button:first-child {
        background-color:#3CE37C;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #E501FF;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Input prompt and image
input_text = st.text_input("Input prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

# Submit logic
submit = st.button("Submit")

if submit:
    placeholder = st.empty()
    with placeholder.container():
        if lottie_spinner:
            st_lottie(lottie_spinner, speed=0.1, loop=True, height=100, width=100, key="loading_spinner")
            st.markdown("<h5 style='text-align: center;'>Ideas Catching Fire... 🔥</h5>", unsafe_allow_html=True)
        else:
            st.info("Generating response...")

    # Get Gemini response
    raw_response = get_gemini_response(input_text, image)
    cleaned_response = re.sub(r'</div>\s*$', '', raw_response.strip(), flags=re.IGNORECASE)

    # Remove loading placeholder
    placeholder.empty()

    # Show result
    st.header("The Response is:")
    st.markdown(
        f"""
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px; font-size: 16px;">
            {cleaned_response}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show balloon animation on success
    if lottie_balloon:
        st_lottie(lottie_balloon, speed=1, loop=False, height=200, width=200, key="balloon_animation_success")
