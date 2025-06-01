"""
Test script for MediaPipe detection functionality.
This script tests the detection capabilities without involving Blender.
"""

import cv2
import time
from utils.detection import MediaPipeDetector

def test_detection():
    """Test the detection functionality with webcam feed."""
    print("Initializing MediaPipe detector...")
    detector = MediaPipeDetector()
    
    print("Opening webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("\nControls:")
    print("  'p' - Toggle pose detection")
    print("  'f' - Toggle face detection")
    print("  'h' - Toggle hand detection")
    print("  'ESC' - Exit")
    
    # Initialize detection status
    detection_status = {
        'pose': True,
        'face': True,
        'hands': True
    }
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
                
            # Process frame
            results = detector.process_frame(frame)
            
            # Draw landmarks based on enabled detections
            if detection_status['pose'] and results.pose_landmarks:
                detector.draw_landmarks(frame, results.pose_landmarks, detector.mp_pose.POSE_CONNECTIONS, 'pose')
            
            if detection_status['face'] and results.face_landmarks:
                detector.draw_landmarks(frame, results.face_landmarks, detector.mp_face_mesh.FACEMESH_TESSELATION, 'face')
            
            if detection_status['hands']:
                if results.left_hand_landmarks:
                    detector.draw_landmarks(frame, results.left_hand_landmarks, detector.mp_hands.HAND_CONNECTIONS, 'hand')
                if results.right_hand_landmarks:
                    detector.draw_landmarks(frame, results.right_hand_landmarks, detector.mp_hands.HAND_CONNECTIONS, 'hand')
            
            # Display detection status
            y_offset = 30
            for detection_type, is_enabled in detection_status.items():
                status = "ON" if is_enabled else "OFF"
                color = (0, 255, 0) if is_enabled else (0, 0, 255)
                cv2.putText(frame, f"{detection_type}: {status}", (10, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                y_offset += 30
            
            # Show frame
            cv2.imshow('MediaPipe Detection Test', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('p'):
                detection_status['pose'] = not detection_status['pose']
            elif key == ord('f'):
                detection_status['face'] = not detection_status['face']
            elif key == ord('h'):
                detection_status['hands'] = not detection_status['hands']
            
            # Add small delay to prevent high CPU usage
            time.sleep(0.01)
            
    finally:
        print("\nCleaning up...")
        cap.release()
        cv2.destroyAllWindows()
        detector.close()

if __name__ == "__main__":
    test_detection() 