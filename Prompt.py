import streamlit as st
import requests
from PIL import Image

# Hugging Face API setup
HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # you can swap with another text model

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.set_page_config(page_title="AI Photography Prompt Generator")
st.title("📸 AI Photography Prompt Generator")

# Upload reference image
ref_image = st.file_uploader("Upload Reference Image", type=["jpg", "jpeg", "png"])

subject = st.text_input("Subject", "tamarind tree in sunset")
lighting = st.selectbox("Lighting", ["Golden Hour", "Studio Light", "Neon Glow", "Natural Daylight"])
lens = st.selectbox("Lens", ["35mm Wide", "50mm Standard", "85mm Portrait", "Macro"])
composition = st.radio("Composition", ["Portrait", "Landscape", "Close-up", "Aerial"])
style = st.multiselect("Style Filters", ["Cinematic", "Vintage", "HDR", "Monochrome"])

if st.button("Generate AI Prompt"):
    user_input = f"Create a DSLR-style photography prompt. Subject: {subject}, Lighting: {lighting}, Lens: {lens}, Composition: {composition}, Style: {', '.join(style)}."
    
    output = query({"inputs": user_input})
    
    # Hugging Face returns text in 'generated_text'
    if isinstance(output, list) and "generated_text" in output[0]:
        ai_prompt = output[0]["generated_text"]
    else:
        ai_prompt = str(output)

    st.success("AI‑Generated Prompt:")
    st.code(ai_prompt)

    if ref_image:
        image = Image.open(ref_image)
        st.image(image, caption="Reference Image", use_column_width=True)
        st.info("This image can be used with the AI prompt in your generator.")
