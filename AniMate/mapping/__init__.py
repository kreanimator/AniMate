"""
AniMate mapping package: provides mapping classes for different rig types.
"""
from .mixamo_mapping import MixamoMapping
from .rigify_mapping import RigifyMapping
from .maya_mapping import MayaMapping
from .base_mappings import BaseRigMapping
from .mapping_factory import RigMappingFactory

__all__ = [
    "MixamoMapping",
    "RigifyMapping",
    "MayaMapping",
    "BaseRigMapping",
    "RigMappingFactory",
] 