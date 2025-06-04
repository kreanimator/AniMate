"""
Maya rig mapping implementation.
"""
from .base_mappings import BaseRigMapping

class MayaMapping(BaseRigMapping):
    def get_bone_hierarchy(self):
        return {}

    def get_pose_mapping(self):
        return {}

    def get_face_mapping(self):
        return {}

    def get_hand_mapping(self):
        return {}

    def get_bone_rotation_limits(self):
        return {}

    def get_bone_scale_factors(self):
        return {}

    def get_capabilities(self):
        return {
            'face': False,
            'hands': False,
        }

    def get_axis_corrections(self):
        return {} 