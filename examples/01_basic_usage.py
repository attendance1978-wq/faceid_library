"""
Basic FaceID Usage Example
Run this to see the library in action with simple examples
"""

from faceid import FaceID
import os

def main():
    # Initialize FaceID
    print("Initializing FaceID...")
    face_system = FaceID()
    print("✓ FaceID initialized\n")
    
    # Example 1: Register faces (assuming you have sample images)
    print("=" * 50)
    print("Example 1: Register Faces")
    print("=" * 50)
    
    sample_images = {
        "person_001": "alice.jpg",
        "person_002": "bob.jpg",
    }
    
    for person_id, image_path in sample_images.items():
        if os.path.exists(image_path):
            try:
                name = person_id.replace("_", " ").title()
                face_system.register_face(image_path, person_id, name)
                print(f"✓ Registered {name}")
            except Exception as e:
                print(f"✗ Failed to register {person_id}: {e}")
        else:
            print(f"⚠ Image not found: {image_path}")
    
    # Example 2: List registered people
    print("\n" + "=" * 50)
    print("Example 2: List Registered People")
    print("=" * 50)
    
    people = face_system.database.list_people()
    if people:
        for person in people:
            print(f"  • {person['name']} (ID: {person['person_id']})")
    else:
        print("  No people registered yet")
    
    # Example 3: Test identification on sample image
    print("\n" + "=" * 50)
    print("Example 3: Identify Faces")
    print("=" * 50)
    
    test_image = "test.jpg"
    if os.path.exists(test_image):
        try:
            results = face_system.identify_face(test_image)
            print(f"Found {len(results)} face(s):\n")
            
            for i, result in enumerate(results):
                print(f"Face {i+1}:")
                print(f"  Detection confidence: {result['confidence']:.2%}")
                
                if result['matches']:
                    print(f"  Matches:")
                    for match in result['matches']:
                        print(f"    - {match['name']}: {match['similarity']:.2%}")
                else:
                    print(f"  No matches found")
                print()
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print(f"⚠ Test image not found: {test_image}")
    
    # Example 4: Compare two faces
    print("=" * 50)
    print("Example 4: Compare Two Faces")
    print("=" * 50)
    
    face1 = "person1.jpg"
    face2 = "person2.jpg"
    
    if os.path.exists(face1) and os.path.exists(face2):
        try:
            similarity = face_system.compare_faces(face1, face2)
            match = "MATCH" if similarity >= 0.6 else "DIFFERENT"
            print(f"Similarity: {similarity:.2%} [{match}]")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print(f"⚠ One or both face images not found")
    
    # Example 5: Save database
    print("\n" + "=" * 50)
    print("Example 5: Save Database")
    print("=" * 50)
    
    db_path = "face_database.pkl"
    if len(face_system.database) > 0:
        face_system.database.save(db_path)
        print(f"✓ Database saved to {db_path}")
    else:
        print("Database is empty, nothing to save")
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
