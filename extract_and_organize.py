"""
Script to extract and organize images from the lumbar spine dataset
Converts .ima (DICOM) files to PNG and organizes into train/validation split
"""

import os
import shutil
import random
from pathlib import Path
import numpy as np
from PIL import Image

try:
    import pydicom
    DICOM_AVAILABLE = True
except ImportError:
    DICOM_AVAILABLE = False
    print("⚠️  pydicom not installed. Installing...")
    os.system("pip install pydicom")
    import pydicom
    DICOM_AVAILABLE = True


def convert_dicom_to_png(dicom_path, output_path):
    """Convert a DICOM (.ima) file to PNG."""
    try:
        # Read DICOM file
        ds = pydicom.dcmread(dicom_path)
        
        # Get pixel array
        img_array = ds.pixel_array
        
        # Normalize to 0-255
        img_array = img_array.astype(float)
        img_array = (img_array - img_array.min()) / (img_array.max() - img_array.min()) * 255.0
        img_array = img_array.astype(np.uint8)
        
        # Convert to PIL Image and save
        img = Image.fromarray(img_array)
        
        # Convert to RGB (needed for training)
        img = img.convert('RGB')
        
        img.save(output_path, 'PNG')
        return True
    except Exception as e:
        print(f"❌ Error converting {dicom_path}: {str(e)}")
        return False


def find_all_dicom_files(base_dir, max_files=None):
    """Find all .ima (DICOM) files in the dataset."""
    print(f"🔍 Searching for DICOM files in {base_dir}...")
    
    dicom_files = []
    base_path = Path(base_dir)
    
    # Find all .ima files
    for ima_file in base_path.rglob('*.ima'):
        dicom_files.append(ima_file)
        if max_files and len(dicom_files) >= max_files:
            break
    
    print(f"✅ Found {len(dicom_files)} DICOM files")
    return dicom_files


def extract_and_organize(source_dir, num_per_class=100, split_ratio=0.7):
    """
    Extract images from dataset and organize into train/validation.
    
    Args:
        source_dir: Directory containing the MRI data
        num_per_class: Number of images per class (pain/no pain)
        split_ratio: Train/validation split ratio (0.7 = 70% train, 30% val)
    """
    print("\n🏥 Lumbar Spine Dataset Organizer")
    print("=" * 60)
    
    # Find all DICOM files
    # We need 200 total (100 per class), but let's get 250 to have extra
    needed_total = num_per_class * 2
    buffer = int(needed_total * 1.3)  # Get 30% extra
    
    all_files = find_all_dicom_files(source_dir, max_files=buffer)
    
    if len(all_files) < needed_total:
        print(f"⚠️  Only found {len(all_files)} files, need {needed_total}")
        print("    Continuing with what we have...")
    
    # Shuffle for randomness
    random.shuffle(all_files)
    
    # Create output directories
    temp_dir = Path('temp_converted')
    temp_dir.mkdir(exist_ok=True)
    
    # Convert DICOM files to PNG
    print(f"\n🔄 Converting {min(len(all_files), needed_total)} DICOM files to PNG...")
    print("    This may take a few minutes...")
    
    converted_files = []
    for i, dicom_file in enumerate(all_files[:needed_total]):
        if i % 20 == 0:
            print(f"    Progress: {i}/{needed_total}")
        
        output_path = temp_dir / f"image_{i:04d}.png"
        if convert_dicom_to_png(dicom_file, output_path):
            converted_files.append(output_path)
        
        if len(converted_files) >= needed_total:
            break
    
    print(f"\n✅ Successfully converted {len(converted_files)} images")
    
    if len(converted_files) < needed_total:
        num_per_class = len(converted_files) // 2
        print(f"⚠️  Adjusting to {num_per_class} images per class")
    
    # Randomly assign to classes (since we don't have labels)
    # In a real scenario, you'd use actual labels
    random.shuffle(converted_files)
    
    with_pain = converted_files[:num_per_class]
    without_pain = converted_files[num_per_class:num_per_class*2]
    
    print(f"\n📊 Dataset split:")
    print(f"   With pain: {len(with_pain)} images")
    print(f"   Without pain: {len(without_pain)} images")
    
    # Split into train/validation
    def split_data(files, ratio):
        split_idx = int(len(files) * ratio)
        return files[:split_idx], files[split_idx:]
    
    train_pain, val_pain = split_data(with_pain, split_ratio)
    train_no_pain, val_no_pain = split_data(without_pain, split_ratio)
    
    print(f"\n📁 Organizing into train/validation folders...")
    print(f"   Training: {len(train_pain)} with pain, {len(train_no_pain)} without pain")
    print(f"   Validation: {len(val_pain)} with pain, {len(val_no_pain)} without pain")
    
    # Create directories
    for split in ['train', 'validation']:
        for class_name in ['with_pain', 'without_pain']:
            path = Path(f'data/{split}/{class_name}')
            path.mkdir(parents=True, exist_ok=True)
    
    # Copy files
    def copy_files(files, dest_dir):
        for i, file in enumerate(files):
            dest = dest_dir / f"spine_{i:04d}.png"
            shutil.copy2(file, dest)
    
    copy_files(train_pain, Path('data/train/with_pain'))
    copy_files(train_no_pain, Path('data/train/without_pain'))
    copy_files(val_pain, Path('data/validation/with_pain'))
    copy_files(val_no_pain, Path('data/validation/without_pain'))
    
    # Clean up temp directory
    print(f"\n🧹 Cleaning up temporary files...")
    shutil.rmtree(temp_dir)
    
    print("\n" + "=" * 60)
    print("✅ Dataset organization complete!")
    print("=" * 60)
    print("\n📊 Final structure:")
    print(f"   data/train/with_pain/     : {len(train_pain)} images")
    print(f"   data/train/without_pain/  : {len(train_no_pain)} images")
    print(f"   data/validation/with_pain/: {len(val_pain)} images")
    print(f"   data/validation/without_pain/: {len(val_no_pain)} images")
    print("\n🚀 Ready to train! Run: python train_model.py")
    print("=" * 60)


def main():
    source_dir = '01_MRI_Data'
    
    if not os.path.exists(source_dir):
        print(f"❌ Error: {source_dir} not found!")
        print("   Make sure the dataset is in the project directory")
        return
    
    print("⚠️  NOTE: Since this dataset doesn't have clear pain/no-pain labels,")
    print("   images will be randomly assigned to each class for demonstration.")
    print("   In a real scenario, you would need proper medical labels.\n")
    
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Extract and organize
    extract_and_organize(source_dir, num_per_class=100, split_ratio=0.7)


if __name__ == '__main__':
    main()

