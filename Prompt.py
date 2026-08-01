import streamlit as st
import requests
from PIL import Image

HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

st.title("📸 AI Photography Prompt Generator")

ref_image = st.file_uploader("Upload Reference Image", type=["jpg","jpeg","png"])
subject = st.text_input("Subject", "tamarind tree in sunset")
lighting = st.selectbox("Lighting", ["Golden Hour","Studio Light","Neon Glow","Natural Daylight"])
lens = st.selectbox("Lens", ["35mm Wide","50mm Standard","85mm Portrait","Macro"])
composition = st.radio("Composition", ["Portrait","Landscape","Close-up","Aerial"])
style = st.multiselect("Style Filters", ["Cinematic","Vintage","HDR","Monochrome"])

if st.button("Generate AI Prompt"):
    user_input = f"Create a DSLR-style photography prompt. Subject: {subject}, Lighting: {lighting}, Lens: {lens}, Composition: {composition}, Style: {', '.join(style)}."
    output = query({"inputs": user_input})

    if isinstance(output, list) and "generated_text" in output[0]:
        ai_prompt = output[0]["generated_text"]
    elif "error" in output:
        ai_prompt = f"⚠️ API Error: {output['error']}"
    else:
        ai_prompt = str(output)

    st.success("AI‑Generated Prompt:")
    st.code(ai_prompt)

    if ref_image:
        image = Image.open(ref_image)
        st.image(image, caption="Reference Image", use_column_width=True)
