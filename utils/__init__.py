__author__ = "Valentin Bakin"

"""
Utility package for helper functions and modules.
Contains:
- pose_detection: Functions for pose detection and landmark capture
- face_detection: Functions for face detection and landmark capture
- hand_detection: Functions for hand detection and landmark capture

"""

from .pose_detection import PoseDetector
from .face_detection import FaceMeshDetector
from .hands_detection import HandDetector


__all__ = ["PoseDetector", "FaceMeshDetector", "HandDetector"]
