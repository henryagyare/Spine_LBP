# 🏥 Spinal Disease Classifier

**Discrete Structures Final Project**

A deep learning application for detecting abnormalities in lumbar spine MRI scans using computer vision and AI-powered analysis.

---

## 👥 Project Team

- **Mohammed Abdulai** - UI/UX Design & Application Development
- **Henry Asante** - Model Training & Optimization  
- **Chris Gadze** - Dataset Acquisition & Preparation

---

## 🛠️ Tech Stack

- **Streamlit** - Web Framework
- **Python** - Programming Language
- **MobileNet-V2** - Model Architecture
- **TensorFlow/Keras** - Deep Learning Framework
- **PyDICOM** - Medical Image Processing
- **Groq AI** - Post-prediction Analysis

---

## 📊 Project Overview

This application demonstrates the application of machine learning in healthcare, specifically for spinal disease classification. The model:

- Uses **MobileNet-V2** architecture (lightweight and efficient)
- Classifies spine MRI scans into "with pain" or "without pain"
- Provides **AI-powered post-prediction analysis** using Groq's Llama 3.3 70B model
- Achieves **51.67% validation accuracy** on the test dataset

---

## 🚀 Features

- ✅ Real-time MRI scan classification
- ✅ Confidence score visualization
- ✅ AI-powered diagnostic analysis
- ✅ Educational recommendations
- ✅ Professional medical interface
- ✅ Responsive web design

---

## 📁 Project Structure

```
Spinal-Disease-Classifier/
├── main.py                 # Streamlit web application
├── train_model.py          # Model training script
├── ai_analysis.py          # AI analysis integration
├── utils.py                # Helper functions
├── requirements.txt        # Python dependencies
├── model/                  # Trained model files
│   ├── spinal_classifier.h5
│   ├── labels.txt
│   └── training_history.png
├── API_SETUP.md           # AI setup guide
├── QUICKSTART.md          # Quick start guide
└── DATASET_GUIDE.md       # Dataset instructions
```

**📊 Dataset Repository:** [Spinal_Dataset](https://github.com/saabiqsaha/Spinal_Dataset)  
The training and validation images (200 MRI scans) are hosted separately.

---

## 🔧 Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/saabiqsaha/Spinal_pain_DS_class_project.git
cd Spinal_pain_DS_class_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🎯 Running the Application

```bash
# Start the Streamlit app
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🤖 AI Analysis Setup (Optional)

To enable AI-powered post-prediction analysis:

1. Get a free API key from [Groq Console](https://console.groq.com/keys)
2. Copy `.env.example` to `.env`
3. Add your API key to `.env`:
   ```
   GROQ_API_KEY=your_key_here
   ```
4. Restart the app

See [GET_API_KEY.md](GET_API_KEY.md) for detailed instructions.

---

## 📊 Model Details

**Architecture:** MobileNet-V2 (pre-trained on ImageNet)

**Training Configuration:**
- Input Size: 224×224 RGB images
- Training Images: 140 (70 per class)
- Validation Images: 60 (30 per class)
- Epochs: 16 (early stopping)
- Optimizer: Adam (lr=0.001)
- Batch Size: 16

**Performance:**
- Training Accuracy: ~72%
- Validation Accuracy: 51.67%
- Model Size: 11 MB

---

## 🎓 Educational Context

This project demonstrates:

- **Transfer Learning** - Using pre-trained MobileNet-V2
- **Medical Image Processing** - DICOM to PNG conversion
- **Data Augmentation** - Rotation, flipping, zoom
- **API Integration** - Groq AI for analysis
- **Web Deployment** - Streamlit framework
- **Environment Management** - Secure API key handling

---

## 📸 Screenshots

### Main Interface
Upload MRI scans and get instant predictions with confidence scores.

### AI Analysis
Post-prediction analysis provides medical context and recommendations.

### Model Performance
Training history and validation metrics visualization.

---

## 🔒 Security

- API keys stored in `.env` (not committed to version control)
- Secure environment variable loading
- Input validation and error handling
- Medical disclaimer for educational use

---

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step setup guide
- **[API_SETUP.md](API_SETUP.md)** - AI analysis configuration
- **[GET_API_KEY.md](GET_API_KEY.md)** - Quick API key guide
- **[DATASET_GUIDE.md](DATASET_GUIDE.md)** - Dataset preparation
- **[STATUS.md](STATUS.md)** - Project status and overview

---

## ⚠️ Disclaimer

This application is developed for **educational purposes only** as part of a Discrete Structures course project. It is not intended for clinical use and should not be used as a substitute for professional medical diagnosis. Always consult qualified healthcare professionals for medical advice.

---

## 🙏 Acknowledgments

- **Mendeley Data** - Lumbar Spine MRI Dataset
- **TensorFlow/Keras** - Deep learning framework
- **Streamlit** - Web application framework
- **Groq** - AI analysis API
- **MobileNet** - Model architecture

---

## 📄 License

This project is created for educational purposes. Please respect data privacy and medical ethics guidelines when using or extending this work.

---

## 📞 Contact

For questions or feedback about this project, please contact the team members through the university.

---

**Built with ❤️ for Discrete Structures Final Project**
