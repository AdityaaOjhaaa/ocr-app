import streamlit as st
from PIL import Image
import numpy as np
import easyocr
import torch

# Force CPU mode
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
torch.backends.cudnn.enabled = False

# Initialize session state
if 'ocr_ready' not in st.session_state:
    st.session_state.ocr_ready = False

# Page config - Keep it simple
st.set_page_config(
    page_title="OCR Scanner",
    layout="centered",  # Changed to centered for better compatibility
    initial_sidebar_state="collapsed"
)

# Initialize OCR
@st.cache_resource(show_spinner=True)
def load_ocr():
    try:
        return easyocr.Reader(['en'], gpu=False, download_enabled=True)
    except Exception as e:
        st.error(f"OCR initialization error: {str(e)}")
        return None

# Main app
def main():
    st.title("OCR Scanner")
    
    # Initialize OCR
    if not st.session_state.ocr_ready:
        with st.spinner("Loading OCR system..."):
            reader = load_ocr()
            if reader is not None:
                st.session_state.ocr_ready = True
            else:
                st.error("Failed to initialize OCR. Please refresh the page.")
                return

    # File upload
    uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Show image
        col1, col2 = st.columns(2)
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Process image
        with col2:
            if st.button("Extract Text"):
                try:
                    with st.spinner("Processing image..."):
                        # Convert to numpy array
                        image_array = np.array(image)
                        
                        # Get OCR results
                        reader = load_ocr()
                        results = reader.readtext(image_array, detail=0)
                        
                        if results:
                            st.success("Text extracted successfully!")
                            st.text_area(
                                "Extracted Text:",
                                value="\n".join(results),
                                height=200
                            )
                        else:
                            st.warning("No text detected in the image.")
                except Exception as e:
                    st.error("Error processing image. Please try another image.")
                    st.exception(e)

if __name__ == "__main__":
    main()
