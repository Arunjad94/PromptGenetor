import streamlit as st
import requests
from PIL import Image

# Hugging Face token (store safely in .streamlit/secrets.toml for deployment)
HF_TOKEN = "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"

# List of models to try in order
MODELS = [
    "google/flan-t5-small",
    "google/flan-t5-base",
    "google/flan-t5-large",
    "tiiuae/falcon-7b-instruct",
    "facebook/bart-large",
    "gpt2",
    "EleutherAI/gpt-neo-1.3B",
    "EleutherAI/gpt-neo-2.7B",
    "bigscience/bloomz-560m",
    "bigscience/bloomz-1b7"
]

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_model(model, payload):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

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
        output = query_model(model, {"inputs": user_input})

        # Hugging Face returns list with 'generated_text' or dict with 'error'
        if isinstance(output, list) and "generated_text" in output[0]:
            ai_prompt = output[0]["generated_text"]
            st.success(f"✅ Success with {model}")
            break
        elif "error" in output:
            st.warning(f"⚠️ {model} failed: {output['error']}")
        else:
            st.warning(f"⚠️ {model} returned unexpected output: {output}")

    if ai_prompt:
        st.success("AI‑Generated Prompt:")
        st.code(ai_prompt)
    else:
        st.error("❌ All models failed. Please try again later.")

    if ref_image:
        image = Image.open(ref_image)
        st.image(image, caption="Reference Image", use_column_width=True)
        st.info("This image can be used with the AI prompt in your generator.")
