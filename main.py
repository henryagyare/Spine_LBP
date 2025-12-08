import streamlit as st
from keras.models import load_model
from PIL import Image
from utils import classify
from ai_analysis import get_ai_analysis, is_api_configured, get_api_setup_instructions
import os

import tensorflow as tf
import keras
print("TF version:", tf.__version__)
print("Keras version:", keras.__version__)


# Set page config
st.set_page_config(
    page_title="Discrete Structures Final Project",
    page_icon="🏥",
    layout="wide"
)

# Set title
st.title('🏥 Spinal Disease Classifier')
st.subheader('📚 Discrete Structures Final Project')

# Add description/context
st.markdown("""
### About This Project
This deep learning application helps detect abnormalities in lumbar spine MRI scans using computer vision. 
The model was trained using MobileNet-V2 architecture on MRI images to provide instant diagnostic support.

**How it works:**
1. Upload an MRI scan of a lumbar spine
2. The AI model analyzes the image
3. Get instant classification results with confidence scores

⚠️ **Disclaimer:** This tool is for educational and research purposes only. It should not be used as a substitute 
for professional medical diagnosis. Always consult with qualified healthcare professionals.
""")

# Set header
st.header('Upload a Lumbar Spine MRI Scan')

# Check if model exists
MODEL_PATH = 'model/spinal_classifier.keras'
LABELS_PATH = 'model/labels.txt'

if not os.path.exists(MODEL_PATH):
    st.error("❌ Model not found! Please train the model first by running: `python train_model.py`")
    st.info("""
    **Setup Instructions:**
    1. Organize your dataset in the `data/` directory
    2. Run `python train_model.py` to train the model
    3. Come back here and refresh the page
    """)
    st.stop()

# Upload file
file = st.file_uploader('Upload MRI scan (JPEG, JPG, or PNG)', type=['jpeg', 'jpg', 'png'])

# Load classifier
try:
    model = load_model(MODEL_PATH)
    
    # Load class names
    with open(LABELS_PATH, 'r') as f:
        class_names = [line.strip().split(' ')[1] for line in f.readlines()]
except Exception as e:
    st.error(f"❌ Error loading model: {str(e)}")
    st.stop()

# Display image and make prediction
if file is not None:
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Display the uploaded image
        image = Image.open(file).convert('RGB')
        st.image(image, caption='Uploaded MRI Scan', use_column_width=True)
    
    with col2:
        # Add a spinner while processing
        with st.spinner('🔍 Analyzing MRI scan...'):
            # Classify image
            class_name, conf_score = classify(image, model, class_names)
        
        # Display results
        st.markdown("### 🎯 Classification Result")
        
        # Display prediction with colored background
        if class_name.lower() == 'normal':
            st.success(f"**Diagnosis:** {class_name.upper()}")
        else:
            st.warning(f"**Diagnosis:** {class_name.upper()}")
        
        # Display confidence score with progress bar
        st.markdown(f"**Confidence Score:** {conf_score:.2%}")
        st.progress(float(conf_score))
        
        # AI-Powered Analysis Section
        st.markdown("---")
        st.markdown("### 🤖 AI-Powered Analysis")
        
        if is_api_configured():
            with st.spinner('🔍 Generating AI analysis...'):
                ai_analysis = get_ai_analysis(class_name, conf_score)
                if ai_analysis:
                    st.info(ai_analysis)
                else:
                    st.warning("Unable to generate AI analysis at this time.")
        else:
            with st.expander("ℹ️ Enable AI Analysis (Optional)"):
                st.markdown(get_api_setup_instructions())
        
        # Add interpretation
        st.markdown("---")
        st.markdown("### 📊 Interpretation")
        
        if conf_score > 0.90:
            st.success("✅ **High Confidence** - The model is very certain about this classification.")
        elif conf_score > 0.70:
            st.warning("⚠️ **Moderate Confidence** - Consider consulting a medical professional for confirmation.")
        else:
            st.error("❌ **Low Confidence** - Please upload a clearer image or consult a medical expert.")
        
        # Additional information
        st.markdown("---")
        st.markdown("### 💡 Recommendations")
        
        if class_name.lower() == 'abnormal':
            st.markdown("""
            - Consult with a radiologist or spine specialist
            - Consider additional imaging if recommended
            - Discuss treatment options with your healthcare provider
            - Keep track of symptoms and their progression
            """)
        else:
            st.markdown("""
            - Results suggest normal findings
            - Maintain good spinal health through proper posture
            - Regular exercise and core strengthening recommended
            - Consult a doctor if you experience persistent symptoms
            """)

# Sidebar with additional information
with st.sidebar:
    st.markdown("### 👥 Project Team")
    st.markdown("""
    **Mohammed Abdulai**  
    *UI/UX Design & Application Development*
    
    **Henry Asante**  
    *Model Training & Optimization*
    
    **Chris Gadze**  
    *Dataset Acquisition & Preparation*
    """)
    
    st.markdown("---")
    
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
    - **Streamlit** - Web Framework
    - **Python** - Programming Language
    - **MobileNet-V2** - Model Architecture
    - **TensorFlow/Keras** - Deep Learning Framework
    - **PyDICOM** - Medical Image Processing
    """)
    
    st.markdown("---")
    
    st.markdown("### 📖 Model Details")
    st.markdown("""
    **Architecture:** MobileNet-V2  
    **Input Size:** 224x224 pixels  
    **Classes:** With Pain, Without Pain  
    **Training Images:** 140  
    **Validation Accuracy:** 51.67%
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Best Practices")
    st.markdown("""
    - Use clear, high-quality MRI scans
    - Ensure proper image orientation
    - Sagittal or axial views work best
    - DICOM images should be converted to JPEG/PNG
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Settings")
    if st.button("🔄 Clear Cache"):
        st.cache_data.clear()
        st.success("Cache cleared!")

