# ==================================================
# Spinal Disease Classifier — Portfolio UI (Streamlit-safe)
# ==================================================
import os
import base64
import streamlit as st
from PIL import Image
from keras.models import load_model

from utils import classify
from ai_analysis import get_ai_analysis, is_api_configured, get_api_setup_instructions

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="Spinal Disease Classifier", page_icon="🧠", layout="wide"
)

# ---------------------------
# Paths
# ---------------------------
MODEL_PATH = "model/spinal_classifier.keras"
LABELS_PATH = "model/labels.txt"
HERO_IMAGE = "assets/hero_bg.png"


# ==================================================
# Helpers
# ==================================================
def load_image_base64(path: str) -> str:
    """Load an image file and return base64 string. Returns '' if missing."""
    if not path or not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


@st.cache_resource
def load_classifier(model_path: str, labels_path: str):
    """Load model + labels once per session."""
    if not os.path.exists(model_path):
        return None, None

    model = load_model(model_path)

    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"Labels file not found at: {labels_path}")

    with open(labels_path, "r") as f:
        # expects lines like: "0 Normal" or "1 Abnormal"
        labels = [line.strip().split(" ", 1)[1] for line in f if line.strip()]

    return model, labels


def inject_global_css():
    """Global styling that plays nicely with Streamlit."""
    st.markdown(
        """
        <style>
        /* give page a darker feel */
        .stApp {
            background: radial-gradient(circle at top left, #0b1220 0%, #050a14 60%, #020617 100%);
        }

        /* tighten main container width a bit */
        section.main > div { 
            padding-top: 1.5rem;
        }

        /* nicer headings */
        h1, h2, h3 {
            letter-spacing: 0.2px;
        }

        /* smaller label spacing */
        .stFileUploader label {
            font-weight: 600;
        }

        /* make sidebar match */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
            border-right: 1px solid rgba(255,255,255,0.06);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str, hero_image_path: str):
    """Hero banner (safe HTML only)."""
    img_b64 = load_image_base64(hero_image_path)

    bg_css = ""
    if img_b64:
        # Background image with dark overlay
        bg_css = f"""
        background-image:
            linear-gradient(rgba(2,6,23,0.78), rgba(2,6,23,0.78)),
            url("data:image/png;base64,{img_b64}");
        background-size: cover;
        background-position: center;
        """
    else:
        # Fallback if image missing
        bg_css = "background: linear-gradient(135deg, #0b1220, #020617);"

    st.markdown(
        f"""
        <style>
        .hero {{
            {bg_css}
            border-radius: 18px;
            padding: 3.2rem 3rem;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 18px 45px rgba(0,0,0,0.35);
            margin-bottom: 1.75rem;
        }}
        .hero h1 {{
            color: #ffffff;
            font-size: 2.7rem;
            margin: 0 0 0.6rem 0;
        }}
        .hero p {{
            color: rgba(226,232,240,0.88);
            font-size: 1.08rem;
            max-width: 780px;
            margin: 0;
            line-height: 1.55;
        }}
        .hero-badges {{
            margin-top: 1.4rem;
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
        }}
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            font-size: 0.85rem;
            color: rgba(226,232,240,0.9);
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.10);
            backdrop-filter: blur(10px);
        }}
        </style>

        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>

        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards():
    st.markdown(
        """
        <style>
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 1rem;
            margin: 1.25rem 0 1.5rem 0;
        }
        .card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1rem 1rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.20);
            min-height: 110px;
        }
        .card h4 {
            margin: 0 0 0.35rem 0;
            color: #ffffff;
            font-size: 1.0rem;
        }
        .card p {
            margin: 0;
            color: rgba(148,163,184,0.95);
            font-size: 0.9rem;
            line-height: 1.45;
        }
        /* responsive */
        @media (max-width: 1100px) {
            .feature-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 650px) {
            .feature-grid { grid-template-columns: 1fr; }
        }
        </style>

        <h2 style="color:white; margin-top: 0.5rem;">How It Works</h2>
        <div class="feature-grid">

        <div class="card">
            <div class="card-head">
            <span style="font-size:1.2rem;">🧠</span>
            <h4 style="margin:0;">Deep Learning Model</h4>
            </div>
            <p>MobileNetV2-based CNN performs lumbar MRI classification.</p>
        </div>

        <div class="card">
            <div class="card-head">
            <span style="font-size:1.2rem;">📤</span>
            <h4 style="margin:0;">Image Upload</h4>
            </div>
            <p>Upload a lumbar spine MRI scan in JPG or PNG format.</p>
        </div>

        <div class="card">
            <div class="card-head">
            <span style="font-size:1.2rem;">⚡</span>
            <h4 style="margin:0;">Instant Prediction</h4>
            </div>
            <p>Get a prediction with confidence scoring in seconds.</p>
        </div>

        <div class="card">
            <div class="card-head">
            <span style="font-size:1.2rem;">🧪</span>
            <h4 style="margin:0;">Educational Use</h4>
            </div>
            <p>Designed for learning & demonstration — not medical diagnosis.</p>
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# App
# ==================================================
inject_global_css()

render_hero(
    title="Spinal Disease Classifier",
    subtitle="AI-assisted lumbar spine MRI classification using deep learning. Upload an MRI scan to receive an instant prediction with confidence scoring.",
    hero_image_path=HERO_IMAGE,
)

render_feature_cards()

st.markdown(
    """
    <div style="color: rgba(226,232,240,0.9); max-width: 920px; line-height: 1.6;">
      <strong>Disclaimer:</strong> This tool is intended for educational and research exploration only.
      It is not a medical device and must not be used for diagnosis or treatment.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ==================================================
# Load model
# ==================================================
try:
    model, class_names = load_classifier(MODEL_PATH, LABELS_PATH)
except Exception as e:
    st.error(f"Error loading model/labels: {e}")
    st.stop()

if model is None:
    st.error(
        "Model not found. Train or place the model at: model/spinal_classifier.keras"
    )
    st.info("Expected paths:\n- model/spinal_classifier.keras\n- model/labels.txt")
    st.stop()

# ==================================================
# Upload
# ==================================================
st.markdown("## Upload a Lumbar Spine MRI Scan")
uploaded_file = st.file_uploader(
    "Upload an MRI scan (JPG / PNG)", type=["jpg", "jpeg", "png"]
)

# ==================================================
# Prediction UI
# ==================================================
if uploaded_file:
    st.divider()
    left, right = st.columns([1, 1], gap="large")

    with left:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded MRI Scan", use_container_width=True)

    with right:
        with st.spinner("Analyzing MRI scan..."):
            class_name, confidence = classify(image, model, class_names)

        st.markdown("### 🎯 Classification Result")

        if class_name.lower() == "normal":
            st.success(f"**Result:** {class_name.upper()}")
        else:
            st.warning(f"**Result:** {class_name.upper()}")

        st.markdown(f"**Confidence:** {confidence:.2%}")
        st.progress(float(confidence))

        st.divider()

        st.markdown("### 🤖 AI Interpretation")
        if is_api_configured():
            with st.spinner("Generating AI analysis..."):
                analysis = get_ai_analysis(class_name, confidence)
            st.info(analysis if analysis else "AI analysis unavailable.")
        else:
            with st.expander("Enable AI Analysis (Optional)"):
                st.markdown(get_api_setup_instructions())

        st.divider()

        st.markdown("### 📊 Confidence Assessment")
        if confidence > 0.90:
            st.success("High confidence prediction.")
        elif confidence > 0.70:
            st.warning("Moderate confidence. Consider professional review.")
        else:
            st.error("Low confidence. Image quality may be insufficient.")

        st.divider()

        st.markdown("### 💡 General Recommendations")
        if class_name.lower() != "normal":
            st.markdown(
                """
                - Consult a medical professional  
                - Consider further diagnostic imaging  
                - Monitor symptoms over time  
                """
            )
        else:
            st.markdown(
                """
                - Maintain good posture and spinal health  
                - Regular exercise and mobility work recommended  
                - Seek medical advice if symptoms persist  
                """
            )

# ==================================================
# Sidebar
# ==================================================
with st.sidebar:
    st.markdown("## 🛠️ Technical Overview")
    st.markdown(
        """
        - **Model:** MobileNetV2 (Transfer Learning)  
        - **Input Size:** 224 × 224  
        - **Classes:** Pain / No Pain  
        - **Deployment:** Streamlit  
        """
    )

    st.divider()

    st.markdown("## 📌 Best Practices")
    st.markdown(
        """
        - Use clear, high-quality MRI scans  
        - Proper orientation improves results  
        - Convert DICOM files to JPG/PNG  
        """
    )

    st.divider()

    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared")

# ==================================================
# Footer
# ==================================================
st.divider()
st.markdown(
    """
    <div style="text-align:center; color: rgba(148,163,184,0.95); padding-bottom: 1rem;">
        <a href="https://github.com/henryagyare/Spine_LBP" target="_blank">GitHub</a> •
        <a href="https://henryasante.vercel.app/" target="_blank">Portfolio</a>
        <br/><br/>
        Educational & research use only.
    </div>
    """,
    unsafe_allow_html=True,
)
