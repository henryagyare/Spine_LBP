# 🏥 Lumbar Spine MRI Dataset

**Discrete Structures Final Project - Training Data**

This dataset contains processed MRI images used for training the Spinal Disease Classifier model.

---

## 📊 Dataset Overview

**Source:** Extracted from Mendeley Lumbar Spine MRI Dataset  
**Processing:** DICOM (.ima) files converted to PNG format  
**Total Images:** 200  
**Classes:** 2 (with_pain, without_pain)

---

## 📁 Dataset Structure

```
data/
├── train/
│   ├── with_pain/       (70 images)
│   └── without_pain/    (70 images)
└── validation/
    ├── with_pain/       (30 images)
    └── without_pain/    (30 images)
```

---

## 📈 Dataset Statistics

**Training Set:**
- With Pain: 70 images
- Without Pain: 70 images
- Total: 140 images

**Validation Set:**
- With Pain: 30 images
- Without Pain: 30 images
- Total: 60 images

**Split Ratio:** 70% train, 30% validation

---

## 🔄 Data Processing

1. **Source:** Original DICOM (.ima) files from Mendeley dataset
2. **Conversion:** DICOM → PNG using PyDICOM
3. **Normalization:** Pixel values normalized to 0-255
4. **Format:** RGB PNG images
5. **Size:** 224×224 pixels (resized during training)

---

## 🎯 Usage

This dataset is designed for training a binary classification model:

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Create data generator
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    zoom_range=0.2
)

# Load training data
train_generator = train_datagen.flow_from_directory(
    'train/',
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical'
)
```

---

## ⚠️ Important Notes

### Labeling
The "with_pain" and "without_pain" labels were assigned **randomly** for educational/demonstration purposes. This dataset is:

- ✅ Suitable for demonstrating ML workflows
- ✅ Good for learning data preprocessing
- ✅ Useful for understanding model training
- ❌ NOT suitable for actual medical diagnosis
- ❌ NOT clinically validated

### Ethical Considerations
- Images are anonymized medical scans
- Used for educational purposes only
- Should not be used for clinical decision-making
- Proper medical labeling would require expert radiologists

---

## 🔗 Related Repository

**Main Project:** [Spinal Disease Classifier](https://github.com/saabiqsaha/Spinal_pain_DS_class_project)

The main repository contains:
- Complete ML pipeline
- Model training code
- Streamlit web application
- AI-powered analysis
- Full documentation

---

## 📊 Image Specifications

**Format:** PNG  
**Color Mode:** RGB  
**Original Size:** Variable  
**Training Size:** Resized to 224×224  
**Bit Depth:** 8-bit  
**Average File Size:** ~110KB per image

---

## 🎓 Educational Purpose

This dataset was created for a Discrete Structures course project to demonstrate:

- Medical image preprocessing
- Dataset organization
- Train/validation splitting
- Data augmentation techniques
- Binary classification tasks

---

## 👥 Project Team

- **Mohammed Abdulai** - UI/UX Design & Application Development
- **Henry Asante** - Model Training & Optimization
- **Chris Gadze** - Dataset Acquisition & Preparation

---

## 📄 Original Dataset Source

**Mendeley Data:**  
Lumbar Spine MRI Dataset  
https://data.mendeley.com/datasets/k57fr854j2/1

515 patients with symptomatic back pain  
Sagittal and axial views of lumbar vertebrae

---

## 📝 Citation

If you use this processed dataset, please acknowledge:

1. The original Mendeley dataset source
2. Our preprocessing and organization work
3. Educational/non-clinical nature of labels

---

## ⚠️ Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY**

This dataset is part of a student project and should not be used for:
- Clinical diagnosis
- Medical decision-making
- Patient care
- Research requiring validated medical labels

Always consult qualified healthcare professionals for medical imaging interpretation.

---

## 📊 Dataset Statistics Summary

| Category | Train | Validation | Total |
|----------|-------|------------|-------|
| With Pain | 70 | 30 | 100 |
| Without Pain | 70 | 30 | 100 |
| **Total** | **140** | **60** | **200** |

---

## 🔒 License & Usage

This processed dataset is provided for educational purposes. Original source data follows the licensing terms of the Mendeley dataset. Please respect medical data privacy and ethical guidelines.

---

**Created for Discrete Structures Final Project**  
**Course Project - Educational Use Only**

