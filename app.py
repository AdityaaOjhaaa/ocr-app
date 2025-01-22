import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import os
import torch

# Ensure CUDA is not required
os.environ['CUDA_VISIBLE_DEVICES'] = ''
torch.backends.cudnn.enabled = False

# Cache the EasyOCR reader initialization
@st.cache_resource(show_spinner=False)
def load_ocr():
    try:
        return easyocr.Reader(['en'], gpu=False)
    except Exception as e:
        st.error(f"Failed to initialize EasyOCR: {str(e)}")
        return None

# Basic page config
st.set_page_config(
    page_title="OCR Scanner",
    page_icon="📝",
    initial_sidebar_state="collapsed"
)

# Initialize the reader
reader = load_ocr()

if reader is None:
    st.error("Could not initialize the OCR system. Please try again later.")
    st.stop()

# Main app
st.title("📝 OCR Scanner")
st.write("Upload an image to extract text")

# File uploader
try:
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=400)
        
        # Extract text button
        if st.button("📋 Extract Text"):
            with st.spinner("Processing image... This might take a few moments."):
                try:
                    # Convert image to numpy array
                    image_array = np.array(image)
                    
                    # Perform OCR
                    results = reader.readtext(image_array, detail=0)
                    
                    # Display results
                    if results:
                        st.success("Text extracted successfully!")
                        st.text_area(
                            "Extracted Text:",
                            value="\n".join(results),
                            height=200
                        )
                    else:
                        st.warning("No text was detected in the image.")
                        
                except Exception as e:
                    st.error("Error processing image. Please try with a different image.")
                    st.info("Make sure the image contains clear, readable text.")

except Exception as e:
    st.error("An error occurred with the application. Please try refreshing the page.")
