"""
Real-time Camera Recognition Example
Use your webcam for live face recognition
"""

import cv2
from faceid import FaceID

def main():
    print("=" * 50)
    print("Real-time Camera Recognition")
    print("=" * 50)
    print("\nInitializing...")
    
    # Initialize FaceID
    try:
        face_system = FaceID()
        print("✓ FaceID initialized")
    except Exception as e:
        print(f"✗ Error initializing FaceID: {e}")
        return
    
    # Try to load existing database
    db_path = "face_database.pkl"
    try:
        face_system.database.load(db_path)
        print(f"✓ Loaded database from {db_path}")
        print(f"  Registered people: {len(face_system.database)}")
    except Exception as e:
        print(f"⚠ No existing database found")
    
    print("\nStarting camera...")
    print("Press 'q' to quit")
    print("Press 's' to save frame")
    
    # Open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("✗ Could not open camera")
        return
    
    frame_count = 0
    process_interval = 3  # Process every 3 frames for performance
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("✗ Error reading frame")
                break
            
            frame_count += 1
            
            # Process every N frames
            if frame_count % process_interval == 0:
                try:
                    # Identify faces
                    results = face_system.identify_face(frame)
                    
                    # Draw results
                    for result in results:
                        x1, y1, x2, y2 = result['bbox']
                        confidence = result['confidence']
                        
                        if result['matches']:
                            # Found a match
                            best_match = result['matches'][0]
                            name = best_match['name']
                            similarity = best_match['similarity']
                            color = (0, 255, 0)  # Green
                            label = f"{name} ({similarity:.0%})"
                        else:
                            # No match
                            name = "Unknown"
                            color = (0, 0, 255)  # Red
                            label = "Unknown"
                        
                        # Draw bounding box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        
                        # Draw label background
                        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 
                                                     0.6, 2)[0]
                        cv2.rectangle(frame, (x1, y1-25), 
                                     (x1 + label_size[0] + 5, y1), color, -1)
                        
                        # Draw label text
                        cv2.putText(frame, label, (x1 + 2, y1 - 7),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                                   (255, 255, 255), 2)
                
                except Exception as e:
                    print(f"Error processing frame: {e}")
            
            # Add info text
            info_text = f"Faces: {len(frame_count)} | DB: {len(face_system.database)}"
            cv2.putText(frame, info_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, "Press 'q' to quit | 's' to save",
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                       (255, 255, 255), 1)
            
            # Display frame
            cv2.imshow('FaceID - Real-time Recognition', frame)
            
            # Handle key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('s'):
                filename = f"capture_{frame_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"\n✓ Saved frame to {filename}")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("✓ Camera closed")
        
        # Optionally save database
        try:
            response = input("Save database? (y/n): ").lower()
            if response == 'y':
                face_system.database.save(db_path)
                print(f"✓ Database saved to {db_path}")
        except:
            pass

if __name__ == "__main__":
    main()
