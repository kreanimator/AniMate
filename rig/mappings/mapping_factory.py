"""
Factory for creating rig mappings.
"""
import bpy
from .base_mappings import BaseRigMapping
from .mixamo_mapping import MixamoMapping
from .rigify_mapping import RigifyMapping
from .maya_mapping import MayaMapping

class RigMappingFactory:
    """Factory for creating rig mappings."""
    
    _mappings = {
        'MIXAMO': MixamoMapping,
        'RIGIFY': RigifyMapping,
        'MAYA': MayaMapping
    }

    @classmethod
    def create_mapping(cls, rig_type: str) -> BaseRigMapping:
        """
        Create a mapping for the specified rig type.
        
        Args:
            rig_type: The type of rig ('MIXAMO', 'RIGIFY', etc.)
            
        Returns:
            A mapping instance for the specified rig type
            
        Raises:
            ValueError: If the rig type is not supported
        """
        if rig_type not in cls._mappings:
            raise ValueError(f"Unsupported rig type: {rig_type}")
        return cls._mappings[rig_type]()
    
    @classmethod
    def get_supported_rigs(cls):
        """Get list of supported rig types."""
        return list(cls._mappings.keys())

    @classmethod
    def get_bone_hierarchy(cls, rig_type):
        """Get the expected bone hierarchy for a rig type."""
        mapping = cls.create_mapping(rig_type)
        return mapping.get_bone_hierarchy()

    @classmethod
    def get_pose_mapping(cls, rig_type):
        """Get the pose mapping for a rig type."""
        mapping = cls.create_mapping(rig_type)
        return mapping.get_pose_mapping()

    @classmethod
    def get_face_mapping(cls, rig_type):
        """Get the face mapping for a rig type."""
        mapping = cls.create_mapping(rig_type)
        return mapping.get_face_mapping()

    @classmethod
    def get_hand_mapping(cls, rig_type):
        """Get the hand mapping for a rig type."""
        mapping = cls.create_mapping(rig_type)
        return mapping.get_hand_mapping() 