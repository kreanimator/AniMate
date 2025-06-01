__author__ = "Valentin Bakin"

"""
Data package for AniMate.
Contains configurations, test rigs, and landmark definitions.
"""

from .landmark_structure import (
    POSE_LANDMARKS,
    FACE_LANDMARKS,
    HAND_LANDMARKS,
    LANDMARK_CONNECTIONS
)

from .test_rigs import (
    BASIC_HUMANOID,
    FACE_RIG,
    HAND_RIG
)

from .bone_mappings import (
    POSE_LANDMARKS_TO_BONES,
    FACE_LANDMARKS_TO_BONES,
    HAND_LANDMARKS_TO_BONES
)

__all__ = [
    'POSE_LANDMARKS',
    'FACE_LANDMARKS',
    'HAND_LANDMARKS',
    'LANDMARK_CONNECTIONS',
    'BASIC_HUMANOID',
    'FACE_RIG',
    'HAND_RIG',
    'POSE_LANDMARKS_TO_BONES',
    'FACE_LANDMARKS_TO_BONES',
    'HAND_LANDMARKS_TO_BONES'
]