# Dataset Acquisition Guide 📚

## What I Can't Do Automatically

Due to authentication requirements and terms of service, I **cannot automatically download** medical image datasets from most sources. Here's what you need to do manually:

---

## ✅ Recommended Datasets

### Option 1: Kaggle (EASIEST)

**Steps:**
1. **Create Kaggle account**: https://www.kaggle.com/
2. **Search for datasets**: "lumbar spine MRI" or "spinal disease classification"
3. **Popular datasets to try:**
   - Search: "spine mri classification"
   - Search: "lumbar spine normal abnormal"
   - RSNA Lumbar Spine competitions

4. **Download:**
   - Click on a dataset
   - Accept terms and conditions
   - Click "Download" button
   - Extract the ZIP file

5. **Organize:**
   ```
   data/
   ├── train/
   │   ├── normal/      ← Put 70% of normal images here
   │   └── abnormal/    ← Put 70% of abnormal images here
   └── validation/
       ├── normal/      ← Put 30% of normal images here
       └── abnormal/    ← Put 30% of abnormal images here
   ```

---

### Option 2: Mendeley Data (FREE, NO ACCOUNT)

**Lumbar Spine MRI Dataset**
- URL: https://data.mendeley.com/datasets/k57fr854j2/1
- Size: 515 patients
- Type: Lumbar spine sagittal and axial views

**Steps:**
1. Visit the URL above
2. Click "Download all files"
3. Extract the ZIP
4. Organize images into normal/abnormal based on labels provided
5. Split into train/validation (70/30 split)

---

### Option 3: Medical Image Archive (ADVANCED)

**The Cancer Imaging Archive (TCIA)**
- URL: https://www.cancerimagingarchive.net/
- Requires: Free account registration
- Contains: Various medical imaging datasets including spinal scans

---

## 🚀 Quick Start After Download

### Using the helper script:
```bash
python download_dataset.py
```
This will:
- Create the directory structure
- Guide you through organization
- Validate your dataset

### Manual organization:
1. Put your images in the folders as shown above
2. Aim for 100-200 images per class minimum
3. Images should be JPEG, JPG, or PNG format
4. For DICOM files, convert them first (see below)

---

## 🔄 Converting DICOM to PNG/JPEG

If your dataset is in DICOM format (.dcm files):

```python
# Install required package
pip install pydicom opencv-python

# Convert script
import pydicom
import cv2
import numpy as np

def dicom_to_png(dicom_path, output_path):
    ds = pydicom.dcmread(dicom_path)
    img = ds.pixel_array
    # Normalize to 0-255
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite(output_path, img)

# Usage
dicom_to_png('scan.dcm', 'scan.png')
```

---

## 📊 Dataset Quality Tips

✅ **Good:**
- Clear, high-resolution images
- Consistent imaging orientation (sagittal or axial)
- Properly labeled (normal vs abnormal)
- Balanced classes (similar number of images in each)

❌ **Avoid:**
- Blurry or low-quality scans
- Mixed image types without organization
- Heavily imbalanced classes
- Images from different body parts

---

## 🎯 Minimum Requirements

- **Training images**: 100-200 per class (normal/abnormal)
- **Validation images**: 30-50 per class
- **Image format**: JPEG, JPG, or PNG
- **Total**: ~300-500 images minimum

---

## ⚡ Testing With Small Dataset

If you want to test the pipeline first:
1. Download just 20-30 images per class
2. Split: 15-20 for training, 5-10 for validation
3. Run training to verify everything works
4. Then add more images for better accuracy

---

## 🆘 Need Help?

If you're stuck:
1. Run `python download_dataset.py` for guided setup
2. Check the README.md for overall project structure
3. Ensure images are in the correct folder structure
4. Verify image formats (use `file image.jpg` command)

---

## 🔍 Example: Quick Kaggle Download

```bash
# 1. Install Kaggle CLI (already done)
pip install kaggle

# 2. Set up credentials
# Download kaggle.json from your Kaggle account
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# 3. Search for datasets
kaggle datasets list -s "lumbar spine mri"

# 4. Download (example dataset name)
kaggle datasets download -d username/spine-mri-dataset

# 5. Unzip
unzip spine-mri-dataset.zip -d data/raw/

# 6. Organize into train/validation folders
# (Do this manually or write a script based on dataset structure)
```

---

## ✅ Validation

Before training, verify your setup:

```bash
# Check structure
tree data/ -L 2

# Count images
echo "Training Normal: $(ls data/train/normal | wc -l)"
echo "Training Abnormal: $(ls data/train/abnormal | wc -l)"
echo "Validation Normal: $(ls data/validation/normal | wc -l)"
echo "Validation Abnormal: $(ls data/validation/abnormal | wc -l)"
```

Expected output:
```
Training Normal: 120
Training Abnormal: 115
Validation Normal: 35
Validation Abnormal: 38
```

---

**Once your dataset is ready, run:** `python train_model.py`

