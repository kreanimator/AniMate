"""
Example script demonstrating how to use AniMate for live motion capture.
"""

import bpy
import sys
import os
import cv2

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.detection import MediaPipeDetector, create_camera
from rig.blender_mapper import BlenderRigMapper

def setup_blender_scene():
    """Set up the Blender scene for motion capture."""
    # Get the active armature
    armature = bpy.context.active_object
    if not armature or armature.type != 'ARMATURE':
        raise ValueError("Please select an armature object")
    
    # Create the rig mapper
    rig_mapper = BlenderRigMapper(armature)
    
    return rig_mapper

def main():
    """Main function for live motion capture."""
    # Initialize MediaPipe detector
    detector = MediaPipeDetector(
        enable_pose=True,
        enable_face=True,
        enable_hands=True
    )
    
    # Initialize camera
    cap = create_camera()
    
    # Set up Blender scene
    rig_mapper = setup_blender_scene()
    
    # Detection status
    detection_status = {
        'pose': True,
        'face': True,
        'hands': True
    }
    
    try:
        while True:
            # Read frame from camera
            success, frame = cap.read()
            if not success:
                print("Failed to read from camera")
                break
            
            # Process frame with MediaPipe
            frame, results = detector.process_frame(frame, draw_landmarks=True)
            
            # Update Blender rig based on enabled detections
            if detection_status['pose'] and results.pose_landmarks:
                rig_mapper.process_pose_landmarks(results.pose_landmarks)
            
            if detection_status['face'] and results.face_landmarks:
                rig_mapper.process_face_landmarks(results.face_landmarks[0])
            
            if detection_status['hands']:
                if results.left_hand_landmarks:
                    rig_mapper.process_hand_landmarks(results.left_hand_landmarks, is_right_hand=False)
                if results.right_hand_landmarks:
                    rig_mapper.process_hand_landmarks(results.right_hand_landmarks, is_right_hand=True)
            
            # Update Blender viewport
            bpy.context.view_layer.update()
            
            # Display detection status
            y_offset = 60
            for det_type, is_enabled in detection_status.items():
                status = "ON" if is_enabled else "OFF"
                color = (0, 255, 0) if is_enabled else (0, 0, 255)
                cv2.putText(frame, f"{det_type}: {status}", (10, y_offset),
                           cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
                y_offset += 30
            
            # Display frame
            cv2.imshow('AniMate Capture', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('p'):  # Toggle pose detection
                detection_status['pose'] = not detection_status['pose']
                detector.pose = detector.mp_pose.Pose(
                    static_image_mode=False,
                    model_complexity=1,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                ) if detection_status['pose'] else None
            elif key == ord('f'):  # Toggle face detection
                detection_status['face'] = not detection_status['face']
                detector.face_mesh = detector.mp_face.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                ) if detection_status['face'] else None
            elif key == ord('h'):  # Toggle hand detection
                detection_status['hands'] = not detection_status['hands']
                detector.hands = detector.mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=2,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                ) if detection_status['hands'] else None
                
    finally:
        # Clean up
        cap.release()
        detector.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 