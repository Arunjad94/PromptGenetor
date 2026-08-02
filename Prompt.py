import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch

st.set_page_config(page_title="AI Photography Prompt Generator")
st.title("📸 AI Photography Prompt Generator")

# Upload reference image
ref_image = st.file_uploader("Upload Reference Image", type=["jpg", "jpeg", "png"])

subject = st.text_input("Subject", "tamarind tree in sunset")
lighting = st.selectbox("Lighting", ["Golden Hour","Studio Light","Neon Glow","Natural Daylight"])
lens = st.selectbox("Lens", ["35mm Wide","50mm Standard","85mm Portrait","Macro"])
composition = st.radio("Composition", ["Portrait","Landscape","Close-up","Aerial"])
style = st.multiselect("Style Filters", ["Cinematic","Vintage","HDR","Monochrome"])

if st.button("Generate AI Prompt") and ref_image:
    image = Image.open(ref_image).convert("RGB")

    ai_prompt = None
    model_used = None

    # Try BLIP
    try:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)
        ai_prompt = f"{description}. DSLR-style {composition.lower()} shot of {subject}, with {lens}, under {lighting}, styled as {', '.join(style)}."
        model_used = "BLIP-base"
    except Exception:
        pass

    # Fallback: ViT-GPT2
    if ai_prompt is None:
        try:
            model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
            output_ids = model.generate(pixel_values, max_length=50)
            description = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            ai_prompt = f"{description}. DSLR-style {composition.lower()} shot of {subject}, with {lens}, under {lighting}, styled as {', '.join(style)}."
            model_used = "ViT-GPT2"
        except Exception:
            pass

    # Final consolidated output
    if ai_prompt:
        st.success(f"AI‑Generated Prompt (via {model_used}):")
        st.code(ai_prompt)
        st.image(image, caption="Reference Image", use_column_width=True)
    else:
        st.error("❌ All captioning models failed. Please try again locally with GPU support or check dependencies.")
