@"
Quick Start Guide
=================

Basic Usage
-----------

Here's a simple example to get you started with FaceID:

.. code-block:: python

   from faceid import FaceID
   import cv2

   # Initialize the system
   face_system = FaceID()

   # Register a face from an image
   face_system.register_face("paul.jpg", "paul", "Paul")

   # Recognize faces in an image
   results = face_system.identify_face("test.jpg")
   
   for result in results:
       if result['matches']:
           best_match = result['matches'][0]
           print(f"Recognized: {best_match['name']}")
           print(f"Confidence: {best_match['similarity']:.1%}")

Real-time Camera Recognition
----------------------------

.. code-block:: python

   from faceid import FaceID
   import cv2

   face_system = FaceID()
   cap = cv2.VideoCapture(0)

   while True:
       ret, frame = cap.read()
       results = face_system.identify_face(frame)
       
       for result in results:
           x1, y1, x2, y2 = result['bbox']
           if result['matches']:
               name = result['matches'][0]['name']
               # Draw green box for recognized faces
               cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
               cv2.putText(frame, name, (x1, y1-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
           else:
               # Draw red box for unknown faces
               cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
               cv2.putText(frame, "Unknown", (x1, y1-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
       
       cv2.imshow('FaceID', frame)
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

   cap.release()
   cv2.destroyAllWindows()

Run the Interactive Demo
------------------------

.. code-block:: bash

   python -c "from faceid.demo import run_demo; run_demo()"

The demo provides:
1. Register faces from images
2. Test recognition on images
3. Real-time camera recognition
4. Compare two faces
5. List registered people
"@ | Out-File -FilePath quickstart.rst -Encoding UTF8