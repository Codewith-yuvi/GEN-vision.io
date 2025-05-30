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

# Load Lottie animations
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Error loading Lottie URL: {e}")
        return None

# Page config
st.set_page_config(page_title="GEN Vision AI Assistant")

# ✅ Clean White Background & Styling
st.markdown("""
    <style>
    [data-testid="stApp"] {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
    }

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

    /* Centering and ensuring the balloon animation appears below */
    .balloon-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 30px; /* Add some space from the content */
    }
    </style>
""", unsafe_allow_html=True)

# Load animations
lottie_coding = load_lottiefile("coding.json")
lottie_spinner = load_lottiefile("spinner.json")
lottie_balloon = load_lottiefile("balloon.json")

# App title and subtitle
st.title("GEN Vision AI Assistant")
st.subheader("See the better future with GEN-Vision")

# Show animation (kept)
if lottie_coding:
    st_lottie(lottie_coding, speed=0.5, loop=True, height=250, key="coding_lottie")

# Input fields
input_text = st.text_input("Input prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

# Submit button
submit = st.button("Submit")

if submit:
    placeholder = st.empty()
    with placeholder.container():
        if lottie_spinner:
            st_lottie(lottie_spinner, speed=0.5, loop=True, height=200, key="loading_spinner")
            st.markdown("<h5 style='text-align: center;'>Ideas Catching Fire... 🔥</h5>", unsafe_allow_html=True)
        else:
            st.info("Generating response...")

    # Get Gemini response
    raw_response = get_gemini_response(input_text, image)
    cleaned_response = re.sub(r'</div>\s*$', '', raw_response.strip(), flags=re.IGNORECASE)

    placeholder.empty()

    # Display response
    if lottie_balloon:
        st.markdown('<div class="balloon-container">', unsafe_allow_html=True)  # Open the container div
        st_lottie(lottie_balloon, speed=1, loop=False, height=100, width=100, key="balloon_animation_success")
        st.markdown('</div>', unsafe_allow_html=True)  # Close the container div
    st.markdown("### The Response is:")
    st.markdown(
        f"""
        <div style="background-color: #6EF5FC; padding: 15px; border-radius: 10px; font-size: 16px;">
            {cleaned_response}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show balloon animation on success (now positioned below the response)
    # if lottie_balloon:
    #     st.markdown('<div class="balloon-container">', unsafe_allow_html=True)  # Open the container div
    #     st_lottie(lottie_balloon, speed=1, loop=False, height=200, width=200, key="balloon_animation_success")
    #     st.markdown('</div>', unsafe_allow_html=True)  # Close the container div
