"""
IMPORTANT: The mesh and armature must be upright (Z up) and in T-pose before starting capture.
If your mesh is lying down, apply rotation and scale in Object Mode (Ctrl+A) to both the armature and mesh.
"""
import bpy
import math
import json
import os
from mathutils import Vector, Matrix, Euler
from .mappings.mapping_factory import RigMappingFactory
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger("AniMateRigMapper")
logger.setLevel(logging.DEBUG)

class BlenderRigMapper:
    def __init__(self, armature_obj=None, rig_type='MIXAMO'):
        print(f"[AniMateRigMapper] Creating BlenderRigMapper for rig_type={rig_type}")
        self.armature = armature_obj
        self.driver_objects = {}  # Store driver objects
        self.mapping = RigMappingFactory.create_mapping(rig_type)
        self.prefix = ''
        self.blend_to_rest_pose = False  # Option to blend to rest pose if data missing
        self.rig_data = {}  # Store rig data including bone positions and rotations
        self.is_initialized = False  # Flag to track if rig has been initialized
        self.foot_locked = False  # Flag for foot locking
        self.motion_locked = False  # Flag for motion locking
        self.original_pose = {}  # Store original pose data
        self.motion_smoothing = 0.5  # Motion smoothing factor (0-1)
        self.region_locks = {  # Region-specific locks
            'upper_body': False,
            'lower_body': False,
            'left_arm': False,
            'right_arm': False,
            'head': False
        }
        
        # Per-bone axis correction for Mixamo bones
        self.axis_corrections = self.mapping.get_axis_corrections()
        if armature_obj:
            self.setup_armature(armature_obj)

    def setup_armature(self, armature_obj):
        print(f"[AniMateRigMapper] Setting up armature: {armature_obj.name if armature_obj else 'None'}")
        self.armature = armature_obj
        if not self.armature or self.armature.type != 'ARMATURE':
            print("[AniMateRigMapper] ERROR: Invalid armature object")
            raise ValueError("Invalid armature object")
        
        # Detect common prefix (e.g., 'mixamorig:')
        bone_names = [bone.name for bone in self.armature.pose.bones]
        prefix = ''
        if bone_names:
            # Find the longest common prefix ending with ':'
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
        # Store pose bones for quick access
        self.pose_bones = {bone.name: bone for bone in self.armature.pose.bones}
        print(f"[AniMateRigMapper] Detected bones: {list(self.pose_bones.keys())}")
        
        # Verify bone hierarchy matches the mapping
        self._verify_bone_hierarchy()

    def _create_driver_objects(self):
        """Create empty objects to drive bone rotations and add constraints. Store rest pose offsets."""
        # Remove old driver objects
        for obj in list(bpy.data.objects):
            if obj.name.startswith("Driver_"):
                bpy.data.objects.remove(obj, do_unlink=True)
        # Remove old AniMate constraints
        if self.armature:
            for pose_bone in self.armature.pose.bones:
                for c in list(pose_bone.constraints):
                    if c.name.startswith("AniMate_CopyRot"):
                        pose_bone.constraints.remove(c)
        driver_collection = bpy.data.collections.get("AniMate_Drivers")
        if not driver_collection:
            driver_collection = bpy.data.collections.new("AniMate_Drivers")
            bpy.context.scene.collection.children.link(driver_collection)
        self.rest_pose_rotations = {}  # Store rest pose rotation for each bone
        self.driver_objects = {}
        for bone in self.armature.data.bones:
            driver_name = f"Driver_{bone.name}"
            driver = bpy.data.objects.new(driver_name, None)
            driver_collection.objects.link(driver)
            driver.parent = self.armature
            driver.parent_type = 'OBJECT'
            driver.location = bone.head_local
            # Set driver rotation to match bone's rest pose
            if bone.name in self.armature.pose.bones:
                pose_bone = self.armature.pose.bones[bone.name]
                rest_rot = pose_bone.matrix.to_euler()
                driver.rotation_euler = rest_rot
                self.rest_pose_rotations[bone.name] = rest_rot
                if bone.name in [self.prefix + 'Hips', self.prefix + 'Spine', self.prefix + 'Spine1', self.prefix + 'Spine2', self.prefix + 'Neck', self.prefix + 'Head']:
                    print(f"[DEBUG] Rest pose for {bone.name}: {rest_rot}")
                # Add Copy Rotation constraint
                constraint = pose_bone.constraints.new(type='COPY_ROTATION')
                constraint.name = f"AniMate_CopyRot_{bone.name}"
                constraint.target = driver
                constraint.target_space = 'WORLD'
                constraint.owner_space = 'POSE'
                print(f"[DEBUG] Constraint for {bone.name}: WORLD/POSE")
                constraint.mix_mode = 'REPLACE'
                print(f"[DEBUG] Created driver and constraint for {bone.name}")
            self.driver_objects[bone.name] = driver

    def process_pose_landmarks(self, landmarks):
        """Process pose landmarks and apply to driver objects with region-based isolation."""
        if not self.armature or not landmarks:
            print("[AniMateRigMapper] WARNING: No armature or landmarks for pose processing.")
            return
        world_coords = {}
        for i, landmark in enumerate(landmarks.landmark):
            if hasattr(landmark, 'visibility') and landmark.visibility > 0.5:
                world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))
        pose_mapping = self.mapping.get_pose_mapping()
        for bone_name, landmark_indices in pose_mapping.items():
            full_bone_name = self.prefix + bone_name
            if full_bone_name not in self.driver_objects:
                print(f"[AniMateRigMapper] WARNING: Bone '{full_bone_name}' from mapping not found in rig. Skipping.")
                continue
            # Region-based isolation logic
            if bone_name == "Hips":
                required = [11, 12, 23, 24]
                if any(idx not in world_coords for idx in required):
                    print(f"[AniMateRigMapper] Skipping {full_bone_name}: required hips/shoulders not visible.")
                    continue
            if bone_name in ["Spine", "Spine1", "Spine2"]:
                required = [11, 12]
                if any(idx not in world_coords for idx in required):
                    print(f"[AniMateRigMapper] Skipping {full_bone_name}: required shoulders not visible.")
                    continue
            if bone_name in ["Neck", "Head"]:
                required = [0, 2, 8]
                if any(idx not in world_coords for idx in required):
                    print(f"[AniMateRigMapper] Skipping {full_bone_name}: required head/neck not visible.")
                    continue
            if any(idx not in world_coords for idx in landmark_indices):
                if self.blend_to_rest_pose:
                    driver = self.driver_objects[full_bone_name]
                    rest_rot = self.rest_pose_rotations.get(bone_name, Euler((0, 0, 0)))
                    driver.rotation_euler = driver.rotation_euler.lerp(rest_rot, 0.2)
                print(f"[AniMateRigMapper] Skipping {full_bone_name}: not all required landmarks present.")
                continue
            if len(landmark_indices) == 2:
                start_point = world_coords[landmark_indices[0]]
                end_point = world_coords[landmark_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                rotation = self.apply_rotation_limits(bone_name, rotation)
                scale_factor = self.mapping.get_bone_scale_factors().get(bone_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, rotation.y * scale_factor, rotation.z * scale_factor))
                # Apply per-bone axis correction ONLY (no global _remap_axes)
                axis_correction_fn = self.get_axis_correction(bone_name)
                corrected_euler = axis_correction_fn(rotation)
                rest_rot = self.rest_pose_rotations.get(bone_name, Euler((0, 0, 0)))
                # Set driver rotation RELATIVE to rest pose
                final_driver_rot = (rest_rot.to_matrix().inverted() @ corrected_euler.to_matrix()).to_euler()
                driver = self.driver_objects[full_bone_name]
                # Debug prints for key bones
                if bone_name in ["Hips", "Spine", "Spine1", "Spine2", "Neck", "Head", "LeftArm", "LeftForeArm", "RightArm", "RightForeArm"]:
                    print(f"[DEBUG] {full_bone_name} rest_euler: {rest_rot}, raw: {rotation}, corrected: {corrected_euler}, final_driver: {final_driver_rot}")
                driver.rotation_euler = final_driver_rot

    def _verify_bone_hierarchy(self):
        """Verify that the armature's bone hierarchy matches the mapping."""
        expected_hierarchy = self.mapping.get_bone_hierarchy()
        actual_bones = {bone.name: bone for bone in self.armature.data.bones}
        
        def check_hierarchy(expected, parent=None):
            for bone_name, children in expected.items():
                if bone_name not in actual_bones:
                    print(f"Warning: Expected bone '{bone_name}' not found in armature")
                    continue
                    
                if parent and actual_bones[bone_name].parent != actual_bones[parent]:
                    print(f"Warning: Bone '{bone_name}' has unexpected parent")
                    
                check_hierarchy(children, bone_name)
        
        check_hierarchy(expected_hierarchy)

    def calculate_bone_rotation(self, start_point, end_point, up_vector=Vector((0, 1, 0))):
        # For Blender Z-up, use Y as up vector for Mixamo
        bone_vector = end_point - start_point
        bone_vector.normalize()
        y_axis = bone_vector
        z_axis = up_vector.cross(y_axis)
        z_axis.normalize()
        x_axis = y_axis.cross(z_axis)
        rot_matrix = Matrix((x_axis, y_axis, z_axis)).to_4x4()
        return rot_matrix.to_euler('XYZ')

    def apply_rotation_limits(self, bone_name, rotation):
        """Apply rotation limits to the bone."""
        limits = self.mapping.get_bone_rotation_limits()
        if bone_name in limits:
            bone_limits = limits[bone_name]
            for axis in ['x', 'y', 'z']:
                if axis in bone_limits:
                    min_val, max_val = bone_limits[axis]
                    setattr(rotation, axis, max(min_val, min(max_val, getattr(rotation, axis))))
        return rotation

    def get_axis_correction(self, bone_name):
        """Get the axis correction function for a bone, or identity if not specified."""
        full_bone_name = self.prefix + bone_name
        return self.axis_corrections.get(full_bone_name, lambda e: e)

    def process_face_landmarks(self, landmarks):
        """Process face landmarks and apply to face driver objects (isolation: only if face landmarks present)."""
        if not landmarks:
            print("[AniMateRigMapper] WARNING: No landmarks for face processing.")
            return
        face_mapping = self.mapping.get_face_mapping()
        world_coords = {}
        for i, landmark in enumerate(landmarks.landmark):
            if hasattr(landmark, 'visibility') and landmark.visibility > 0.5:
                world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))
        for bone_name, landmark_indices in face_mapping.items():
            full_bone_name = self.prefix + bone_name
            if full_bone_name not in self.driver_objects:
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
                rest_rot = self.rest_pose_rotations.get(bone_name, Euler((0, 0, 0)))
                corrected_rot = (rest_rot.to_matrix().inverted() @ rotation.to_matrix()).to_euler()
                driver = self.driver_objects[full_bone_name]
                print(f"[DEBUG] Setting {full_bone_name} driver rotation: {corrected_rot}")
                driver.rotation_euler = corrected_rot

    def process_hand_landmarks(self, landmarks, is_right_hand=True):
        """Process hand landmarks and apply to hand driver objects (isolation: only if hand landmarks present)."""
        if not landmarks:
            print("[AniMateRigMapper] WARNING: No landmarks for hand processing.")
            return
        hand_mapping = self.mapping.get_hand_mapping()
        world_coords = {}
        for i, landmark in enumerate(landmarks.landmark):
            if hasattr(landmark, 'visibility') and landmark.visibility > 0.5:
                world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))
        for finger_name, joint_indices in hand_mapping.items():
            if is_right_hand and not finger_name.endswith('.R'):
                continue
            if not is_right_hand and not finger_name.endswith('.L'):
                continue
            bone_name = finger_name
            full_bone_name = self.prefix + bone_name
            if full_bone_name not in self.driver_objects:
                continue
            if any(idx not in world_coords for idx in joint_indices):
                continue
            if len(joint_indices) == 2:
                start_point = world_coords[joint_indices[0]]
                end_point = world_coords[joint_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                rotation = self.apply_rotation_limits(bone_name, rotation)
                scale_factor = self.mapping.get_bone_scale_factors().get(bone_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, rotation.y * scale_factor, rotation.z * scale_factor))
                axis_correction_fn = self.get_axis_correction(bone_name)
                corrected_rot = axis_correction_fn(rotation)
                driver = self.driver_objects[full_bone_name]
                print(f"[DEBUG] Setting {full_bone_name} driver rotation: {corrected_rot}")
                driver.rotation_euler = corrected_rot

    def update_rig(self, pose_landmarks=None, face_landmarks=None, left_hand_landmarks=None, right_hand_landmarks=None):
        """Update the entire rig with new landmark data, processing both hands independently."""
        if not self.armature:
            return

        # Process all landmark types
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

    def scan_rig(self):
        """Scan the rig and store all bone data including positions and rotations."""
        if not self.armature:
            print("[AniMateRigMapper] ERROR: No armature to scan")
            return False

        print("[AniMateRigMapper] Scanning rig...")
        self.rig_data = {
            'armature_name': self.armature.name,
            'bones': {},
            'mapping': {
                'pose': self.mapping.get_pose_mapping(),
                'face': self.mapping.get_face_mapping(),
                'hand': self.mapping.get_hand_mapping()
            }
        }

        # Store data for each bone
        for bone in self.armature.data.bones:
            bone_data = {
                'head': list(bone.head_local),
                'tail': list(bone.tail_local),
                'matrix_local': [list(row) for row in bone.matrix_local],
                'parent': bone.parent.name if bone.parent else None,
                'use_connect': bone.use_connect,
                'use_inherit_rotation': bone.use_inherit_rotation,
                'use_local_location': bone.use_local_location,
                'use_relative_parent': bone.use_relative_parent
            }
            self.rig_data['bones'][bone.name] = bone_data

        print(f"[AniMateRigMapper] Rig scan complete. Found {len(self.rig_data['bones'])} bones.")
        return True

    def save_rig_data(self, filepath=None):
        """Save rig data to a JSON file."""
        if not self.rig_data:
            print("[AniMateRigMapper] ERROR: No rig data to save")
            return False

        if filepath is None:
            # Use default path in the same directory as the blend file
            blend_file_path = bpy.data.filepath
            if not blend_file_path:
                print("[AniMateRigMapper] ERROR: Blend file not saved")
                return False
            filepath = os.path.join(os.path.dirname(blend_file_path), f"{self.armature.name}_rig_data.json")

        try:
            with open(filepath, 'w') as f:
                json.dump(self.rig_data, f, indent=2)
            print(f"[AniMateRigMapper] Rig data saved to {filepath}")
            return True
        except Exception as e:
            print(f"[AniMateRigMapper] ERROR saving rig data: {str(e)}")
            return False

    def load_rig_data(self, filepath):
        """Load rig data from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                self.rig_data = json.load(f)
            print(f"[AniMateRigMapper] Rig data loaded from {filepath}")
            return True
        except Exception as e:
            print(f"[AniMateRigMapper] ERROR loading rig data: {str(e)}")
            return False

    def initialize_rig(self):
        """Initialize the rig by setting up drivers and constraints."""
        if not self.armature:
            print("[AniMateRigMapper] ERROR: No armature to initialize")
            return False

        print("[AniMateRigMapper] Initializing rig...")
        
        # Create driver objects and constraints
        self._create_driver_objects()
        
        # Lock only the feet bones by default (not all bones)
        self._lock_bones()
        
        self.is_initialized = True
        print("[AniMateRigMapper] Rig initialization complete")
        return True

    def _lock_bones(self):
        """Lock only the feet bones by default (not all bones)."""
        if not self.rig_data:
            print("[AniMateRigMapper] WARNING: No rig data available for locking bones")
            return

        print("[AniMateRigMapper] Locking feet bones to initial positions...")
        foot_bones = [self.prefix + 'LeftFoot', self.prefix + 'RightFoot']
        for bone_name in foot_bones:
            if bone_name in self.armature.pose.bones:
                pose_bone = self.armature.pose.bones[bone_name]
                pose_bone.lock_location = (True, True, True)
                pose_bone.lock_rotation = (True, True, True)
                pose_bone.lock_scale = (True, True, True)
                print(f"[DEBUG] Locked foot bone: {bone_name}")

    def toggle_foot_lock(self):
        """Toggle foot locking on/off."""
        self.foot_locked = not self.foot_locked
        print(f"[AniMateRigMapper] Foot lock {'enabled' if self.foot_locked else 'disabled'}")
        
        if self.foot_locked:
            # Lock feet bones
            foot_bones = ['mixamorig:LeftFoot', 'mixamorig:RightFoot']
            for bone_name in foot_bones:
                if bone_name in self.armature.pose.bones:
                    pose_bone = self.armature.pose.bones[bone_name]
                    pose_bone.lock_location = (True, True, True)
                    pose_bone.lock_rotation = (True, True, True)
        else:
            # Unlock feet bones
            foot_bones = ['mixamorig:LeftFoot', 'mixamorig:RightFoot']
            for bone_name in foot_bones:
                if bone_name in self.armature.pose.bones:
                    pose_bone = self.armature.pose.bones[bone_name]
                    pose_bone.lock_location = (False, False, False)
                    pose_bone.lock_rotation = (False, False, False)

    def toggle_motion_lock(self):
        """Toggle motion locking on/off."""
        self.motion_locked = not self.motion_locked
        print(f"[AniMateRigMapper] Motion lock {'enabled' if self.motion_locked else 'disabled'}")
        
        if self.motion_locked:
            # Lock all bones except hands and face
            for bone in self.armature.pose.bones:
                if not (bone.name.startswith('mixamorig:LeftHand') or 
                       bone.name.startswith('mixamorig:RightHand') or
                       bone.name.startswith('mixamorig:Head')):
                    bone.lock_location = (True, True, True)
                    bone.lock_rotation = (True, True, True)
        else:
            # Unlock all bones
            for bone in self.armature.pose.bones:
                bone.lock_location = (False, False, False)
                bone.lock_rotation = (False, False, False)

    def validate_rig(self):
        """Validate the rig setup and return any issues found."""
        issues = []
        
        if not self.armature:
            issues.append("No armature object found")
            return issues
            
        # Check if armature is in T-pose
        if not self._is_t_pose():
            issues.append("Armature is not in T-pose")
            
        # Check for required bones
        required_bones = [
            'mixamorig:Hips',
            'mixamorig:Spine',
            'mixamorig:LeftArm',
            'mixamorig:RightArm',
            'mixamorig:LeftLeg',
            'mixamorig:RightLeg'
        ]
        
        for bone_name in required_bones:
            if bone_name not in self.armature.pose.bones:
                issues.append(f"Required bone {bone_name} not found")
                
        # Check bone hierarchy
        if not self._verify_bone_hierarchy():
            issues.append("Bone hierarchy verification failed")
            
        # Check for mesh parent
        if not self.armature.children:
            issues.append("No mesh parented to armature")
            
        return issues

    def _is_t_pose(self):
        """Check if the armature is in T-pose."""
        if not self.armature:
            return False
            
        # Check arm angles
        left_arm = self.armature.pose.bones.get('mixamorig:LeftArm')
        right_arm = self.armature.pose.bones.get('mixamorig:RightArm')
        
        if left_arm and right_arm:
            left_angle = left_arm.matrix.to_euler().y
            right_angle = right_arm.matrix.to_euler().y
            
            # Arms should be roughly horizontal (90 degrees)
            return abs(left_angle - math.radians(90)) < 0.1 and abs(right_angle - math.radians(-90)) < 0.1
            
        return False

    def store_original_pose(self):
        """Store the original pose of the armature."""
        if not self.armature:
            return False
            
        self.original_pose = {}
        for bone in self.armature.pose.bones:
            self.original_pose[bone.name] = {
                'matrix': bone.matrix.copy(),
                'matrix_basis': bone.matrix_basis.copy(),
                'location': bone.location.copy(),
                'rotation_quaternion': bone.rotation_quaternion.copy(),
                'rotation_euler': bone.rotation_euler.copy(),
                'scale': bone.scale.copy()
            }
        print("[AniMateRigMapper] Original pose stored")
        return True

    def restore_original_pose(self):
        """Restore the armature to its original pose."""
        if not self.armature or not self.original_pose:
            return False
            
        for bone in self.armature.pose.bones:
            if bone.name in self.original_pose:
                pose_data = self.original_pose[bone.name]
                bone.matrix = pose_data['matrix']
                bone.matrix_basis = pose_data['matrix_basis']
                bone.location = pose_data['location']
                bone.rotation_quaternion = pose_data['rotation_quaternion']
                bone.rotation_euler = pose_data['rotation_euler']
                bone.scale = pose_data['scale']
                
        print("[AniMateRigMapper] Original pose restored")
        return True

    def set_motion_smoothing(self, factor):
        """Set the motion smoothing factor (0-1)."""
        self.motion_smoothing = max(0.0, min(1.0, factor))
        print(f"[AniMateRigMapper] Motion smoothing set to {self.motion_smoothing}")

    def toggle_region_lock(self, region):
        """Toggle lock for a specific body region."""
        if region not in self.region_locks:
            print(f"[AniMateRigMapper] ERROR: Unknown region {region}")
            return
            
        self.region_locks[region] = not self.region_locks[region]
        print(f"[AniMateRigMapper] {region} lock {'enabled' if self.region_locks[region] else 'disabled'}")
        
        # Define bone groups for each region
        region_bones = {
            'upper_body': ['mixamorig:Spine', 'mixamorig:Spine1', 'mixamorig:Spine2', 'mixamorig:Neck'],
            'lower_body': ['mixamorig:Hips', 'mixamorig:LeftUpLeg', 'mixamorig:RightUpLeg'],
            'left_arm': ['mixamorig:LeftArm', 'mixamorig:LeftForeArm', 'mixamorig:LeftHand'],
            'right_arm': ['mixamorig:RightArm', 'mixamorig:RightForeArm', 'mixamorig:RightHand'],
            'head': ['mixamorig:Head', 'mixamorig:Neck']
        }
        
        # Apply locks to bones in the region
        for bone_name in region_bones.get(region, []):
            if bone_name in self.armature.pose.bones:
                pose_bone = self.armature.pose.bones[bone_name]
                pose_bone.lock_location = (self.region_locks[region],) * 3
                pose_bone.lock_rotation = (self.region_locks[region],) * 3
                pose_bone.lock_scale = (self.region_locks[region],) * 3

    def apply_motion_smoothing(self, new_rotation, current_rotation):
        """Apply motion smoothing to rotation changes."""
        if self.motion_smoothing == 0:
            return new_rotation
            
        # Interpolate between current and new rotation
        smoothed = Euler((
            current_rotation.x + (new_rotation.x - current_rotation.x) * self.motion_smoothing,
            current_rotation.y + (new_rotation.y - current_rotation.y) * self.motion_smoothing,
            current_rotation.z + (new_rotation.z - current_rotation.z) * self.motion_smoothing
        ))
        return smoothed 
                    