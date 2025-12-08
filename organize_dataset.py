"""
Script to help organize downloaded dataset into training structure
"""

import os
import shutil
from pathlib import Path
import random


def organize_from_raw():
    """Organize images from data/raw into train/validation split."""
    raw_dir = Path('data/raw')
    
    if not raw_dir.exists():
        print("❌ data/raw directory not found!")
        print("📋 Please download your dataset and place it in data/raw/")
        return
    
    # Find all images in raw directory
    image_extensions = ['.jpg', '.jpeg', '.png', '.dcm']
    all_images = []
    
    for ext in image_extensions:
        all_images.extend(list(raw_dir.rglob(f'*{ext}')))
        all_images.extend(list(raw_dir.rglob(f'*{ext.upper()}')))
    
    if not all_images:
        print("❌ No images found in data/raw/")
        print("📋 Supported formats: JPG, JPEG, PNG, DICOM")
        return
    
    print(f"\n✅ Found {len(all_images)} images in data/raw/")
    print("\n📋 Please manually organize your images:")
    print("   Look at each image and determine if it's normal or abnormal")
    print("   Then move them to:")
    print("   - data/train/normal/")
    print("   - data/train/abnormal/")
    print("   - data/validation/normal/")
    print("   - data/validation/abnormal/")
    print("\n💡 Tip: Use 70-80% for training, 20-30% for validation")
    
    # Show sample of found images
    print("\n📸 Sample of found images:")
    for img in all_images[:10]:
        print(f"   {img}")
    
    if len(all_images) > 10:
        print(f"   ... and {len(all_images) - 10} more")


def auto_split_organized_data():
    """
    If user has already organized into normal/abnormal in raw,
    automatically split into train/validation.
    """
    raw_normal = Path('data/raw/normal')
    raw_abnormal = Path('data/raw/abnormal')
    
    if not (raw_normal.exists() and raw_abnormal.exists()):
        print("\n💡 Alternative: Organize your images in data/raw/ as:")
        print("   data/raw/normal/     (all normal images)")
        print("   data/raw/abnormal/   (all abnormal images)")
        print("   Then run this script again for auto-split")
        return
    
    # Get all images
    normal_images = list(raw_normal.glob('*.[jp][pn][g]')) + list(raw_normal.glob('*.[JP][PN][G]'))
    abnormal_images = list(raw_abnormal.glob('*.[jp][pn][g]')) + list(raw_abnormal.glob('*.[JP][PN][G]'))
    
    if not normal_images or not abnormal_images:
        print("❌ No images found in data/raw/normal or data/raw/abnormal")
        return
    
    print(f"\n✅ Found {len(normal_images)} normal and {len(abnormal_images)} abnormal images")
    
    # Shuffle
    random.shuffle(normal_images)
    random.shuffle(abnormal_images)
    
    # Split 70-30
    split_ratio = 0.7
    normal_split = int(len(normal_images) * split_ratio)
    abnormal_split = int(len(abnormal_images) * split_ratio)
    
    # Create directories
    for split in ['train', 'validation']:
        for class_name in ['normal', 'abnormal']:
            Path(f'data/{split}/{class_name}').mkdir(parents=True, exist_ok=True)
    
    # Copy files
    print("\n📁 Copying files...")
    
    # Normal images
    for i, img in enumerate(normal_images):
        if i < normal_split:
            dest = Path(f'data/train/normal/{img.name}')
        else:
            dest = Path(f'data/validation/normal/{img.name}')
        shutil.copy2(img, dest)
    
    # Abnormal images
    for i, img in enumerate(abnormal_images):
        if i < abnormal_split:
            dest = Path(f'data/train/abnormal/{img.name}')
        else:
            dest = Path(f'data/validation/abnormal/{img.name}')
        shutil.copy2(img, dest)
    
    print("✅ Dataset organized successfully!")
    print("\n📊 Summary:")
    print(f"   Training Normal: {len(list(Path('data/train/normal').glob('*')))}")
    print(f"   Training Abnormal: {len(list(Path('data/train/abnormal').glob('*')))}")
    print(f"   Validation Normal: {len(list(Path('data/validation/normal').glob('*')))}")
    print(f"   Validation Abnormal: {len(list(Path('data/validation/abnormal').glob('*')))}")
    
    print("\n🚀 Ready to train! Run: python train_model.py")


def main():
    print("🏥 Dataset Organization Tool")
    print("=" * 60)
    
    print("\n📋 Choose an option:")
    print("1. I have images in data/raw/ (not organized)")
    print("2. I have images in data/raw/normal and data/raw/abnormal")
    print("3. Show me what to do")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        organize_from_raw()
    elif choice == '2':
        auto_split_organized_data()
    else:
        print("\n📖 Dataset Organization Guide:")
        print("=" * 60)
        print("\n Step 1: Download dataset from one of these sources:")
        print("   - Kaggle: https://www.kaggle.com/datasets")
        print("   - Mendeley: https://data.mendeley.com/datasets/k57fr854j2/1")
        print("\n Step 2: Extract downloaded files to data/raw/")
        print("\n Step 3: Organize images:")
        print("   Option A: Put all in data/raw/, run this script (choice 1)")
        print("   Option B: Organize into data/raw/normal and data/raw/abnormal,")
        print("             run this script (choice 2) for automatic split")
        print("\n Step 4: Train the model: python train_model.py")
        print("=" * 60)


if __name__ == '__main__':
    main()

