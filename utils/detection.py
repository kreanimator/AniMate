"""
MediaPipe detection module for AniMate.
Handles pose, face, and hand detection using MediaPipe.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass

@dataclass
class DetectionResults:
    """Container for detection results from MediaPipe."""
    pose_landmarks: Optional[Any] = None
    face_landmarks: Optional[Any] = None
    left_hand_landmarks: Optional[Any] = None
    right_hand_landmarks: Optional[Any] = None

class MediaPipeDetector:
    """MediaPipe detector for pose, face, and hand tracking."""
    
    def __init__(self):
        """Initialize MediaPipe solutions and drawing utilities."""
        # Initialize MediaPipe solutions
        self.mp_pose = mp.solutions.pose
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize pose detector
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize face mesh detector
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize hand detector
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def process_frame(self, frame: np.ndarray) -> DetectionResults:
        """Process a single frame for pose, face, and hand detection."""
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process pose
        pose_results = self.pose.process(rgb_frame)
        
        # Process face
        face_results = self.face_mesh.process(rgb_frame)
        
        # Process hands
        hands_results = self.hands.process(rgb_frame)
        
        return DetectionResults(
            pose_landmarks=pose_results.pose_landmarks,
            face_landmarks=face_results.multi_face_landmarks[0] if face_results.multi_face_landmarks else None,
            left_hand_landmarks=hands_results.multi_hand_landmarks[0] if hands_results.multi_hand_landmarks and len(hands_results.multi_hand_landmarks) > 0 else None,
            right_hand_landmarks=hands_results.multi_hand_landmarks[1] if hands_results.multi_hand_landmarks and len(hands_results.multi_hand_landmarks) > 1 else None
        )
    
    def draw_landmarks(self, frame: np.ndarray, landmarks: Any, connections: Any, landmark_type: str = 'pose') -> None:
        """
        Draw landmarks and connections on the frame.
        
        Args:
            frame: Frame to draw on
            landmarks: Landmarks to draw
            connections: Connections between landmarks
            landmark_type: Type of landmarks ('pose', 'face', or 'hand')
        """
        if landmark_type == 'pose':
            self.mp_drawing.draw_landmarks(
                frame,
                landmarks,
                connections,
                self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        elif landmark_type == 'face':
            self.mp_drawing.draw_landmarks(
                frame,
                landmarks,
                connections,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
        elif landmark_type == 'hand':
            self.mp_drawing.draw_landmarks(
                frame,
                landmarks,
                connections,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style()
            )
    
    def close(self) -> None:
        """Clean up MediaPipe resources."""
        self.pose.close()
        self.face_mesh.close()
        self.hands.close()

def create_camera(camera_id: int = 0, width: int = 1280, height: int = 720) -> cv2.VideoCapture:
    """
    Create and configure a camera capture object.
    
    Args:
        camera_id: Camera device ID
        width: Frame width
        height: Frame height
        
    Returns:
        Configured VideoCapture object
    """
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

def process_camera_feed(
    cap: cv2.VideoCapture,
    detector: MediaPipeDetector,
    detection_status: Dict[str, bool]
) -> None:
    """Process camera feed with detection and visualization."""
    while True:
        ret, frame = cap.read()
        if not ret:
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
        
        # Show frame
        cv2.imshow('MediaPipe Detection', frame)
        
        # Break on ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break

if __name__ == "__main__":
    detector = MediaPipeDetector()
    cap = create_camera()
    
    try:
        process_camera_feed(cap, detector, {
            'pose': True,
            'face': True,
            'hands': True
        })
    finally:
        cap.release()
        detector.close()
        cv2.destroyAllWindows() 