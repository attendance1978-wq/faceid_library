# FaceID - Advanced Face Recognition and Identification Library

![FaceID](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

FaceID is a powerful, easy-to-use face recognition library that provides face detection, recognition, and identification capabilities. Built with modern deep learning techniques, it's designed for both research and production use.

## Features

- 🎯 **Face Detection**: Multiple backends (MediaPipe, OpenCV) for robust detection
- 🔍 **Face Recognition**: State-of-the-art embedding models (FaceNet, ArcFace, VGGFace)
- 💾 **Database Management**: Built-in face database with persistence
- 🚀 **Real-time Processing**: Optimized for video streams
- 📱 **Easy API**: Simple and intuitive interface
- 🎨 **Visualization Tools**: Built-in drawing utilities
- ⚡ **Multiple Backends**: Flexible detector and model selection

## Installation

### Basic Installation

```bash
pip install -r requirements.txt
```

### GPU Support (Optional)

For NVIDIA GPU acceleration with CUDA:

```bash
pip install tensorflow-gpu>=2.8.0
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### 1. Basic Face Recognition

```python
from faceid import FaceID

# Initialize the system
face_system = FaceID()

# Register faces
face_system.register_face("alice.jpg", "alice_001", "Alice")
face_system.register_face("bob.jpg", "bob_002", "Bob")

# Identify faces in new image
results = face_system.identify_face("test_image.jpg")

for result in results:
    if result['matches']:
        best_match = result['matches'][0]
        print(f"Found {best_match['name']} with {best_match['similarity']:.2%} confidence")
    else:
        print("Unknown face detected")
```

### 2. Face Comparison

```python
from faceid import FaceID

face_system = FaceID()

# Compare two faces
similarity = face_system.compare_faces("face1.jpg", "face2.jpg")

if similarity >= 0.6:
    print(f"Same person! Similarity: {similarity:.2%}")
else:
    print(f"Different people. Similarity: {similarity:.2%}")
```

### 3. Face Verification

```python
from faceid import FaceID

face_system = FaceID()

# Register a known person
face_system.register_face("john.jpg", "john_001", "John")

# Verify a test image
is_match, similarity = face_system.verify_face("john_test.jpg", "john_001")

if is_match:
    print(f"Verified! Similarity: {similarity:.2%}")
else:
    print(f"Verification failed. Similarity: {similarity:.2%}")
```

## Advanced Usage

### Real-time Video Recognition

```python
import cv2
from faceid import FaceID

face_system = FaceID()

# Load registered faces
face_system.database.load("my_faces.db")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Identify faces
    results = face_system.identify_face(frame)
    
    for result in results:
        x1, y1, x2, y2 = result['bbox']
        
        if result['matches']:
            name = result['matches'][0]['name']
            color = (0, 255, 0)  # Green
        else:
            name = "Unknown"
            color = (0, 0, 255)  # Red
        
        # Draw box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, name, (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    cv2.imshow('FaceID', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Database Management

```python
from faceid import FaceID

face_system = FaceID()

# Register people
face_system.register_face("alice.jpg", "alice_001", "Alice", 
                         metadata={"dept": "Engineering"})
face_system.register_face("bob.jpg", "bob_002", "Bob",
                         metadata={"dept": "Marketing"})

# Save database
face_system.database.save("faces.db")

# Load database in another session
face_system.database.load("faces.db")

# List all registered people
people = face_system.database.list_people()
for person in people:
    print(f"{person['person_id']}: {person['name']}")
    print(f"  Metadata: {person['metadata']}")

# Get specific person
person = face_system.database.get_person("alice_001")
print(person['name'])

# Delete a person
face_system.database.delete_person("bob_002")

# Clear entire database
face_system.database.clear()
```

### Batch Processing

```python
from faceid import FaceID
import glob

face_system = FaceID()

# Register all people from image files
image_files = glob.glob("people/*.jpg")

for img_path in image_files:
    person_id = Path(img_path).stem
    try:
        face_system.register_face(img_path, person_id, person_id)
        print(f"Registered {person_id}")
    except Exception as e:
        print(f"Failed to register {person_id}: {e}")

# Test on batch
test_files = glob.glob("test/*.jpg")
for test_img in test_files:
    results = face_system.identify_face(test_img)
    print(f"\n{test_img}:")
    for result in results:
        if result['matches']:
            match = result['matches'][0]
            print(f"  Found: {match['name']} ({match['similarity']:.2%})")
```

### Custom Configuration

```python
from faceid import FaceID

# Using ArcFace model with OpenCV detector
face_system = FaceID(
    model_type="arcface",
    detector_backend="opencv",
    device="cuda"  # or "cpu"
)

# Adjust matching threshold (lower = stricter)
results = face_system.identify_face("test.jpg", threshold=0.5)
```

## API Reference

### FaceID Class

#### Initialization
```python
FaceID(model_type="facenet", detector_backend="mediapipe", device="auto")
```
- `model_type`: "facenet", "arcface", or "vggface"
- `detector_backend`: "mediapipe" or "opencv"
- `device`: "auto", "cpu", or "cuda"

#### Methods

**register_face(image, person_id, person_name, metadata)**
- Register a new face in the database
- Returns: True if successful
- Raises: ValueError if no/multiple faces detected

**identify_face(image, threshold=0.6)**
- Identify faces in an image
- Returns: List of detection results with matches

**compare_faces(face1, face2)**
- Compare two faces
- Returns: Similarity score (0-1)

**verify_face(image, person_id, threshold=0.6)**
- Verify if a face matches a specific person
- Returns: (is_match, similarity_score) tuple

**train_model(images_dir, save_path)**
- Fine-tune the model (coming soon)

### FaceDatabase Class

**add_person(person_id, name, encoding, metadata)**
- Add person to database

**find_matches(encoding, threshold)**
- Find matching persons

**get_encoding(person_id)**
- Get face encoding for a person

**get_person(person_id)**
- Get person information

**delete_person(person_id)**
- Remove person from database

**list_people()**
- Get all registered people

**save(path)**
- Save database to file

**load(path)**
- Load database from file

**clear()**
- Clear all data

### Utility Functions

**load_image(source)**
- Load image from file path, URL, or numpy array

**validate_image(image)**
- Validate image format

**draw_boxes(image, boxes, labels, colors)**
- Draw bounding boxes on image

**compare_faces(encoding1, encoding2, threshold)**
- Compare two face encodings

## Running the Demo

Interactive demo with menu:

```bash
python -c "from faceid.demo import run_demo; run_demo()"
```

The demo provides:
- Face registration from images
- Real-time camera recognition
- Face comparison
- Database management

## Supported Models

### Face Detection Backends
- **MediaPipe**: Fast, accurate, recommended
- **OpenCV Cascade**: Lightweight, no dependencies

### Face Recognition Models
- **FaceNet**: High accuracy, widely used
- **ArcFace**: State-of-the-art, excellent performance
- **VGGFace**: Reliable, well-tested

## Requirements

- Python 3.7+
- NumPy
- OpenCV
- TensorFlow
- MediaPipe (optional but recommended)
- NumPy
- Requests

## Performance Tips

1. **Reduce frame rate** for real-time processing
2. **Use GPU** for faster inference
3. **Adjust thresholds** based on your use case
4. **Batch process** when possible
5. **Cache encodings** for known faces

## Troubleshooting

### No faces detected
- Ensure good lighting
- Try increasing image resolution
- Check that faces are frontally oriented

### Low accuracy
- Increase database samples per person
- Adjust similarity threshold
- Try different model (ArcFace for better accuracy)

### Performance issues
- Switch to "opencv" detector (lighter)
- Use GPU acceleration
- Reduce image resolution
- Process every Nth frame in video

## Project Structure

```
faceid/
├── __init__.py          # Package initialization
├── core.py              # Main FaceID class
├── models.py            # Face encoding models
├── detector.py          # Face detection
├── database.py          # Face database
├── utils.py             # Utility functions
└── demo.py              # Interactive demo

setup.py                 # Package setup
requirements.txt         # Dependencies
README.md               # This file
```

## License

MIT License - See LICENSE file for details

## Citation

If you use FaceID in your research, please cite:

```bibtex
@software{faceid2024,
  title={FaceID: Advanced Face Recognition Library},
  author={FaceID Team},
  year={2024},
  url={https://github.com/faceid/faceid}
}
```

## Contributing

Contributions are welcome! Areas for improvement:
- Additional face recognition models
- Real-time training
- Distributed processing
- More comprehensive tests
- Performance optimizations

## Support

- **Documentation**: https://faceid.readthedocs.io
- **Issues**: https://github.com/faceid/faceid/issues
- **Email**: support@faceid.com

## Changelog

### v1.0.0 (Initial Release)
- Face detection (MediaPipe, OpenCV)
- Face recognition (FaceNet, ArcFace, VGGFace)
- Database management with persistence
- Real-time video support
- Comprehensive utility functions
- Interactive demo

## Acknowledgments

Built with inspiration from:
- FaceNet (Schroff et al.)
- ArcFace (Deng et al.)
- MediaPipe (Google)
- OpenCV community

---

**Made with ❤️ by FaceID Team**
