@"
Examples
========

This page contains complete working examples for common use cases.

Example 1: Basic Face Registration and Recognition
--------------------------------------------------

.. literalinclude:: ../examples/01_basic_usage.py
   :language: python
   :linenos:
   :caption: examples/01_basic_usage.py

Example 2: Real-time Camera Recognition
---------------------------------------

.. literalinclude:: ../examples/02_camera_recognition.py
   :language: python
   :linenos:
   :caption: examples/02_camera_recognition.py

Example 3: Database Management
------------------------------

.. literalinclude:: ../examples/03_database_management.py
   :language: python
   :linenos:
   :caption: examples/03_database_management.py

Example 4: Batch Processing
---------------------------

.. literalinclude:: ../examples/04_batch_processing.py
   :language: python
   :linenos:
   :caption: examples/04_batch_processing.py

Example 5: Custom Recognition Logic
-----------------------------------

Here's an example of custom recognition with confidence threshold:

.. code-block:: python

   from faceid import FaceID
   import cv2

   class CustomFaceRecognition:
       def __init__(self, threshold=0.7):
           self.face_system = FaceID()
           self.threshold = threshold
       
       def recognize_with_feedback(self, image_path):
           results = self.face_system.identify_face(image_path)
           
           for result in results:
               if result['matches']:
                   best_match = result['matches'][0]
                   if best_match['similarity'] >= self.threshold:
                       return best_match['name'], "HIGH_CONFIDENCE"
                   else:
                       return best_match['name'], "LOW_CONFIDENCE"
               else:
                   return None, "NO_MATCH"
           return None, "NO_FACE"

   # Usage
   recognizer = CustomFaceRecognition(threshold=0.75)
   name, status = recognizer.recognize_with_feedback("test.jpg")
   print(f"Recognized: {name}, Status: {status}")

Example 6: Video File Processing
--------------------------------

.. code-block:: python

   from faceid import FaceID
   import cv2

   def process_video(video_path, output_path=None):
       face_system = FaceID()
       cap = cv2.VideoCapture(video_path)
       
       frame_count = 0
       recognized_faces = {}
       
       while cap.isOpened():
           ret, frame = cap.read()
           if not ret:
               break
           
           results = face_system.identify_face(frame)
           
           for result in results:
               if result['matches']:
                   name = result['matches'][0]['name']
                   recognized_faces[name] = recognized_faces.get(name, 0) + 1
           
           frame_count += 1
           
           if frame_count % 100 == 0:
               print(f"Processed {frame_count} frames...")
       
       cap.release()
       
       print("\nRecognition Summary:")
       for name, count in recognized_faces.items():
           print(f"  {name}: detected in {count} frames")
       
       return recognized_faces

   # Process a video file
   results = process_video("test_video.mp4")
"@ | Out-File -FilePath examples.rst -Encoding UTF8