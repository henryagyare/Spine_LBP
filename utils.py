import numpy as np
from PIL import Image

def classify(image, model, class_names):
    """
    Classify an image using the trained model.
    
    Args:
        image: PIL Image object
        model: Trained Keras model
        class_names: List of class names
    
    Returns:
        Tuple of (predicted_class_name, confidence_score)
    """
    # Resize image to 224x224
    image = image.resize((224, 224))
    
    # Convert to array and normalize
    image_array = np.asarray(image)
    
    # Normalize pixel values to [0, 1]
    normalized_image_array = image_array.astype(np.float32) / 255.0
    
    # Add batch dimension
    data = np.expand_dims(normalized_image_array, axis=0)
    
    # Make prediction
    prediction = model.predict(data, verbose=0)
    
    # Get the predicted class index and confidence
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    
    return class_name, confidence_score


def preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess an image for model input.
    
    Args:
        image_path: Path to the image file
        target_size: Tuple of (height, width) for resizing
    
    Returns:
        Preprocessed image array
    """
    img = Image.open(image_path).convert('RGB')
    img = img.resize(target_size)
    img_array = np.asarray(img)
    img_array = img_array.astype(np.float32) / 255.0
    
    return img_array

