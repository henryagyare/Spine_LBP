"""
Helper script to download and organize spinal MRI datasets

This script provides multiple options for dataset acquisition:
1. Kaggle API (requires setup)
2. Manual download instructions
3. Sample dataset creation for testing
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path


def check_kaggle_setup():
    """Check if Kaggle API is properly configured."""
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    if not kaggle_json.exists():
        return False
    return True


def setup_kaggle():
    """Guide user through Kaggle API setup."""
    print("\n📋 Kaggle API Setup Instructions:")
    print("=" * 60)
    print("1. Go to https://www.kaggle.com/")
    print("2. Log in to your account")
    print("3. Click on your profile picture → Settings")
    print("4. Scroll down to 'API' section")
    print("5. Click 'Create New Token'")
    print("6. This will download 'kaggle.json'")
    print("7. Move it to ~/.kaggle/ directory:")
    print("   mkdir -p ~/.kaggle")
    print("   mv ~/Downloads/kaggle.json ~/.kaggle/")
    print("   chmod 600 ~/.kaggle/kaggle.json")
    print("=" * 60)


def download_from_kaggle(dataset_name):
    """Download dataset from Kaggle."""
    try:
        import kaggle
        print(f"\n📥 Downloading dataset: {dataset_name}")
        kaggle.api.dataset_download_files(dataset_name, path='data/raw', unzip=True)
        print("✅ Download complete!")
        return True
    except Exception as e:
        print(f"❌ Error downloading from Kaggle: {e}")
        return False


def create_sample_dataset():
    """Create a sample dataset structure for testing."""
    print("\n🔧 Creating sample dataset structure...")
    
    # Create directories
    for split in ['train', 'validation']:
        for class_name in ['normal', 'abnormal']:
            path = f'data/{split}/{class_name}'
            os.makedirs(path, exist_ok=True)
    
    print("✅ Directory structure created!")
    print("\n📋 Next steps:")
    print("1. Add your MRI images to the following folders:")
    print("   - data/train/normal/      (100-150 normal spine images)")
    print("   - data/train/abnormal/    (100-150 abnormal spine images)")
    print("   - data/validation/normal/ (30-50 normal spine images)")
    print("   - data/validation/abnormal/ (30-50 abnormal spine images)")
    print("\n2. Then run: python train_model.py")


def show_dataset_sources():
    """Display available dataset sources."""
    print("\n📚 Available Dataset Sources:")
    print("=" * 60)
    
    print("\n1️⃣ Kaggle Datasets (Recommended):")
    print("   Search for: 'lumbar spine MRI' or 'spinal disease'")
    print("   URL: https://www.kaggle.com/datasets")
    
    print("\n2️⃣ Mendeley Data:")
    print("   Lumbar Spine MRI Dataset")
    print("   URL: https://data.mendeley.com/datasets/k57fr854j2/1")
    print("   (515 patients, requires manual download)")
    
    print("\n3️⃣ Medical Image Databases:")
    print("   - The Cancer Imaging Archive (TCIA)")
    print("   - OpenNeuro")
    print("   - RadioGraphics Archives")
    
    print("\n4️⃣ Research Datasets:")
    print("   - RSNA Challenges on Kaggle")
    print("   - Grand Challenge (grand-challenge.org)")
    
    print("\n=" * 60)


def main():
    """Main function to handle dataset download."""
    print("🏥 Spinal Disease Classifier - Dataset Setup")
    print("=" * 60)
    
    # Check if data already exists
    if os.path.exists('data/train') and len(os.listdir('data/train')) > 0:
        print("✅ Dataset directory already exists!")
        response = input("\nDo you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    print("\n📋 Select an option:")
    print("1. Download from Kaggle (requires API setup)")
    print("2. View dataset sources for manual download")
    print("3. Create empty structure (I'll add images manually)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        if not check_kaggle_setup():
            print("\n❌ Kaggle API not configured!")
            setup_kaggle()
            print("\n💡 After setup, run this script again.")
        else:
            print("\n🔍 Popular datasets:")
            print("1. Search 'lumbar spine mri' on Kaggle")
            print("2. Example: 'username/dataset-name'")
            
            dataset = input("\nEnter Kaggle dataset name (or 'search' to open browser): ").strip()
            if dataset.lower() == 'search':
                import webbrowser
                webbrowser.open('https://www.kaggle.com/datasets?search=lumbar+spine+mri')
            elif dataset:
                download_from_kaggle(dataset)
    
    elif choice == '2':
        show_dataset_sources()
        print("\n💡 After downloading, organize images into the structure:")
        create_sample_dataset()
    
    elif choice == '3':
        create_sample_dataset()
    
    else:
        print("\n👋 Goodbye!")
        return
    
    print("\n✅ Setup complete!")
    print("🚀 Next step: python train_model.py")


if __name__ == '__main__':
    main()

