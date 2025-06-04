"""
Blender rig mapping implementation for real-time motion capture.
"""
import bpy
import logging
import sys
import math
import json
import os
from mathutils import Vector, Matrix, Euler
from typing import Dict, Optional, Any, List, Tuple
from ..mapping import RigMappingFactory
from .drivers import DriverManager
from .transfer import TransferManager

# Configure logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger("AniMateRigMapper")
logger.setLevel(logging.DEBUG)

class BlenderRigMapper:
    """Main class for mapping MediaPipe landmarks to Blender rig bones."""

    def __init__(self, armature_obj: Optional[bpy.types.Object] = None, rig_type: str = 'MIXAMO'):
        """
        Initialize the rig mapper.

        Args:
            armature_obj: The Blender armature object to map to
            rig_type: Type of rig ('MIXAMO', 'RIGIFY', etc.)
        """
        logger.info(f"Creating BlenderRigMapper for rig_type={rig_type}")
        self.armature = armature_obj
        self.driver_objects: Dict[str, bpy.types.Object] = {}
        self.mapping = RigMappingFactory.create_mapping(rig_type)
        self.prefix = ''
        self.blend_to_rest_pose = False
        self.rig_data: Dict[str, Any] = {}
        self.is_initialized = False
        self.foot_locked = False
        self.motion_locked = False
        self.original_pose: Dict[str, Any] = {}
        self.motion_smoothing = 0.5
        self.region_locks = {
            'upper_body': False,
            'lower_body': False,
            'left_arm': False,
            'right_arm': False,
            'head': False
        }
        
        self.axis_corrections = self.mapping.get_axis_corrections()
        if armature_obj:
            self.setup_armature(armature_obj)
        self.driver_manager = DriverManager(self.armature, self.mapping, self.prefix)
        self.transfer_manager = TransferManager(self.driver_manager, self.mapping)
        self.rest_pose_rotations = self.driver_manager.rest_pose_rotations

    def setup_armature(self, armature_obj: bpy.types.Object) -> None:
        """
        Set up the armature for mapping.

        Args:
            armature_obj: The Blender armature object to set up
        """
        logger.info(f"Setting up armature: {armature_obj.name if armature_obj else 'None'}")
        self.armature = armature_obj
        if not self.armature or self.armature.type != 'ARMATURE':
            logger.error("Invalid armature object")
            raise ValueError("Invalid armature object")
        
        # Detect common prefix (e.g., 'mixamorig:')
        bone_names = [bone.name for bone in self.armature.pose.bones]
        prefix = ''
        if bone_names:
            first = bone_names[0]
            for i in range(len(first)):
                c = first[i]
                for name in bone_names:
                    if i >= len(name) or name[i] != c:
                        prefix = first[:i]
                        break
                else:
                    continue
                break
            if prefix and not prefix.endswith(':'):
                prefix = ''
            self.prefix = prefix
        else:
            self.prefix = ''
            
        self.pose_bones = {bone.name: bone for bone in self.armature.pose.bones}
        logger.info(f"Detected bones: {list(self.pose_bones.keys())}")
        
        self._verify_bone_hierarchy()

    def process_pose_landmarks(self, landmarks: Any) -> None:
        """
        Process pose landmarks and apply to driver objects.

        Args:
            landmarks: MediaPipe pose landmarks
        """
        if not self.armature or not landmarks:
            logger.warning("No armature or landmarks for pose processing")
            return
            
        world_coords = {}
        for i, landmark in enumerate(landmarks.landmark):
            if hasattr(landmark, 'visibility') and landmark.visibility > 0.5:
                world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))
                
        pose_mapping = self.mapping.get_pose_mapping()
        self.transfer_manager.apply_pose_landmarks(
            world_coords, 
            pose_mapping, 
            self.axis_corrections, 
            self.driver_manager.rest_pose_rotations
        )

    def process_face_landmarks(self, landmarks: Any) -> None:
        """
        Process face landmarks and apply to driver objects.

        Args:
            landmarks: MediaPipe face landmarks
        """
        if not self.armature or not landmarks:
            logger.warning("No armature or landmarks for face processing")
            return
            
        world_coords = {}
        for i, landmark in enumerate(landmarks.landmark):
            if hasattr(landmark, 'visibility') and landmark.visibility > 0.5:
                world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))
                
        face_mapping = self.mapping.get_face_mapping()
        self.transfer_manager.apply_face_landmarks(
            world_coords, 
            face_mapping, 
            self.driver_manager.rest_pose_rotations
        )

    def process_hand_landmarks(self, landmarks: Any, is_right_hand: bool = True) -> None:
        """
        Process hand landmarks and apply to driver objects.

        Args:
            landmarks: MediaPipe hand landmarks
            is_right_hand: Whether this is the right hand
        """
        if not self.armature or not landmarks:
            logger.warning("No armature or landmarks for hand processing")
            return
            
        world_coords = {}
        for i, landmark in enumerate(landmarks.landmark):
            if hasattr(landmark, 'visibility') and landmark.visibility > 0.5:
                world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))
                
        hand_mapping = self.mapping.get_hand_mapping()
        self.transfer_manager.apply_hand_landmarks(
            world_coords,
            hand_mapping,
            self.axis_corrections,
            self.driver_manager.rest_pose_rotations,
            is_right_hand
        )

    def update_rig(self, 
                  pose_landmarks: Optional[Any] = None,
                  face_landmarks: Optional[Any] = None,
                  left_hand_landmarks: Optional[Any] = None,
                  right_hand_landmarks: Optional[Any] = None) -> None:
        """
        Update the entire rig with new landmark data.

        Args:
            pose_landmarks: MediaPipe pose landmarks
            face_landmarks: MediaPipe face landmarks
            left_hand_landmarks: MediaPipe left hand landmarks
            right_hand_landmarks: MediaPipe right hand landmarks
        """
        if not self.armature:
            return

        if pose_landmarks:
            self.process_pose_landmarks(pose_landmarks)
        if face_landmarks:
            self.process_face_landmarks(face_landmarks)
        if left_hand_landmarks:
            self.process_hand_landmarks(left_hand_landmarks, is_right_hand=False)
        if right_hand_landmarks:
            self.process_hand_landmarks(right_hand_landmarks, is_right_hand=True)
        
        # Update viewport
        bpy.context.view_layer.update()
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()

    def _verify_bone_hierarchy(self) -> None:
        """Verify that the armature's bone hierarchy matches the mapping."""
        expected_hierarchy = self.mapping.get_bone_hierarchy()
        actual_bones = {bone.name: bone for bone in self.armature.data.bones}
        
        def check_hierarchy(expected: Dict, parent: Optional[str] = None) -> None:
            for bone_name, children in expected.items():
                full_bone_name = self.prefix + bone_name
                if full_bone_name not in actual_bones:
                    logger.warning(f"Expected bone '{bone_name}' not found in armature")
                    continue
                if parent:
                    full_parent_name = self.prefix + parent
                    if actual_bones[full_bone_name].parent != actual_bones.get(full_parent_name):
                        logger.warning(f"Bone '{bone_name}' has unexpected parent")
                check_hierarchy(children, bone_name)
        
        check_hierarchy(expected_hierarchy)

    def calculate_bone_rotation(self, 
                              start_point: Vector,
                              end_point: Vector,
                              up_vector: Vector = Vector((0, 1, 0))) -> Euler:
        """
        Calculate bone rotation from start and end points.

        Args:
            start_point: Start point of the bone
            end_point: End point of the bone
            up_vector: Up vector for orientation

        Returns:
            Euler rotation for the bone
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

        Args:
            bone_name: Name of the bone
            rotation: Current rotation to limit

        Returns:
            Limited rotation
        """
        limits = self.mapping.get_bone_rotation_limits()
        if bone_name in limits:
            bone_limits = limits[bone_name]
            for axis in ['x', 'y', 'z']:
                if axis in bone_limits:
                    min_val, max_val = bone_limits[axis]
                    setattr(rotation, axis, max(min_val, min(max_val, getattr(rotation, axis))))
        return rotation

    def get_axis_correction(self, bone_name: str) -> Any:
        """
        Get the axis correction function for a bone.

        Args:
            bone_name: Name of the bone

        Returns:
            Axis correction function or identity if not specified
        """
        full_bone_name = self.prefix + bone_name
        return self.axis_corrections.get(full_bone_name, lambda e: e)

    def scan_rig(self) -> bool:
        """
        Scan the rig and store all bone data.

        Returns:
            True if scan was successful
        """
        if not self.armature:
            logger.error("No armature to scan")
            return False

        logger.info("Scanning rig...")
        self.rig_data = {
            'armature_name': self.armature.name,
            'bones': {},
            'mapping': {
                'pose': self.mapping.get_pose_mapping(),
                'face': self.mapping.get_face_mapping(),
                'hand': self.mapping.get_hand_mapping()
            }
        }
        
        for bone in self.armature.data.bones:
            self.rig_data['bones'][bone.name] = {
                'head': list(bone.head_local),
                'tail': list(bone.tail_local),
                'matrix_local': [list(row) for row in bone.matrix_local]
            }
            
        return True

    def save_rig_data(self, filepath: Optional[str] = None) -> None:
        """
        Save rig data to a JSON file.

        Args:
            filepath: Path to save the data to
        """
        if not self.rig_data:
            logger.warning("No rig data to save")
            return
            
        if not filepath:
            filepath = f"{self.armature.name}_rig_data.json"
            
        with open(filepath, 'w') as f:
            json.dump(self.rig_data, f, indent=2)
            
        logger.info(f"Saved rig data to {filepath}")

    def load_rig_data(self, filepath: str) -> bool:
        """
        Load rig data from a JSON file.

        Args:
            filepath: Path to load the data from

        Returns:
            True if load was successful
        """
        try:
            with open(filepath, 'r') as f:
                self.rig_data = json.load(f)
            return True
        except Exception as e:
            logger.error(f"Failed to load rig data: {e}")
            return False

    def initialize_rig(self) -> bool:
        """
        Initialize the rig for motion capture.

        Returns:
            True if initialization was successful
        """
        if not self.armature:
            logger.error("No armature to initialize")
            return False
            
        if not self._is_t_pose():
            logger.warning("Armature is not in T-pose")
            return False
            
        self.scan_rig()
        self.store_original_pose()
        self.is_initialized = True
        return True

    def _is_t_pose(self) -> bool:
        """
        Check if the armature is in T-pose.

        Returns:
            True if in T-pose
        """
        if not self.armature:
            return False
            
        # Check key bones for T-pose alignment
        spine = self.armature.pose.bones.get(self.prefix + 'Spine')
        left_arm = self.armature.pose.bones.get(self.prefix + 'LeftArm')
        right_arm = self.armature.pose.bones.get(self.prefix + 'RightArm')
        
        if not all([spine, left_arm, right_arm]):
            return False
            
        # Check if arms are roughly horizontal
        spine_dir = spine.tail - spine.head
        left_dir = left_arm.tail - left_arm.head
        right_dir = right_arm.tail - right_arm.head
        
        return (abs(left_dir.y) < 0.1 and abs(right_dir.y) < 0.1 and
                abs(left_dir.x + right_dir.x) < 0.1)

    def store_original_pose(self) -> None:
        """Store the original pose of the armature."""
        if not self.armature:
            return
            
        self.original_pose = {}
        for bone in self.armature.pose.bones:
            self.original_pose[bone.name] = {
                'rotation': list(bone.rotation_euler),
                'location': list(bone.location),
                'scale': list(bone.scale)
            }

    def restore_original_pose(self) -> None:
        """Restore the original pose of the armature."""
        if not self.armature or not self.original_pose:
            return
            
        for bone_name, pose_data in self.original_pose.items():
            bone = self.armature.pose.bones.get(bone_name)
            if bone:
                bone.rotation_euler = pose_data['rotation']
                bone.location = pose_data['location']
                bone.scale = pose_data['scale']

    def set_motion_smoothing(self, factor: float) -> None:
        """
        Set the motion smoothing factor.

        Args:
            factor: Smoothing factor (0-1)
        """
        self.motion_smoothing = max(0.0, min(1.0, factor))

    def toggle_region_lock(self, region: str) -> None:
        """
        Toggle locking of a specific region.

        Args:
            region: Region to toggle ('upper_body', 'lower_body', etc.)
        """
        if region in self.region_locks:
            self.region_locks[region] = not self.region_locks[region]
            logger.info(f"{region} lock: {self.region_locks[region]}")

    def apply_motion_smoothing(self, new_rotation: Euler, current_rotation: Euler) -> Euler:
        """
        Apply motion smoothing to a rotation.

        Args:
            new_rotation: New rotation to apply
            current_rotation: Current rotation to smooth from

        Returns:
            Smoothed rotation
        """
        return Euler((
            current_rotation.x + (new_rotation.x - current_rotation.x) * self.motion_smoothing,
            current_rotation.y + (new_rotation.y - current_rotation.y) * self.motion_smoothing,
            current_rotation.z + (new_rotation.z - current_rotation.z) * self.motion_smoothing
        ))

