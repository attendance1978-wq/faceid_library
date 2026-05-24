"""
Utility functions for FaceID
"""

import numpy as np
import cv2
from typing import Union, List, Tuple
from pathlib import Path
import requests
from urllib.parse import urlparse

def load_image(source: Union[str, np.ndarray]) -> np.ndarray:
    """
    Load image from file path, URL, or numpy array
    
    Args:
        source: Image source (path, URL, or numpy array)
        
    Returns:
        RGB image as numpy array
    """
    if isinstance(source, np.ndarray):
        # Ensure RGB format
        if len(source.shape) == 2:
            source = cv2.cvtColor(source, cv2.COLOR_GRAY2RGB)
        elif source.shape[2] == 4:
            source = cv2.cvtColor(source, cv2.COLOR_BGRA2RGB)
        elif source.shape[2] == 3:
            # Assume BGR to RGB conversion if needed
            source = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
        return source
    
    # Check if URL
    if is_url(source):
        response = requests.get(source, stream=True)
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Load from file
    img = cv2.imread(str(source))
    if img is None:
        raise ValueError(f"Could not load image from {source}")
    
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def is_url(path: str) -> bool:
    """Check if path is a URL"""
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_image(image: np.ndarray):
    """Validate image format"""
    if not isinstance(image, np.ndarray):
        raise TypeError("Image must be numpy array")
    
    if len(image.shape) not in [2, 3]:
        raise ValueError(f"Invalid image shape: {image.shape}")
    
    if len(image.shape) == 3 and image.shape[2] not in [1, 3, 4]:
        raise ValueError(f"Invalid number of channels: {image.shape[2]}")

def draw_boxes(image: np.ndarray, 
               boxes: List[List[int]], 
               labels: List[str] = None,
               colors: List[Tuple[int, int, int]] = None) -> np.ndarray:
    """
    Draw bounding boxes on image
    
    Args:
        image: Input image
        boxes: List of bounding boxes [x1, y1, x2, y2]
        labels: Optional labels for each box
        colors: Optional colors for each box
        
    Returns:
        Image with drawn boxes
    """
    img = image.copy()
    
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        
        # Choose color
        if colors and i < len(colors):
            color = colors[i]
        else:
            color = (0, 255, 0)  # Green
        
        # Draw rectangle
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        
        # Draw label
        if labels and i < len(labels):
            label = labels[i]
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            cv2.rectangle(img, (x1, y1 - label_size[1] - 5), 
                         (x1 + label_size[0], y1), color, -1)
            cv2.putText(img, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return img

def compare_faces(encoding1: np.ndarray, 
                  encoding2: np.ndarray, 
                  threshold: float = 0.6) -> bool:
    """
    Compare two face encodings
    
    Args:
        encoding1: First face encoding
        encoding2: Second face encoding
        threshold: Similarity threshold
        
    Returns:
        True if faces match
    """
    from .core import FaceID
    similarity = FaceID._cosine_similarity(encoding1, encoding2)
    return similarity >= threshold

def preprocess_face(image: np.ndarray, 
                    target_size: Tuple[int, int] = (160, 160)) -> np.ndarray:
    """
    Preprocess face image for model input
    
    Args:
        image: Input face image
        target_size: Target size (height, width)
        
    Returns:
        Preprocessed image
    """
    # Resize
    img = cv2.resize(image, target_size)
    
    # Normalize to [0, 1]
    img = img.astype(np.float32) / 255.0
    
    # Standardize (mean subtraction)
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img = (img - mean) / std
    
    return img
