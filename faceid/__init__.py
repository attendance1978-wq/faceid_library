"""
FaceID - Advanced Face Recognition and Identification Library
A comprehensive library for face detection, recognition, and identification
"""

from .core import FaceID
from .models import FaceEncoder
from .database import FaceDatabase
from .detector import FaceDetector
from .utils import load_image, draw_boxes, compare_faces

__version__ = "1.0.0"
__author__ = "FaceID Team"
__all__ = [
    "FaceID",
    "FaceEncoder", 
    "FaceDatabase",
    "FaceDetector",
    "load_image",
    "draw_boxes",
    "compare_faces"
]
