"""
Training script for Spinal Disease Classifier
Uses MobileNet-V2 for transfer learning on lumbar spine MRI images
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

import tensorflow as tf
import keras
print("TF version:", tf.__version__)
print("Keras version:", keras.__version__)


# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 50
LEARNING_RATE = 0.001

# Data paths
TRAIN_DIR = 'data/train'
VAL_DIR = 'data/validation'
# MODEL_SAVE_PATH = 'model/spinal_classifier.h5'
MODEL_SAVE_PATH = 'model/spinal_classifier.keras'


def check_dataset():
    """Check if dataset directories exist and contain images."""
    if not os.path.exists(TRAIN_DIR):
        raise FileNotFoundError(f"Training directory not found: {TRAIN_DIR}")
    
    if not os.path.exists(VAL_DIR):
        raise FileNotFoundError(f"Validation directory not found: {VAL_DIR}")
    
    # Count images in each class
    classes = [d for d in os.listdir(TRAIN_DIR) 
               if os.path.isdir(os.path.join(TRAIN_DIR, d)) and not d.startswith('.')]
    print("\n📊 Dataset Summary:")
    print("=" * 50)
    
    for split_name, split_dir in [('Training', TRAIN_DIR), ('Validation', VAL_DIR)]:
        print(f"\n{split_name} Data:")
        for class_name in classes:
            class_path = os.path.join(split_dir, class_name)
            if os.path.exists(class_path) and os.path.isdir(class_path):
                num_images = len([f for f in os.listdir(class_path) 
                                if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                print(f"  {class_name}: {num_images} images")
    
    print("=" * 50 + "\n")


def create_data_generators():
    """Create data generators with augmentation for training."""
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        fill_mode='nearest'
    )
    
    # Validation data (only rescaling, no augmentation)
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create generators
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, val_generator


def build_model(num_classes):
    """Build a MobileNetV2-based model for spinal disease classification."""
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the base model
    base_model.trainable = False
    
    # Build the model
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # Compile the model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def plot_training_history(history):
    """Plot training and validation accuracy/loss."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Accuracy plot
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Loss plot
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('model/training_history.png')
    print("\n✅ Training history plot saved to 'model/training_history.png'")


def main():
    """Main training function."""
    print("🏥 Spinal Disease Classifier Training")
    print("=" * 50)
    
    # Check dataset
    try:
        check_dataset()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n📋 Please organize your dataset as follows:")
        print("data/")
        print("  ├── train/")
        print("  │   ├── normal/")
        print("  │   └── abnormal/")
        print("  └── validation/")
        print("      ├── normal/")
        print("      └── abnormal/")
        return
    
    # Create data generators
    print("🔄 Creating data generators...")
    train_generator, val_generator = create_data_generators()
    
    num_classes = len(train_generator.class_indices)
    print(f"\n🏷️  Classes: {list(train_generator.class_indices.keys())}")
    print(f"📊 Number of classes: {num_classes}")
    
    # Build model
    print("\n🏗️  Building model...")
    model = build_model(num_classes)
    
    # Print model summary
    print("\n📋 Model Architecture:")
    model.summary()
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        keras.callbacks.ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train the model
    print(f"\n🚀 Starting training for {EPOCHS} epochs...")
    print("=" * 50)
    
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Plot training history
    plot_training_history(history)
    
    # Save class labels
    class_labels = list(train_generator.class_indices.keys())
    with open('model/labels.txt', 'w') as f:
        for i, label in enumerate(class_labels):
            f.write(f"{i} {label}\n")
    
    print("\n✅ Model saved to:", MODEL_SAVE_PATH)
    print("✅ Labels saved to: model/labels.txt")
    
    # Evaluate on validation set
    print("\n📊 Evaluating model on validation set...")
    val_loss, val_accuracy = model.evaluate(val_generator)
    print(f"\n✅ Validation Accuracy: {val_accuracy*100:.2f}%")
    print(f"✅ Validation Loss: {val_loss:.4f}")
    
    # Get predictions for confusion matrix
    print("\n🔍 Generating predictions for detailed analysis...")
    val_generator.reset()
    predictions = model.predict(val_generator, verbose=1)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = val_generator.classes
    
    # Print classification report
    print("\n📊 Classification Report:")
    print("=" * 50)
    print(classification_report(
        true_classes,
        predicted_classes,
        target_names=class_labels
    ))
    
    # Print confusion matrix
    print("\n📊 Confusion Matrix:")
    print("=" * 50)
    cm = confusion_matrix(true_classes, predicted_classes)
    print(cm)
    
    print("\n🎉 Training completed successfully!")
    print("=" * 50)
    print("\n🚀 To deploy the model, run:")
    print("   streamlit run main.py")


if __name__ == '__main__':
    main()

