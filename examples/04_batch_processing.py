"""
Batch Processing Example
Process multiple images efficiently
"""

from faceid import FaceID
from pathlib import Path
import os

def main():
    print("=" * 50)
    print("Batch Face Processing")
    print("=" * 50)
    
    face_system = FaceID()
    
    while True:
        print("\n" + "-" * 50)
        print("Batch Processing Menu")
        print("-" * 50)
        print("1. Register all faces from directory")
        print("2. Test all images in directory")
        print("3. Compare multiple faces")
        print("4. Export database statistics")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            batch_register(face_system)
        elif choice == "2":
            batch_test(face_system)
        elif choice == "3":
            batch_compare(face_system)
        elif choice == "4":
            export_statistics(face_system)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option")

def batch_register(face_system):
    print("\n" + "-" * 50)
    print("Batch Register Faces")
    print("-" * 50)
    print("\nExpected directory structure:")
    print("  people/")
    print("    person1/")
    print("      image1.jpg")
    print("      image2.jpg")
    print("    person2/")
    print("      image1.jpg\n")
    
    people_dir = input("Enter people directory path: ").strip()
    
    if not os.path.exists(people_dir):
        print(f"✗ Directory not found: {people_dir}")
        return
    
    registered = 0
    failed = 0
    
    # Process each person folder
    for person_folder in os.listdir(people_dir):
        person_path = os.path.join(people_dir, person_folder)
        
        if not os.path.isdir(person_path):
            continue
        
        person_id = person_folder.lower().replace(" ", "_")
        person_name = person_folder
        
        # Process first image found for this person
        for image_file in os.listdir(person_path):
            if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(person_path, image_file)
                
                try:
                    face_system.register_face(image_path, person_id, person_name)
                    print(f"✓ Registered {person_name}")
                    registered += 1
                    break  # Use first image only
                except Exception as e:
                    print(f"✗ Failed to register {person_name}: {e}")
                    failed += 1
                    break
    
    print(f"\nResults: {registered} registered, {failed} failed")

def batch_test(face_system):
    print("\n" + "-" * 50)
    print("Batch Test Images")
    print("-" * 50)
    
    test_dir = input("Enter test images directory: ").strip()
    
    if not os.path.exists(test_dir):
        print(f"✗ Directory not found: {test_dir}")
        return
    
    threshold_str = input("Enter threshold (default 0.6): ").strip()
    try:
        threshold = float(threshold_str) if threshold_str else 0.6
    except:
        threshold = 0.6
    
    results_file = "batch_results.txt"
    
    with open(results_file, 'w') as f:
        f.write("Batch Test Results\n")
        f.write("=" * 50 + "\n\n")
        
        image_count = 0
        match_count = 0
        
        # Process all images
        for image_file in sorted(os.listdir(test_dir)):
            if not image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            
            image_path = os.path.join(test_dir, image_file)
            image_count += 1
            
            try:
                results = face_system.identify_face(image_path, threshold=threshold)
                
                f.write(f"Image: {image_file}\n")
                
                if results:
                    f.write(f"  Faces found: {len(results)}\n")
                    
                    for i, result in enumerate(results):
                        f.write(f"  Face {i+1}:\n")
                        f.write(f"    Confidence: {result['confidence']:.2%}\n")
                        
                        if result['matches']:
                            match_count += 1
                            f.write(f"    Best match: {result['matches'][0]['name']} ")
                            f.write(f"({result['matches'][0]['similarity']:.2%})\n")
                        else:
                            f.write(f"    No matches\n")
                else:
                    f.write(f"  No faces detected\n")
                
                f.write("\n")
                print(f"✓ Processed {image_file}")
                
            except Exception as e:
                f.write(f"Image: {image_file}\n")
                f.write(f"  Error: {e}\n\n")
                print(f"✗ Error processing {image_file}: {e}")
        
        f.write("-" * 50 + "\n")
        f.write(f"Total images: {image_count}\n")
        f.write(f"Matches found: {match_count}\n")
    
    print(f"\n✓ Results saved to {results_file}")

def batch_compare(face_system):
    print("\n" + "-" * 50)
    print("Batch Compare Faces")
    print("-" * 50)
    
    image_dir = input("Enter directory with images to compare: ").strip()
    
    if not os.path.exists(image_dir):
        print(f"✗ Directory not found")
        return
    
    # Get all images
    images = [f for f in os.listdir(image_dir) 
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if len(images) < 2:
        print("Need at least 2 images to compare")
        return
    
    results_file = "comparison_results.txt"
    
    with open(results_file, 'w') as f:
        f.write("Face Comparison Results\n")
        f.write("=" * 50 + "\n\n")
        
        # Compare all pairs
        for i in range(len(images)):
            for j in range(i + 1, len(images)):
                image1_path = os.path.join(image_dir, images[i])
                image2_path = os.path.join(image_dir, images[j])
                
                try:
                    similarity = face_system.compare_faces(image1_path, image2_path)
                    match = "MATCH" if similarity >= 0.6 else "DIFFERENT"
                    
                    f.write(f"{images[i]} vs {images[j]}\n")
                    f.write(f"  Similarity: {similarity:.2%} [{match}]\n\n")
                    
                    print(f"✓ {images[i]} vs {images[j]}: {similarity:.2%}")
                except Exception as e:
                    f.write(f"{images[i]} vs {images[j]}\n")
                    f.write(f"  Error: {e}\n\n")
                    print(f"✗ Error comparing {images[i]} and {images[j]}")
    
    print(f"\n✓ Results saved to {results_file}")

def export_statistics(face_system):
    print("\n" + "-" * 50)
    print("Database Statistics")
    print("-" * 50)
    
    stats_file = "database_stats.txt"
    
    with open(stats_file, 'w') as f:
        f.write("FaceID Database Statistics\n")
        f.write("=" * 50 + "\n\n")
        
        people = face_system.database.list_people()
        
        f.write(f"Total people: {len(people)}\n\n")
        
        if people:
            f.write("People:\n")
            f.write("-" * 50 + "\n")
            
            for person in sorted(people, key=lambda x: x['name']):
                f.write(f"ID: {person['person_id']}\n")
                f.write(f"Name: {person['name']}\n")
                
                if person['metadata']:
                    f.write(f"Metadata:\n")
                    for key, value in person['metadata'].items():
                        f.write(f"  {key}: {value}\n")
                
                f.write("\n")
    
    print(f"✓ Statistics saved to {stats_file}")
    
    print(f"\nDatabase Summary:")
    print(f"  Total people: {len(face_system.database)}")

if __name__ == "__main__":
    main()
