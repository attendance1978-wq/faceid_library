# Update api.rst (remove the problematic Database class reference)
@"
API Reference
=============

FaceID Class
------------

The main class for face recognition operations.

.. autoclass:: faceid.core.FaceID
   :members:
   :undoc-members:
   :show-inheritance:

Methods
~~~~~~~

.. method:: register_face(image_path, person_id, person_name)

   Register a new face from an image file.

   :param image_path: Path to the image file (string)
   :param person_id: Unique identifier for the person (string)
   :param person_name: Display name for the person (string)
   :raises Exception: If face not found or registration fails
   
   Example:
   
   .. code-block:: python
   
      face_system.register_face("john.jpg", "john_doe", "John Doe")

.. method:: identify_face(image_source)

   Identify faces in an image or video frame.

   :param image_source: Path to image file or numpy array (video frame)
   :return: List of dictionaries containing face information
   :rtype: list
   
   Example:
   
   .. code-block:: python
   
      results = face_system.identify_face("test.jpg")
      for result in results:
          print(result['bbox'], result['matches'])

.. method:: compare_faces(face1_path, face2_path)

   Compare two face images and return similarity score.

   :param face1_path: Path to first face image (string)
   :param face2_path: Path to second face image (string)
   :return: Similarity score between 0 and 1
   :rtype: float
   
   Example:
   
   .. code-block:: python
   
      similarity = face_system.compare_faces("face1.jpg", "face2.jpg")
      if similarity > 0.6:
          print("Faces match!")

Database Management
-------------------

The face database is managed internally. To list registered people:

.. code-block:: python

   people = face_system.database.list_people()
   for person in people:
       print(f"{person['name']} (ID: {person['person_id']})")

Utility Functions
-----------------

.. function:: draw_bbox(image, bbox, label=None, color=(0,255,0))

   Draw bounding box on image.

   :param image: Input image (numpy array)
   :param bbox: Bounding box coordinates [x1,y1,x2,y2]
   :param label: Optional label text
   :param color: Box color as BGR tuple
   :return: Image with drawn box
   :rtype: numpy.ndarray
"@ | Out-File -FilePath api.rst -Encoding UTF8