"""
FaceID Demo Script - Fixed Recognition
"""

import cv2
from faceid import FaceID
import sys
import os
import numpy as np

def run_demo():
    """Run the FaceID demo"""
    print("=" * 50)
    print("FaceID - Advanced Face Recognition Library")
    print("=" * 50)
    
    # Initialize
    print("\nInitializing FaceID system...")
    try:
        face_system = FaceID()
        print("✓ System initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return
    
    print("\n" + "=" * 50)
    print("MENU")
    print("=" * 50)
    print("1. Register faces from image files")
    print("2. Test recognition on image file")
    print("3. Real-time camera recognition")
    print("4. Compare two faces")
    print("5. List registered people")
    print("6. Exit")
    
    while True:
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            register_faces_demo(face_system)
        elif choice == "2":
            test_image_recognition(face_system)
        elif choice == "3":
            real_time_recognition(face_system)
        elif choice == "4":
            compare_faces_demo(face_system)
        elif choice == "5":
            list_people_demo(face_system)
        elif choice == "6":
            print("\nThank you for using FaceID!")
            break
        else:
            print("Invalid option. Please try again.")

def register_faces_demo(face_system):
    """Register faces from images"""
    print("\n" + "-" * 50)
    print("REGISTER FACES")
    print("-" * 50)
    print("\n⚠️  For best results, use a clear front-facing photo")
    print("   Make sure the face is well-lit and looking at camera\n")
    
    while True:
        person_name = input("\nEnter person name (or 'done' to finish): ").strip()
        if person_name.lower() == 'done':
            break
        
        image_path = input(f"Enter image path for {person_name}: ").strip()
        
        # Remove quotes if present
        image_path = image_path.strip('"').strip("'")
        
        if not os.path.exists(image_path):
            print(f"✗ File not found: {image_path}")
            print(f"   Current directory: {os.getcwd()}")
            print(f"   Files here: {[f for f in os.listdir('.') if f.endswith(('.jpg', '.png', '.jpeg'))]}")
            continue
        
        try:
            # Register the face
            face_system.register_face(image_path, person_name.lower(), person_name)
            print(f"✓ Successfully registered {person_name}")
            
            # Verify registration
            people = face_system.database.list_people()
            print(f"   Total registered: {len(people)}")
            
        except Exception as e:
            print(f"✗ Failed to register {person_name}: {e}")

def test_image_recognition(face_system):
    """Test recognition on an image file"""
    print("\n" + "-" * 50)
    print("IMAGE RECOGNITION TEST")
    print("-" * 50)
    
    image_path = input("\nEnter image path to analyze: ").strip()
    image_path = image_path.strip('"').strip("'")
    
    if not os.path.exists(image_path):
        print(f"✗ File not found: {image_path}")
        return
    
    try:
        print("Analyzing image...")
        results = face_system.identify_face(image_path)
        
        if not results:
            print("✗ No faces detected")
            return
        
        print(f"\n✓ Found {len(results)} face(s)")
        
        for i, result in enumerate(results):
            print(f"\n{'='*40}")
            print(f"Face {i+1}:")
            print(f"  Detection confidence: {result['confidence']:.2%}")
            
            if result['matches']:
                print(f"  ✓ RECOGNIZED!")
                for match in result['matches']:
                    print(f"    - Name: {match['name']}")
                    print(f"    - Similarity: {match['similarity']:.2%}")
                    if match['similarity'] >= 0.6:
                        print(f"    - Status: MATCH ✓")
                    else:
                        print(f"    - Status: LOW CONFIDENCE ⚠️")
            else:
                print(f"  ✗ NOT RECOGNIZED")
                print(f"    No matching faces in database")
                
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

def real_time_recognition(face_system):
    """Real-time recognition using webcam - FIXED VERSION"""
    print("\n" + "-" * 50)
    print("REAL-TIME CAMERA RECOGNITION")
    print("-" * 50)
    
    # Check if any faces are registered
    people = face_system.database.list_people()
    if not people:
        print("\n⚠️  No faces registered yet!")
        print("   Please register faces first using option 1")
        print("   Returning to main menu...")
        return
    
    print(f"\n✓ {len(people)} face(s) registered: {[p['name'] for p in people]}")
    print("\nControls:")
    print("  'q' - Quit")
    print("  's' - Save current frame")
    print("  'd' - Debug info")
    print("\nStarting camera...\n")
    
    # Try different camera indices
    cap = None
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"✓ Camera opened successfully (index: {i})")
            break
        else:
            cap.release()
    
    if not cap or not cap.isOpened():
        print("✗ Could not open camera. Please check your webcam.")
        return
    
    frame_count = 0
    process_every_n_frames = 1  # Process every frame for better recognition
    recognition_threshold = 0.6  # Minimum similarity for recognition
    
    # Create a window
    window_name = 'FaceID - Real-time Recognition'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1024, 768)
    
    print("\n✅ Camera ready! Looking for faces...\n")
    print("=" * 50)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame")
            break
        
        frame_count += 1
        display_frame = frame.copy()
        h, w = display_frame.shape[:2]
        
        # Process frames
        if frame_count % process_every_n_frames == 0:
            try:
                # Detect and recognize faces
                results = face_system.identify_face(frame)
                
                if results:
                    for result in results:
                        # Get bounding box
                        bbox = result['bbox']
                        x1, y1, x2, y2 = [int(coord) for coord in bbox]
                        
                        # Ensure coordinates are within frame
                        x1 = max(0, x1)
                        y1 = max(0, y1)
                        x2 = min(w, x2)
                        y2 = min(h, y2)
                        
                        # Check for matches
                        if result['matches'] and len(result['matches']) > 0:
                            best_match = result['matches'][0]
                            name = best_match['name']
                            similarity = best_match['similarity']
                            
                            # Determine if recognized
                            if similarity >= recognition_threshold:
                                # Recognized face
                                label = f"{name} ({similarity:.1%})"
                                color = (0, 255, 0)  # Green
                                status = "RECOGNIZED ✓"
                            else:
                                # Low confidence
                                label = f"{name}? ({similarity:.1%})"
                                color = (0, 255, 255)  # Yellow
                                status = "LOW CONFIDENCE ⚠️"
                        else:
                            # Unknown face
                            label = "Unknown"
                            color = (0, 0, 255)  # Red
                            status = "UNKNOWN ✗"
                        
                        # Draw bounding box
                        cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                        
                        # Draw label background
                        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                        cv2.rectangle(display_frame, 
                                    (x1, y1 - 35), 
                                    (x1 + label_size[0] + 10, y1), 
                                    color, -1)
                        
                        # Draw label text
                        cv2.putText(display_frame, label, 
                                  (x1 + 5, y1 - 10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        
                        # Draw detection confidence
                        if 'confidence' in result:
                            conf_text = f"detection: {result['confidence']:.0%}"
                            cv2.putText(display_frame, conf_text, 
                                      (x1, y2 + 20),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                    
                    # Show summary
                    recognized = sum(1 for r in results if r['matches'] and r['matches'][0]['similarity'] >= recognition_threshold)
                    cv2.putText(display_frame, f"Faces: {len(results)} | Recognized: {recognized}", 
                              (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                else:
                    cv2.putText(display_frame, "No faces detected", 
                              (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    
            except Exception as e:
                print(f"Error in recognition: {e}")
                cv2.putText(display_frame, f"Error: {str(e)[:30]}", 
                          (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Draw instructions
        instructions = [
            "FaceID - Real-time Recognition",
            "Press 'q' to quit | 's' to save | 'd' for debug"
        ]
        
        for i, instruction in enumerate(instructions):
            color = (255, 255, 0) if i == 0 else (200, 200, 200)
            cv2.putText(display_frame, instruction, (10, 30 + i*25), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Show registered people count
        cv2.putText(display_frame, f"Registered: {len(people)}", 
                  (w - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show frame
        cv2.imshow(window_name, display_frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\nQuitting...")
            break
        elif key == ord('s'):
            # Save current frame
            filename = f"capture_{frame_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✓ Saved: {filename}")
        elif key == ord('d'):
            # Debug info
            print("\n" + "=" * 40)
            print("DEBUG INFORMATION:")
            print(f"  Registered people: {len(people)}")
            for p in people:
                print(f"    - {p['name']} (ID: {p['person_id']})")
            print(f"  Recognition threshold: {recognition_threshold}")
            print(f"  Frame count: {frame_count}")
            print("=" * 40 + "\n")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nCamera released and windows closed")

def compare_faces_demo(face_system):
    """Compare two faces"""
    print("\n" + "-" * 50)
    print("COMPARE FACES")
    print("-" * 50)
    
    face1_path = input("\nEnter path to first face image: ").strip()
    face2_path = input("Enter path to second face image: ").strip()
    
    face1_path = face1_path.strip('"').strip("'")
    face2_path = face2_path.strip('"').strip("'")
    
    if not os.path.exists(face1_path) or not os.path.exists(face2_path):
        print("✗ One or both files not found")
        return
    
    try:
        print("Comparing faces...")
        similarity = face_system.compare_faces(face1_path, face2_path)
        
        if similarity >= 0.6:
            print(f"\n✓ MATCH! Similarity: {similarity:.2%}")
        else:
            print(f"\n✗ NO MATCH. Similarity: {similarity:.2%}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

def list_people_demo(face_system):
    """List all registered people"""
    print("\n" + "-" * 50)
    print("REGISTERED PEOPLE")
    print("-" * 50)
    
    people = face_system.database.list_people()
    
    if not people:
        print("\n❌ No people registered yet.")
        print("   Use option 1 to register faces.")
        return
    
    print(f"\n✅ Total registered: {len(people)}\n")
    for i, person in enumerate(people, 1):
        print(f"  {i}. {person['name']} (ID: {person['person_id']})")

if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()