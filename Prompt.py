import streamlit as st
from PIL import Image
from transformers import pipeline

# List of models to try locally
MODELS = [
    "google/flan-t5-small",
    "google/flan-t5-base",
    "google/flan-t5-large",
    "facebook/bart-large",
    "gpt2",
    "EleutherAI/gpt-neo-1.3B",
    "EleutherAI/gpt-neo-2.7B",
    "bigscience/bloomz-560m",
    "bigscience/bloomz-1b7",
    "tiiuae/falcon-7b-instruct"
]

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

    ai_prompt = None
    for model in MODELS:
        st.write(f"🔄 Trying model: {model}...")
        try:
            if "flan" in model or "bart" in model or "bloomz" in model or "falcon" in model:
                generator = pipeline("text2text-generation", model=model)
                result = generator(user_input, max_length=100)
                ai_prompt = result[0]["generated_text"]
            else:
                generator = pipeline("text-generation", model=model)
                result = generator(user_input, max_length=100)
                ai_prompt = result[0]["generated_text"]

            st.success(f"✅ Success with {model}")
            break
        except Exception as e:
            st.warning(f"⚠️ {model} failed: {e}")

    if ai_prompt:
        st.success("AI‑Generated Prompt:")
        st.code(ai_prompt)
    else:
        st.error("❌ All models failed locally. Please check your environment or install missing models.")

    if ref_image:
        image = Image.open(ref_image)
        st.image(image, caption="Reference Image", use_column_width=True)
        st.info("This image can be used with the AI prompt in your generator.")
