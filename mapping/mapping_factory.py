"""
Factory for creating rig mappings.
"""
from .mixamo_mapping import MixamoMapping
from .rigify_mapping import RigifyMapping
from .maya_mapping import MayaMapping
from .base_mappings import BaseRigMapping

class RigMappingFactory:
    _mappings = {
        'MIXAMO': MixamoMapping,
        'RIGIFY': RigifyMapping,
        'MAYA': MayaMapping
    }

    @classmethod
    def create_mapping(cls, rig_type: str) -> BaseRigMapping:
        if rig_type not in cls._mappings:
            raise ValueError(f"Unsupported rig type: {rig_type}")
        return cls._mappings[rig_type]()

    @classmethod
    def get_supported_rigs(cls):
        return list(cls._mappings.keys())

    @classmethod
    def get_bone_hierarchy(cls, rig_type):
        mapping = cls.create_mapping(rig_type)
        return mapping.get_bone_hierarchy()

    @classmethod
    def get_pose_mapping(cls, rig_type):
        mapping = cls.create_mapping(rig_type)
        return mapping.get_pose_mapping()

    @classmethod
    def get_face_mapping(cls, rig_type):
        mapping = cls.create_mapping(rig_type)
        return mapping.get_face_mapping()

    @classmethod
    def get_hand_mapping(cls, rig_type):
        mapping = cls.create_mapping(rig_type)
        return mapping.get_hand_mapping() 
        