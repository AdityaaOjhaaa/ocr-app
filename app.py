import streamlit as st
from PIL import Image
import numpy as np
import easyocr
import torch

# Disable CUDA
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# Page config
st.set_page_config(page_title="OCR Scanner", layout="wide")

# Initialize OCR with caching
@st.cache_resource
def init_ocr():
    return easyocr.Reader(['en'], gpu=False, model_storage_directory='./models')

try:
    # Initialize reader
    reader = init_ocr()

    # Simple interface
    st.title("OCR Scanner")
    
    # File upload
    file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    
    if file:
        image = Image.open(file)
        st.image(image, width=400)
        
        if st.button("Extract Text"):
            with st.spinner("Processing..."):
                # Process image
                image_array = np.array(image)
                results = reader.readtext(image_array, detail=0)
                
                # Show results
                if results:
                    st.text_area("Extracted Text:", "\n".join(results), height=200)
                else:
                    st.warning("No text found in image")

except Exception as e:
    st.error("Setup error. Please check installation.")
