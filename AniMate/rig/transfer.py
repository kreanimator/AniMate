"""
Transfer logic for AniMate Blender addon.
"""
from mathutils import Euler, Vector, Matrix
from typing import Any, Dict, Callable

class TransferManager:
    """Handles transfer of landmark data to Blender rig drivers."""
    def __init__(self, driver_manager: Any, mapping: Any):
        """
        Args:
            driver_manager: DriverManager instance
            mapping: Rig mapping instance
        """
        self.driver_manager = driver_manager
        self.mapping = mapping

    def apply_pose_landmarks(self, world_coords: Dict[int, Vector], pose_mapping: Dict[str, Any], axis_corrections: Dict[str, Callable], rest_pose_rotations: Dict[str, Euler]) -> None:
        """
        Apply pose landmarks to the rig drivers.
        """
        for bone_name, landmark_indices in pose_mapping.items():
            full_bone_name = self.driver_manager.prefix + bone_name
            print(f"[AniMate] Checking mapping for bone: {full_bone_name}, indices: {landmark_indices}")
            if full_bone_name not in self.driver_manager.driver_objects:
                print(f"[AniMate] Bone {full_bone_name} not in driver objects")
                continue
            if any(idx not in world_coords for idx in landmark_indices):
                print(f"[AniMate] Not all indices present for bone {full_bone_name}")
                continue
            if len(landmark_indices) == 2:
                start_point = world_coords[landmark_indices[0]]
                end_point = world_coords[landmark_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                rotation = self.apply_rotation_limits(full_bone_name, rotation)
                scale_factor = self.mapping.get_bone_scale_factors().get(bone_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, rotation.y * scale_factor, rotation.z * scale_factor))
                axis_correction_fn = axis_corrections.get(full_bone_name, lambda e: e)
                corrected_euler = axis_correction_fn(rotation)
                rest_rot = rest_pose_rotations.get(full_bone_name, Euler((0, 0, 0)))
                final_driver_rot = (rest_rot.to_matrix().inverted() @ corrected_euler.to_matrix()).to_euler()
                print(f"[AniMate] Applying rotation to driver {full_bone_name}")
                self.driver_manager.update_driver(full_bone_name, final_driver_rot)

    def calculate_bone_rotation(self, start_point: Vector, end_point: Vector, up_vector: Vector = Vector((0, 1, 0))) -> Euler:
        """
        Calculate bone rotation from start and end points.
        """
        bone_vector = end_point - start_point
        bone_vector.normalize()
        y_axis = bone_vector
        z_axis = up_vector.cross(y_axis)
        z_axis.normalize()
        x_axis = y_axis.cross(z_axis)
        rot_matrix = Matrix((x_axis, y_axis, z_axis)).to_4x4()
        return rot_matrix.to_euler('XYZ')

    def apply_rotation_limits(self, bone_name: str, rotation: Euler) -> Euler:
        """
        Apply rotation limits to the bone.
        """
        limits = self.mapping.get_bone_rotation_limits()
        if bone_name in limits:
            bone_limits = limits[bone_name]
            for axis in ['x', 'y', 'z']:
                if axis in bone_limits:
                    min_val, max_val = bone_limits[axis]
                    setattr(rotation, axis, max(min_val, min(max_val, getattr(rotation, axis))))
        return rotation

    def apply_hand_landmarks(self, world_coords: Dict[int, Vector], hand_mapping: Dict[str, Any], axis_corrections: Dict[str, Callable], rest_pose_rotations: Dict[str, Euler], is_right_hand: bool = True) -> None:
        """
        Apply hands landmarks to the rig drivers.
        """
        print(f"[AniMate] apply_hand_landmarks called for hand, is_right_hand={is_right_hand}")
        print(f"[AniMate] apply_hand_landmarks mapping keys: {list(hand_mapping.keys())}")
        for finger_name, joint_indices in hand_mapping.items():
            print(f"[AniMate] Checking {finger_name} with indices {joint_indices}")
            full_bone_name = self.driver_manager.prefix + finger_name
            if full_bone_name not in self.driver_manager.driver_objects:
                print(f"[AniMate] SKIP: Bone {full_bone_name} not in driver objects")
                continue
            if any(idx not in world_coords for idx in joint_indices):
                print(f"[AniMate] SKIP: Not all indices present for bone {full_bone_name}")
                continue
            print(f"[AniMate] UPDATING: {full_bone_name} with indices {joint_indices}")
            if len(joint_indices) == 2:
                start_point = world_coords[joint_indices[0]]
                end_point = world_coords[joint_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                rotation = self.apply_rotation_limits(full_bone_name, rotation)
                scale_factor = self.mapping.get_bone_scale_factors().get(finger_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, rotation.y * scale_factor, rotation.z * scale_factor))
                axis_correction_fn = axis_corrections.get(full_bone_name, lambda e: e)
                corrected_rot = axis_correction_fn(rotation)
                rest_rot = rest_pose_rotations.get(full_bone_name, Euler((0, 0, 0)))
                final_driver_rot = (rest_rot.to_matrix().inverted() @ corrected_rot.to_matrix()).to_euler()
                self.driver_manager.update_driver(full_bone_name, final_driver_rot)

    def apply_face_landmarks(self, world_coords: Dict[int, Vector], face_mapping: Dict[str, Any], rest_pose_rotations: Dict[str, Euler]) -> None:
        """
        Apply face landmarks to the rig drivers.
        """
        for bone_name, landmark_indices in face_mapping.items():
            if bone_name not in self.driver_manager.driver_objects:
                continue
            if any(idx not in world_coords for idx in landmark_indices):
                continue
            if len(landmark_indices) == 2:
                start_point = world_coords[landmark_indices[0]]
                end_point = world_coords[landmark_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                rotation = self.apply_rotation_limits(bone_name, rotation)
                scale_factor = self.mapping.get_bone_scale_factors().get(bone_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, rotation.y * scale_factor, rotation.z * scale_factor))
                rest_rot = rest_pose_rotations.get(bone_name, Euler((0, 0, 0)))
                final_driver_rot = (rest_rot.to_matrix().inverted() @ rotation.to_matrix()).to_euler()
                self.driver_manager.update_driver(bone_name, final_driver_rot) 
                