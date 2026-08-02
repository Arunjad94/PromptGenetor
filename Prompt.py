import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from transformers import CLIPProcessor, CLIPModel

st.set_page_config(page_title="AI Photography Prompt Generator")
st.title("📸 AI Photography Prompt Generator")

# Upload reference image
ref_image = st.file_uploader("Upload Reference Image", type=["jpg", "jpeg", "png"])

subject = st.text_input("Subject", "tamarind tree in sunset")
lighting = st.selectbox("Lighting", ["Golden Hour","Studio Light","Neon Glow","Natural Daylight"])
lens = st.selectbox("Lens", ["35mm Wide","50mm Standard","85mm Portrait","Macro"])
composition = st.radio("Composition", ["Portrait","Landscape","Close-up","Aerial"])
style = st.multiselect("Style Filters", ["Cinematic","Vintage","HDR","Monochrome"])

def generate_prompt(image, user_text):
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
        model_used = "BLIP"
        return ai_prompt, model_used
    except Exception:
        pass

    # Try BLIP-2
    try:
        processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
        inputs = processor(images=image, text="Describe this photo", return_tensors="pt")
        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)
        ai_prompt = f"{description}. DSLR-style {composition.lower()} shot of {subject}, with {lens}, under {lighting}, styled as {', '.join(style)}."
        model_used = "BLIP-2"
        return ai_prompt, model_used
    except Exception:
        pass

    # Try CLIP (image-text similarity, fallback)
    try:
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        inputs = processor(text=[user_text], images=image, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        description = f"Prompt aligned with image and text: {user_text}"
        ai_prompt = f"{description}. DSLR-style {composition.lower()} shot of {subject}, with {lens}, under {lighting}, styled as {', '.join(style)}."
        model_used = "CLIP"
        return ai_prompt, model_used
    except Exception:
        pass

    return None, None

if st.button("Generate AI Prompt") and ref_image:
    image = Image.open(ref_image).convert("RGB")
    user_text = f"Subject: {subject}, Lighting: {lighting}, Lens: {lens}, Composition: {composition}, Style: {', '.join(style)}"

    ai_prompt, model_used = generate_prompt(image, user_text)

    if ai_prompt:
        st.success(f"AI‑Generated Prompt (via {model_used}):")
        st.code(ai_prompt)
        st.image(image, caption="Reference Image", use_column_width=True)
    else:
        st.error("❌ All models failed. Please check environment or install missing models.")
