"""
Core FaceID functionality
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Union
from pathlib import Path
import cv2
from .detector import FaceDetector
from .models import FaceEncoder
from .database import FaceDatabase
from .utils import load_image, validate_image

class FaceID:
    """
    Main FaceID class for face recognition and identification
    
    Features:
    - Face detection in images and video streams
    - Face encoding/embedding generation
    - Face matching and identification
    - Database management for known faces
    - Real-time recognition
    """
    
    def __init__(self, 
                 model_type: str = "facenet",
                 detector_backend: str = "mediapipe",
                 device: str = "auto"):
        """
        Initialize FaceID system
        
        Args:
            model_type: Type of face recognition model ('facenet', 'arcface', 'vggface')
            detector_backend: Face detector backend ('mediapipe', 'opencv')
            device: Computing device ('auto', 'cpu', 'cuda')
        """
        self.detector = FaceDetector(backend=detector_backend, device=device)
        self.encoder = FaceEncoder(model_type=model_type, device=device)
        self.database = FaceDatabase()
        
    def register_face(self, 
                     image: Union[str, np.ndarray],
                     person_id: str,
                     person_name: str = None,
                     metadata: Dict = None) -> bool:
        """
        Register a new face in the database
        
        Args:
            image: Path to image or numpy array
            person_id: Unique identifier for the person
            person_name: Name of the person
            metadata: Additional metadata
            
        Returns:
            True if registration successful
        """
        # Load and validate image
        img = load_image(image)
        validate_image(img)
        
        # Detect faces
        faces = self.detector.detect_faces(img)
        
        if len(faces) == 0:
            raise ValueError("No face detected in the image")
        elif len(faces) > 1:
            raise ValueError(f"Multiple faces detected ({len(faces)}). Please provide image with single face")
        
        # Get face encoding
        face_box = faces[0]['bbox']
        face_img = self._extract_face(img, face_box)
        encoding = self.encoder.encode(face_img)
        
        # Add to database
        return self.database.add_person(
            person_id=person_id,
            name=person_name or person_id,
            encoding=encoding,
            metadata=metadata
        )
    
    def identify_face(self, 
                     image: Union[str, np.ndarray],
                     threshold: float = 0.6) -> List[Dict]:
        """
        Identify faces in an image
        
        Args:
            image: Path to image or numpy array
            threshold: Similarity threshold for matching (lower = stricter)
            
        Returns:
            List of dictionaries with recognition results
        """
        img = load_image(image)
        validate_image(img)
        
        # Detect all faces
        faces = self.detector.detect_faces(img)
        results = []
        
        for face in faces:
            # Extract face region
            face_img = self._extract_face(img, face['bbox'])
            
            # Get face encoding
            encoding = self.encoder.encode(face_img)
            
            # Find matches in database
            matches = self.database.find_matches(encoding, threshold=threshold)
            
            result = {
                'bbox': face['bbox'],
                'confidence': face['confidence'],
                'matches': matches,
                'encoding': encoding
            }
            
            results.append(result)
            
        return results
    
    def compare_faces(self, 
                     face1: Union[str, np.ndarray],
                     face2: Union[str, np.ndarray]) -> float:
        """
        Compare two faces and return similarity score
        
        Args:
            face1: First face image
            face2: Second face image
            
        Returns:
            Similarity score between 0 and 1
        """
        img1 = load_image(face1)
        img2 = load_image(face2)
        
        # Detect faces
        faces1 = self.detector.detect_faces(img1)
        faces2 = self.detector.detect_faces(img2)
        
        if len(faces1) == 0 or len(faces2) == 0:
            raise ValueError("Could not detect faces in both images")
        
        # Extract and encode faces
        face_img1 = self._extract_face(img1, faces1[0]['bbox'])
        face_img2 = self._extract_face(img2, faces2[0]['bbox'])
        
        encoding1 = self.encoder.encode(face_img1)
        encoding2 = self.encoder.encode(face_img2)
        
        # Calculate similarity
        similarity = self._cosine_similarity(encoding1, encoding2)
        
        return similarity
    
    def verify_face(self, 
                   image: Union[str, np.ndarray],
                   person_id: str,
                   threshold: float = 0.6) -> Tuple[bool, float]:
        """
        Verify if a face matches a specific person
        
        Args:
            image: Face image to verify
            person_id: Person ID to verify against
            threshold: Similarity threshold
            
        Returns:
            (is_match, similarity_score)
        """
        img = load_image(image)
        faces = self.detector.detect_faces(img)
        
        if len(faces) == 0:
            raise ValueError("No face detected in the image")
        
        # Get encoding
        face_img = self._extract_face(img, faces[0]['bbox'])
        encoding = self.encoder.encode(face_img)
        
        # Get stored encoding
        stored_encoding = self.database.get_encoding(person_id)
        
        if stored_encoding is None:
            raise ValueError(f"Person ID '{person_id}' not found in database")
        
        # Calculate similarity
        similarity = self._cosine_similarity(encoding, stored_encoding)
        is_match = similarity >= threshold
        
        return is_match, similarity
    
    def train_model(self, 
                   images_dir: str,
                   save_path: str = None) -> None:
        """
        Train or fine-tune the face recognition model
        
        Args:
            images_dir: Directory containing person folders with images
            save_path: Path to save the trained model
        """
        self.encoder.train(images_dir, save_path)
    
    def _extract_face(self, 
                     image: np.ndarray, 
                     bbox: List[int]) -> np.ndarray:
        """Extract face region from image"""
        x1, y1, x2, y2 = bbox
        face_img = image[y1:y2, x1:x2]
        
        # Resize to expected input size
        face_img = cv2.resize(face_img, (160, 160))
        
        return face_img
    
    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        similarity = dot_product / (norm_a * norm_b)
        # Scale from [-1, 1] to [0, 1]
        return (similarity + 1) / 2
    
    def __repr__(self):
        return f"FaceID(model={self.encoder.model_type}, database_size={len(self.database)})"
