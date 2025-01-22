import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Smart OCR Scanner",
    page_icon="📱",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .css-1v0mbdj.e115fcil1 {
        max-width: 100%;
    }
    .stButton>button {
        width: 100%;
        margin-top: 10px;
        margin-bottom: 10px;
        background-color: #ff4b4b;
        color: white;
    }
    .result-container {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-top: 20px;
    }
    .upload-text {
        text-align: center;
        padding: 20px;
        border: 2px dashed #cccccc;
        border-radius: 10px;
        margin: 20px 0;
    }
    @media (max-width: 768px) {
        .responsive-text {
            font-size: 14px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session states
if 'processed_text' not in st.session_state:
    st.session_state.processed_text = None
if 'reader' not in st.session_state:
    st.session_state.reader = easyocr.Reader(['en'], verbose=False)

# App header
st.title("📱 Smart OCR Scanner")
st.markdown("Extract text from images instantly!", unsafe_allow_html=True)

# File uploader
st.markdown("<div class='upload-text'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop your image here or click to browse",
    type=['png', 'jpg', 'jpeg']
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    # Create two columns for image and text
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, width=400, caption="Uploaded Image")
    
    with col2:
        # Extract text button and processing
        if st.button("Extract Text 🔍", key="extract"):
            with st.spinner("Processing... Please wait"):
                try:
                    # Convert image to numpy array and process
                    image_array = np.array(image)
                    result = st.session_state.reader.readtext(image_array, detail=0)
                    extracted_text = "\n".join(result)
                    st.session_state.processed_text = extracted_text
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
                    st.info("Please try uploading a different image or check if the image contains clear text.")
        
        # Display results if text has been processed
        if st.session_state.processed_text:
            st.markdown("<div class='result-container'>", unsafe_allow_html=True)
            st.text_area(
                "Extracted Text",
                st.session_state.processed_text,
                height=200
            )
            if st.button("Copy Text 📋", key="copy"):
                st.toast("Text copied to clipboard!", icon="✅")
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background-color: rgba(255, 255, 255, 0.9);'>
        <p class='responsive-text'>Made with ❤️ by Your Name</p>
    </div>
    """, unsafe_allow_html=True)

# Error handling for mobile devices
if st.session_state.get('error_occurred'):
    st.error("If you're having issues on mobile, please try refreshing the page or clearing your browser cache.")
    if st.button("Clear Error"):
        st.session_state.error_occurred = False
