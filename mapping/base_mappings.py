"""
Base mapping class for all rig types.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

class BaseRigMapping(ABC):
    """Base class for rig mappings."""
    
    @abstractmethod
    def get_bone_hierarchy(self) -> Dict:
        """Get the expected bone hierarchy for this rig type."""
        pass

    @abstractmethod
    def get_pose_mapping(self) -> Dict[str, List[int]]:
        """Get the mapping between MediaPipe pose landmarks and bone names."""
        pass

    @abstractmethod
    def get_face_mapping(self) -> Dict[str, List[int]]:
        """Get the mapping between MediaPipe face landmarks and bone names."""
        pass

    @abstractmethod
    def get_hand_mapping(self) -> Dict[str, List[int]]:
        """Get the mapping between MediaPipe hand landmarks and bone names."""
        pass

    @abstractmethod
    def get_bone_rotation_limits(self) -> Dict[str, Dict[str, Tuple[float, float]]]:
        """Get rotation limits for each bone."""
        pass

    @abstractmethod
    def get_bone_scale_factors(self) -> Dict[str, float]:
        """Get scale factors for each bone's rotation."""
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, bool]:
        """Get the capabilities of this rig type (face, hands, etc)."""
        pass

    @abstractmethod
    def get_axis_corrections(self):
        """Get axis correction functions for each bone (if any)."""
        pass

    def get_landmark_indices(self, bone_name: str) -> List[int]:
        """Get the MediaPipe landmark indices for a bone."""
        pose_mapping = self.get_pose_mapping()
        if bone_name in pose_mapping:
            return pose_mapping[bone_name]
        return []

    def get_face_landmark_indices(self, bone_name: str) -> List[int]:
        """Get the MediaPipe face landmark indices for a bone."""
        face_mapping = self.get_face_mapping()
        if bone_name in face_mapping:
            return face_mapping[bone_name]
        return []

    def get_hand_landmark_indices(self, bone_name: str) -> List[int]:
        """Get the MediaPipe hand landmark indices for a bone."""
        hand_mapping = self.get_hand_mapping()
        if bone_name in hand_mapping:
            return hand_mapping[bone_name]
        return [] 