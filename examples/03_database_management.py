"""
Database Management Example
Learn how to manage the face database
"""

from faceid import FaceID
import os

def main():
    print("=" * 50)
    print("Face Database Management")
    print("=" * 50)
    
    # Initialize FaceID
    face_system = FaceID()
    db_path = "my_faces.db"
    
    while True:
        print("\n" + "-" * 50)
        print("Database Menu")
        print("-" * 50)
        print("1. Add person from image")
        print("2. List all people")
        print("3. Find matches for face")
        print("4. Verify face")
        print("5. Get person info")
        print("6. Delete person")
        print("7. Save database")
        print("8. Load database")
        print("9. Clear database")
        print("10. Exit")
        
        choice = input("\nSelect option (1-10): ").strip()
        
        if choice == "1":
            add_person(face_system)
        elif choice == "2":
            list_people(face_system)
        elif choice == "3":
            find_matches(face_system)
        elif choice == "4":
            verify_face(face_system)
        elif choice == "5":
            get_person_info(face_system)
        elif choice == "6":
            delete_person(face_system)
        elif choice == "7":
            save_database(face_system, db_path)
        elif choice == "8":
            load_database(face_system, db_path)
        elif choice == "9":
            clear_database(face_system)
        elif choice == "10":
            print("\nGoodbye!")
            break
        else:
            print("Invalid option")

def add_person(face_system):
    print("\n" + "-" * 50)
    print("Add Person")
    print("-" * 50)
    
    person_id = input("Enter person ID: ").strip().lower().replace(" ", "_")
    person_name = input("Enter person name: ").strip()
    image_path = input("Enter image path: ").strip()
    
    if not os.path.exists(image_path):
        print(f"✗ Image not found: {image_path}")
        return
    
    try:
        # Optional metadata
        dept = input("Enter department (optional): ").strip()
        metadata = {"dept": dept} if dept else {}
        
        face_system.register_face(image_path, person_id, person_name, metadata)
        print(f"✓ Successfully added {person_name}")
    except Exception as e:
        print(f"✗ Error: {e}")

def list_people(face_system):
    print("\n" + "-" * 50)
    print("Registered People")
    print("-" * 50)
    
    people = face_system.database.list_people()
    
    if not people:
        print("No people registered")
        return
    
    print(f"\nTotal: {len(people)}\n")
    for person in people:
        print(f"ID: {person['person_id']}")
        print(f"  Name: {person['name']}")
        if person['metadata']:
            print(f"  Metadata: {person['metadata']}")
        print()

def find_matches(face_system):
    print("\n" + "-" * 50)
    print("Find Matches")
    print("-" * 50)
    
    image_path = input("Enter test image path: ").strip()
    
    if not os.path.exists(image_path):
        print(f"✗ Image not found")
        return
    
    threshold = input("Enter threshold (0-1, default 0.6): ").strip()
    try:
        threshold = float(threshold) if threshold else 0.6
    except:
        threshold = 0.6
    
    try:
        results = face_system.identify_face(image_path, threshold=threshold)
        
        if not results:
            print("No faces detected")
            return
        
        print(f"\n✓ Found {len(results)} face(s)\n")
        
        for i, result in enumerate(results):
            print(f"Face {i+1}:")
            print(f"  Confidence: {result['confidence']:.2%}")
            
            if result['matches']:
                print(f"  Matches:")
                for match in result['matches']:
                    print(f"    • {match['name']}: {match['similarity']:.2%}")
            else:
                print(f"  No matches found")
            print()
    except Exception as e:
        print(f"✗ Error: {e}")

def verify_face(face_system):
    print("\n" + "-" * 50)
    print("Verify Face")
    print("-" * 50)
    
    # List available people
    people = face_system.database.list_people()
    if not people:
        print("No people in database")
        return
    
    print("Available people:")
    for person in people:
        print(f"  • {person['person_id']}: {person['name']}")
    
    person_id = input("\nEnter person ID to verify against: ").strip()
    image_path = input("Enter face image: ").strip()
    
    if not os.path.exists(image_path):
        print(f"✗ Image not found")
        return
    
    try:
        is_match, similarity = face_system.verify_face(image_path, person_id)
        
        person = face_system.database.get_person(person_id)
        if is_match:
            print(f"\n✓ VERIFIED: Face matches {person['name']}")
        else:
            print(f"\n✗ NOT VERIFIED: Face does not match {person['name']}")
        
        print(f"Similarity: {similarity:.2%}")
    except Exception as e:
        print(f"✗ Error: {e}")

def get_person_info(face_system):
    print("\n" + "-" * 50)
    print("Get Person Info")
    print("-" * 50)
    
    person_id = input("Enter person ID: ").strip()
    
    person = face_system.database.get_person(person_id)
    if person:
        print(f"\nPerson ID: {person_id}")
        print(f"Name: {person['name']}")
        print(f"Metadata: {person['metadata']}")
    else:
        print(f"✗ Person not found: {person_id}")

def delete_person(face_system):
    print("\n" + "-" * 50)
    print("Delete Person")
    print("-" * 50)
    
    person_id = input("Enter person ID to delete: ").strip()
    
    person = face_system.database.get_person(person_id)
    if not person:
        print(f"✗ Person not found: {person_id}")
        return
    
    confirm = input(f"Delete {person['name']}? (yes/no): ").strip().lower()
    if confirm == "yes":
        face_system.database.delete_person(person_id)
        print(f"✓ Deleted {person['name']}")
    else:
        print("Cancelled")

def save_database(face_system, db_path):
    print("\n" + "-" * 50)
    print("Save Database")
    print("-" * 50)
    
    if len(face_system.database) == 0:
        print("Database is empty")
        return
    
    path = input(f"Enter save path (default: {db_path}): ").strip()
    path = path or db_path
    
    try:
        face_system.database.save(path)
        print(f"✓ Database saved to {path}")
    except Exception as e:
        print(f"✗ Error: {e}")

def load_database(face_system, db_path):
    print("\n" + "-" * 50)
    print("Load Database")
    print("-" * 50)
    
    path = input(f"Enter database path (default: {db_path}): ").strip()
    path = path or db_path
    
    try:
        face_system.database.load(path)
        print(f"✓ Loaded database from {path}")
        print(f"  People: {len(face_system.database)}")
    except Exception as e:
        print(f"✗ Error: {e}")

def clear_database(face_system):
    print("\n" + "-" * 50)
    print("Clear Database")
    print("-" * 50)
    
    if len(face_system.database) == 0:
        print("Database is already empty")
        return
    
    confirm = input(f"Clear all {len(face_system.database)} entries? (yes/no): ").strip().lower()
    if confirm == "yes":
        face_system.database.clear()
        print("✓ Database cleared")
    else:
        print("Cancelled")

if __name__ == "__main__":
    main()
