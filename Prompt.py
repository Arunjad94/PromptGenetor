import streamlit as st
from transformers import pipeline
from PIL import Image

# Keep a short list of lightweight models
MODELS = [
    "google/flan-t5-small",
    "facebook/bart-large",
    "gpt2"
]

st.set_page_config(page_title="AI Photography Prompt Generator")
st.title("📸 AI Photography Prompt Generator")

# Upload reference image
ref_image = st.file_uploader("Upload Reference Image", type=["jpg", "jpeg", "png"])

subject = st.text_input("Subject", "tamarind tree in sunset")
lighting = st.selectbox("Lighting", ["Golden Hour","Studio Light","Neon Glow","Natural Daylight"])
lens = st.selectbox("Lens", ["35mm Wide","50mm Standard","85mm Portrait","Macro"])
composition = st.radio("Composition", ["Portrait","Landscape","Close-up","Aerial"])
style = st.multiselect("Style Filters", ["Cinematic","Vintage","HDR","Monochrome"])

if st.button("Generate AI Prompt"):
    user_input = f"Create a DSLR-style photography prompt. Subject: {subject}, Lighting: {lighting}, Lens: {lens}, Composition: {composition}, Style: {', '.join(style)}."

    ai_prompt = None
    for model in MODELS:
        try:
            if "flan" in model or "bart" in model:
                generator = pipeline("text2text-generation", model=model)
                result = generator(user_input, max_length=80)
                ai_prompt = result[0]["generated_text"]
            else:
                generator = pipeline("text-generation", model=model)
                result = generator(user_input, max_length=80)
                ai_prompt = result[0]["generated_text"]
            break  # stop after first success
        except Exception:
            continue  # silently skip failures

    if ai_prompt:
        st.success("AI‑Generated Prompt:")
        st.code(ai_prompt)
    else:
        st.error("❌ No model succeeded. Please check your environment.")

    if ref_image:
        image = Image.open(ref_image)
        st.image(image, caption="Reference Image", use_column_width=True)
        st.info("This image can be used with the AI prompt in your generator.")
