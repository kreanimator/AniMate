"""
AniMate rig package: provides rig mapping, driver, and transfer logic.
"""
from .blender_mapper import BlenderRigMapper
from .drivers import DriverManager
from .transfer import TransferManager

__all__ = [
    "BlenderRigMapper",
    "DriverManager",
    "TransferManager",
] 