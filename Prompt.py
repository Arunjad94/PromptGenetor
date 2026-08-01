import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

st.set_page_config(page_title="Photography Prompt Generator")
st.title("📸 Photography Prompt Generator")

# Upload reference image
ref_image = st.file_uploader("Upload Reference Image", type=["jpg", "jpeg", "png"])

subject = st.text_input("Subject", "tamarind tree in sunset")
lighting = st.selectbox("Lighting", ["Golden Hour", "Studio Light", "Neon Glow", "Natural Daylight"])
lens = st.selectbox("Lens", ["35mm Wide", "50mm Standard", "85mm Portrait", "Macro"])
composition = st.radio("Composition", ["Portrait", "Landscape", "Close-up", "Aerial"])
style = st.multiselect("Style Filters", ["Cinematic", "Vintage", "HDR", "Monochrome"])

if st.button("Generate Prompt"):
    # Build prompt
    style_text = ", ".join(style) if style else "natural"
    prompt = f"A {composition.lower()} shot of {subject}, captured with {lens}, under {lighting}, styled as {style_text}."
    
    st.success("Generated Prompt:")
    st.code(prompt)

    # Show uploaded reference image
    if ref_image is not None:
        image = Image.open(ref_image)
        st.image(image, caption="Reference Image", use_column_width=True)
        st.info("Use this image + prompt in your AI generator.")

    # Inspiration previews
    html_code = """
    <div style="display:flex;gap:10px;overflow-x:auto;">
      <img src="https://source.unsplash.com/400x300/?cinematic,photography" width="200">
      <img src="https://source.unsplash.com/400x300/?vintage,photography" width="200">
      <img src="https://source.unsplash.com/400x300/?hdr,photography" width="200">
      <img src="https://source.unsplash.com/400x300/?monochrome,photography" width="200">
    </div>
    """
    components.html(html_code, height=320)
