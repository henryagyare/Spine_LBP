#!/bin/bash

# Sample dataset downloader for Spinal Disease Classifier
# This script attempts to download sample spinal MRI images for testing

echo "🔍 Attempting to download sample spinal MRI images..."
echo "=================================================="

cd "$(dirname "$0")"

# Create directories
mkdir -p data/raw/samples

echo ""
echo "📋 Here are the best ways to get spinal MRI data:"
echo ""
echo "1️⃣  KAGGLE (Recommended):"
echo "   - Visit: https://www.kaggle.com/datasets"
echo "   - Search: 'lumbar spine MRI' or 'spine classification'"
echo "   - Download and extract to data/raw/"
echo ""
echo "2️⃣  MENDELEY DATA (Free, No Account):"
echo "   - Visit: https://data.mendeley.com/datasets/k57fr854j2/1"
echo "   - Click 'Download all files'"
echo "   - Extract to data/raw/"
echo ""
echo "3️⃣  SAMPLE DATASETS FROM RESEARCH:"
echo "   - SpineXpert datasets"
echo "   - Grand Challenge competitions"
echo "   - RSNA archives"
echo ""
echo "=================================================="
echo ""
echo "⚠️  Note: Due to medical data privacy and terms of service,"
echo "    I cannot automatically download these datasets."
echo ""
echo "✅  After downloading, run:"
echo "    python organize_dataset.py"
echo ""

