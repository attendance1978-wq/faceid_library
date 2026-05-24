"""
Face detection module
"""

import numpy as np
import cv2
from typing import List, Dict, Tuple, Optional
import warnings

try:
    import mediapipe as mp
    MP_AVAILABLE = True
except ImportError:
    MP_AVAILABLE = False
    warnings.warn("MediaPipe not installed. Using OpenCV detector.")

class FaceDetector:
    """
    Multi-backend face detector
    """
    
    def __init__(self, backend: str = "mediapipe", device: str = "auto"):
        """
        Initialize face detector
        
        Args:
            backend: Detection backend ('mediapipe', 'opencv')
            device: Computing device
        """
        self.backend = backend
        self.device = device
        self.detector = None
        self._init_detector()
    
    def _init_detector(self):
        """Initialize the selected detector"""
        if self.backend == "mediapipe" and MP_AVAILABLE:
            self.mp_face_detection = mp.solutions.face_detection
            self.detector = self.mp_face_detection.FaceDetection(
                model_selection=1, min_detection_confidence=0.5
            )
        elif self.backend == "opencv":
            # Load OpenCV's face detector
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.detector = cv2.CascadeClassifier(cascade_path)
        else:
            # Fallback to OpenCV
            self.backend = "opencv"
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.detector = cv2.CascadeClassifier(cascade_path)
    
    def detect_faces(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces in image
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            List of dictionaries with 'bbox' and 'confidence' keys
        """
        if self.backend == "mediapipe" and MP_AVAILABLE:
            return self._detect_mediapipe(image)
        else:
            return self._detect_opencv(image)
    
    def _detect_mediapipe(self, image: np.ndarray) -> List[Dict]:
        """Detect faces using MediaPipe"""
        results = self.detector.process(image)
        faces = []
        
        if results.detections:
            h, w = image.shape[:2]
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                x2 = int((bbox.xmin + bbox.width) * w)
                y2 = int((bbox.ymin + bbox.height) * h)
                
                faces.append({
                    'bbox': [x1, y1, x2, y2],
                    'confidence': detection.score[0]
                })
        
        return faces
    
    def _detect_opencv(self, image: np.ndarray) -> List[Dict]:
        """Detect faces using OpenCV cascade classifier"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces_rect = self.detector.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        
        faces = []
        for (x, y, w, h) in faces_rect:
            faces.append({
                'bbox': [x, y, x + w, y + h],
                'confidence': 0.9  # OpenCV cascade doesn't provide confidence
            })
        
        return faces
    
    def __repr__(self):
        return f"FaceDetector(backend={self.backend})"
