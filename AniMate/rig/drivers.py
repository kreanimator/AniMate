"""
Driver management for AniMate Blender addon.
"""
import bpy
from mathutils import Euler
from typing import Dict, Optional, Any

class DriverManager:
    """Manages driver objects and constraints for rig motion transfer."""
    def __init__(self, armature: bpy.types.Object, mapping: Any, prefix: str):
        """
        Args:
            armature: Blender armature object
            mapping: Rig mapping instance
            prefix: Bone name prefix
        """
        self.armature = armature
        self.mapping = mapping
        self.prefix = prefix
        self.driver_objects: Dict[str, bpy.types.Object] = {}
        self.rest_pose_rotations: Dict[str, Euler] = {}

    def create_drivers(self) -> None:
        """
        Create driver empties and constraints for each bone in the armature.
        """
        driver_collection = bpy.data.collections.get("AniMate_Drivers")
        if not driver_collection:
            driver_collection = bpy.data.collections.new("AniMate_Drivers")
            bpy.context.scene.collection.children.link(driver_collection)
        for bone in self.armature.data.bones:
            driver_name = f"Driver_{bone.name}"
            driver = bpy.data.objects.new(driver_name, None)
            driver_collection.objects.link(driver)
            driver.parent = self.armature
            driver.parent_type = 'OBJECT'
            driver.location = bone.head_local
            if bone.name in self.armature.pose.bones:
                pose_bone = self.armature.pose.bones[bone.name]
                rest_rot = pose_bone.matrix.to_euler()
                driver.rotation_euler = rest_rot
                self.rest_pose_rotations[bone.name] = rest_rot
                constraint = pose_bone.constraints.new(type='COPY_ROTATION')
                constraint.name = f"AniMate_CopyRot_{bone.name}"
                constraint.target = driver
                constraint.target_space = 'WORLD'
                constraint.owner_space = 'POSE'
                constraint.mix_mode = 'REPLACE'
            self.driver_objects[bone.name] = driver

    def update_driver(self, bone_name: str, euler: Euler) -> None:
        """
        Update the rotation of a driver object.
        Args:
            bone_name: Name of the bone/driver
            euler: Euler rotation to set
        """
        driver = self.driver_objects.get(bone_name)
        if driver:
            print(f"[AniMate] Updating driver {bone_name} to {euler}")
            driver.rotation_euler = euler

    def cleanup(self) -> None:
        """
        Remove all driver objects and constraints created by AniMate.
        """
        for obj in list(bpy.data.objects):
            if obj.name.startswith("Driver_"):
                bpy.data.objects.remove(obj, do_unlink=True)
        if self.armature:
            for pose_bone in self.armature.pose.bones:
                for c in list(pose_bone.constraints):
                    if c.name.startswith("AniMate_CopyRot"):
                        pose_bone.constraints.remove(c) 