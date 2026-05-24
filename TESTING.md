# FaceID Testing Guide

## Installation for Testing

```bash
# Navigate to the project directory
cd faceid

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Test

### 1. Test Imports
```python
python -c "from faceid import FaceID; print('✓ FaceID imported successfully')"
```

### 2. Test Initialization
```python
python -c "from faceid import FaceID; f = FaceID(); print('✓ FaceID initialized'); print(f)"
```

### 3. Test Database
```python
python -c "from faceid.database import FaceDatabase; db = FaceDatabase(); print('✓ Database initialized'); print(db)"
```

### 4. Run Examples

#### Basic Usage
```bash
python examples/01_basic_usage.py
```

#### Database Management
```bash
python examples/03_database_management.py
```

#### Camera Recognition
```bash
python examples/02_camera_recognition.py
```

#### Batch Processing
```bash
python examples/04_batch_processing.py
```

## Manual Testing

### Test 1: Face Registration
```python
from faceid import FaceID

face_system = FaceID()

# Register a face (requires an actual image file)
try:
    face_system.register_face("test_image.jpg", "test_001", "Test Person")
    print("✓ Registration successful")
except Exception as e:
    print(f"✗ Registration failed: {e}")
```

### Test 2: Face Identification
```python
from faceid import FaceID

face_system = FaceID()

# Test on an image
try:
    results = face_system.identify_face("test_image.jpg")
    print(f"✓ Found {len(results)} face(s)")
except Exception as e:
    print(f"✗ Identification failed: {e}")
```

### Test 3: Database Operations
```python
from faceid import FaceDatabase
import numpy as np

db = FaceDatabase()

# Create dummy encoding
dummy_encoding = np.random.randn(128)

# Add person
db.add_person("person_001", "John Doe", dummy_encoding, {"dept": "Engineering"})
print(f"✓ Added person, database size: {len(db)}")

# List people
people = db.list_people()
print(f"✓ Listed {len(people)} people")

# Get person
person = db.get_person("person_001")
print(f"✓ Retrieved person: {person['name']}")

# Save database
db.save("test_db.pkl")
print("✓ Database saved")

# Load database
db2 = FaceDatabase()
db2.load("test_db.pkl")
print(f"✓ Database loaded, size: {len(db2)}")
```

### Test 4: Image Utilities
```python
from faceid.utils import load_image, validate_image, draw_boxes
import numpy as np
import cv2

# Test image loading (requires an actual image file)
try:
    img = load_image("test_image.jpg")
    print(f"✓ Loaded image: {img.shape}")
except Exception as e:
    print(f"Image loading failed: {e}")

# Test image validation
try:
    test_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    validate_image(test_img)
    print("✓ Image validation passed")
except Exception as e:
    print(f"✗ Image validation failed: {e}")

# Test drawing boxes
try:
    test_img = np.zeros((300, 400, 3), dtype=np.uint8)
    boxes = [[50, 50, 150, 150], [200, 100, 300, 200]]
    labels = ["Face 1", "Face 2"]
    result = draw_boxes(test_img, boxes, labels)
    print(f"✓ Drew boxes: {result.shape}")
except Exception as e:
    print(f"✗ Drawing failed: {e}")
```

## Testing with Real Images

### Prepare Test Images
1. Gather some face images (preferably 224x224 or larger)
2. Create a folder structure:
```
data/
├── people/
│   ├── alice/
│   │   └── photo1.jpg
│   └── bob/
│       └── photo1.jpg
└── test/
    └── test_image.jpg
```

### Run Tests
```bash
# Basic usage with your images
python examples/01_basic_usage.py

# Camera test
python examples/02_camera_recognition.py

# Batch test
python examples/04_batch_processing.py
```

## Performance Testing

### Test Inference Speed
```python
import time
from faceid import FaceID
import numpy as np

face_system = FaceID()

# Create test image
test_img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# Warmup
face_system.identify_face(test_img)

# Benchmark
start = time.time()
for i in range(10):
    results = face_system.identify_face(test_img)
elapsed = time.time() - start

print(f"Average time per frame: {elapsed/10:.2f}s")
print(f"FPS: {10/elapsed:.1f}")
```

## Troubleshooting

### Issue: TensorFlow not found
**Solution**: Install TensorFlow
```bash
pip install tensorflow
```

### Issue: MediaPipe not found
**Solution**: Install MediaPipe (optional)
```bash
pip install mediapipe
```

### Issue: OpenCV errors
**Solution**: Reinstall opencv-python
```bash
pip install --upgrade opencv-python
```

### Issue: CUDA/GPU errors
**Solution**: Install GPU-compatible versions
```bash
pip install tensorflow-gpu
```

## Testing Checklist

- [ ] All imports work
- [ ] FaceID initializes without errors
- [ ] Database operations work
- [ ] Face detection works
- [ ] Face encoding works
- [ ] Face comparison works
- [ ] Database persistence works
- [ ] Examples run without crashes
- [ ] Camera detection works
- [ ] Performance is acceptable

## Continuous Integration

For automated testing, use pytest:

```bash
pip install pytest pytest-cov

# Run tests
pytest tests/

# With coverage
pytest --cov=faceid tests/
```

## Reporting Issues

When reporting issues, include:
1. Python version
2. OS and architecture
3. Installed package versions (`pip freeze`)
4. Error traceback
5. Minimal code to reproduce
