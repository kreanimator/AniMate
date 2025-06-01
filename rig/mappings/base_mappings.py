"""
Base mapping class for all rig types.
"""
from abc import ABC, abstractmethod

class BaseRigMapping(ABC):
    """Base class for all rig mappings."""
    
    @abstractmethod
    def get_pose_mapping(self):
        """Get the pose landmark to bone mapping."""
        pass
    
    @abstractmethod
    def get_hand_mapping(self):
        """Get the hand landmark to bone mapping."""
        pass
    
    @abstractmethod
    def get_face_mapping(self):
        """Get the face landmark to bone mapping."""
        pass
    
    @abstractmethod
    def get_bone_hierarchy(self):
        """Get the bone hierarchy for this rig type."""
        pass
    
    @abstractmethod
    def get_bone_rotation_limits(self):
        """Get the rotation limits for each bone."""
        pass
    
    @abstractmethod
    def get_bone_scale_factors(self):
        """Get the scale factors for each bone."""
        pass 