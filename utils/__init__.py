__author__ = "Valentin Bakin"

"""
Utility functions for AniMate.
Contains detection, processing, and helper functions.
"""

from .detection import (
    MediaPipeDetector,
    process_camera_feed,
    DetectionResults
)

__all__ = [
    'MediaPipeDetector',
    'process_camera_feed',
    'DetectionResults'
]
