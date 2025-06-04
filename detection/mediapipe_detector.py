"""
MediaPipe-based detection for pose, hands, and face tracking.
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, Optional, Any

class MediaPipeDetector:
    """Detector class for MediaPipe pose, hands, and face tracking."""

    def __init__(self, mode: str = 'pose'):
        """
        Initialize the MediaPipe detector.

        Args:
            mode: Detection mode ('pose', 'hands', 'face', or 'holistic')
        """
        self.mode = mode
        self.pose = mp.solutions.pose.Pose() if mode in ['pose', 'holistic'] else None
        self.hands = mp.solutions.hands.Hands() if mode in ['hands', 'holistic'] else None
        self.face = mp.solutions.face_mesh.FaceMesh() if mode in ['face', 'holistic'] else None
        self.cap = None

    def start_camera(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

    def get_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None

    def process_frame(self, frame: np.ndarray) -> Dict[str, Optional[Any]]:
        """
        Process a single frame for pose, hands, and face landmarks.

        Args:
            frame: Input frame as numpy array

        Returns:
            Dictionary containing detected landmarks for pose, hands, and face
        """
        results = {}
        if self.pose:
            pose_results = self.pose.process(frame)
            results['pose'] = pose_results.pose_landmarks if pose_results.pose_landmarks else None
        if self.hands:
            hand_results = self.hands.process(frame)
            if hand_results.multi_hand_landmarks:
                # Assume first is left, second is right if both present
                results['left_hand'] = hand_results.multi_hand_landmarks[0] if len(hand_results.multi_hand_landmarks) > 0 else None
                results['right_hand'] = hand_results.multi_hand_landmarks[1] if len(hand_results.multi_hand_landmarks) > 1 else None
            else:
                results['left_hand'] = None
                results['right_hand'] = None
        if self.face:
            face_results = self.face.process(frame)
            results['face'] = face_results.multi_face_landmarks[0] if face_results.multi_face_landmarks else None
        return results

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None 