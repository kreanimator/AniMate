"""
IMPORTANT: The mesh and armature must be upright (Z up) and in T-pose before starting capture.
If your mesh is lying down, apply rotation and scale in Object Mode (Ctrl+A) to both the armature and mesh.
"""
import bpy
import math
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
        # Per-bone axis correction for Mixamo left hand (template for right hand)
        self.axis_corrections = {
            'mixamorig:LeftHand': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:RightHand': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandThumb1': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandThumb2': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandThumb3': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandIndex1': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandIndex2': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandIndex3': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandMiddle1': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandMiddle2': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandMiddle3': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandRing1': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandRing2': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandRing3': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandPinky1': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandPinky2': lambda e: Euler((e.x, e.z, -e.y)),
            'mixamorig:LeftHandPinky3': lambda e: Euler((e.x, e.z, -e.y)),
            # Add for right hand fingers as needed
        }
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
            self.driver_objects[bone.name] = driver
            if bone.name in self.armature.pose.bones:
                pose_bone = self.armature.pose.bones[bone.name]
                self.rest_pose_rotations[bone.name] = pose_bone.matrix.to_euler()
                # Add Copy Rotation constraint
                constraint = pose_bone.constraints.new(type='COPY_ROTATION')
                constraint.name = f"AniMate_CopyRot_{bone.name}"
                constraint.target = driver
                # Use LOCAL/LOCAL for Mixamo hand and finger bones
                if bone.name.startswith('mixamorig:LeftHand') or bone.name.startswith('mixamorig:RightHand'):
                    constraint.target_space = 'LOCAL'
                    constraint.owner_space = 'LOCAL'
                    print(f"[DEBUG] Constraint for {bone.name}: LOCAL/LOCAL")
                else:
                    constraint.target_space = 'WORLD'
                    constraint.owner_space = 'POSE'
                constraint.mix_mode = 'REPLACE'
                print(f"[DEBUG] Created driver and constraint for {bone.name}")

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

    def calculate_bone_rotation(self, start_point, end_point, up_vector=Vector((0, 0, 1))):
        """Calculate bone rotation from two points"""
        bone_vector = end_point - start_point
        bone_vector.normalize()
        
        # Calculate rotation matrix
        z_axis = bone_vector
        x_axis = up_vector.cross(z_axis)
        x_axis.normalize()
        y_axis = z_axis.cross(x_axis)
        
        rot_matrix = Matrix((x_axis, y_axis, z_axis)).to_4x4().transposed()
        return rot_matrix.to_euler()

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

    def _remap_axes(self, euler):
        """Remap axes from MediaPipe to Blender for Mixamo: swap Y and Z, invert new Z."""
        return Euler((euler.x, euler.z, -euler.y))

    def get_axis_correction(self, bone_name):
        """Get the axis correction function for a bone, or identity if not specified."""
        full_bone_name = self.prefix + bone_name
        return self.axis_corrections.get(full_bone_name, lambda e: e)

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
                continue
            # Region-based isolation logic
            if bone_name == "Hips":
                required = [11, 12, 23, 24]
                if any(idx not in world_coords for idx in required):
                    continue
            if bone_name in ["Spine", "Spine1", "Spine2"]:
                required = [11, 12]
                if any(idx not in world_coords for idx in required):
                    continue
            if bone_name in ["Neck", "Head"]:
                required = [0, 2, 8]
                if any(idx not in world_coords for idx in required):
                    continue
            if any(idx not in world_coords for idx in landmark_indices):
                if self.blend_to_rest_pose:
                    driver = self.driver_objects[full_bone_name]
                    rest_rot = self.rest_pose_rotations.get(bone_name, Euler((0, 0, 0)))
                    driver.rotation_euler = driver.rotation_euler.lerp(rest_rot, 0.2)
                continue
            if len(landmark_indices) == 2:
                start_point = world_coords[landmark_indices[0]]
                end_point = world_coords[landmark_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                rotation = self.apply_rotation_limits(bone_name, rotation)
                scale_factor = self.mapping.get_bone_scale_factors().get(bone_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, rotation.y * scale_factor, rotation.z * scale_factor))
                rotation = self._remap_axes(rotation)
                rest_rot = self.rest_pose_rotations.get(bone_name, Euler((0, 0, 0)))
                corrected_rot = (rest_rot.to_matrix().inverted() @ rotation.to_matrix()).to_euler()
                driver = self.driver_objects[full_bone_name]
                print(f"[DEBUG] Setting {full_bone_name} driver rotation: {corrected_rot}")
                driver.rotation_euler = corrected_rot

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
                rotation = self._remap_axes(rotation)
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
                    