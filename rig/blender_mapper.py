"""
Blender rig mapper for motion capture.
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
        self.pose_bones = {}
        self.previous_rotations = {}
        self.mapping = RigMappingFactory.create_mapping(rig_type)
        self.prefix = ''
        self.upper_body_only = True  # Set to True to only update upper body
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

    def process_pose_landmarks(self, landmarks):
        """Process pose landmarks and apply to armature"""
        if not self.armature or not landmarks:
            print("[AniMateRigMapper] WARNING: No armature or landmarks for pose processing.")
            return

        # Convert landmarks to world space coordinates
        world_coords = {}
        for i, landmark in enumerate(landmarks.landmark):
            world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))

        pose_mapping = self.mapping.get_pose_mapping()

        # Expanded upper body and hand/finger bones
        upper_body_bones = [
            "Spine", "Spine1", "Spine2", "Neck", "Head", "HeadTop_End",
            "RightShoulder", "RightArm", "RightForeArm", "RightHand",
            "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand",
            # Right hand fingers
            "RightHandThumb1", "RightHandThumb2", "RightHandThumb3",
            "RightHandIndex1", "RightHandIndex2", "RightHandIndex3",
            "RightHandMiddle1", "RightHandMiddle2", "RightHandMiddle3",
            "RightHandRing1", "RightHandRing2", "RightHandRing3",
            "RightHandPinky1", "RightHandPinky2", "RightHandPinky3",
            # Left hand fingers
            "LeftHandThumb1", "LeftHandThumb2", "LeftHandThumb3",
            "LeftHandIndex1", "LeftHandIndex2", "LeftHandIndex3",
            "LeftHandMiddle1", "LeftHandMiddle2", "LeftHandMiddle3",
            "LeftHandRing1", "LeftHandRing2", "LeftHandRing3",
            "LeftHandPinky1", "LeftHandPinky2", "LeftHandPinky3"
        ]

        for bone_name, landmark_indices in pose_mapping.items():
            full_bone_name = self.prefix + bone_name
            if full_bone_name not in self.pose_bones:
                continue

            # Only update if all required landmark indices are present
            if any(idx not in world_coords for idx in landmark_indices):
                # Special handling for head/neck: keep last known good rotation
                if bone_name in ["Head", "Neck"] and bone_name in self.previous_rotations:
                    quat = self.previous_rotations[bone_name].to_quaternion()
                    self.pose_bones[full_bone_name].rotation_quaternion = quat
                continue

            # (Optional) Only update upper body bones if in upper_body_only mode
            if getattr(self, "upper_body_only", False):
                if bone_name not in upper_body_bones:
                    continue

            # Lock hips if not enough data
            if bone_name == "Hips":
                if not (23 in world_coords and 24 in world_coords):
                    continue

            # Calculate bone orientation from landmarks
            if len(landmark_indices) == 2:
                start_point = world_coords[landmark_indices[0]]
                end_point = world_coords[landmark_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                rotation = self.apply_rotation_limits(bone_name, rotation)
                scale_factor = self.mapping.get_bone_scale_factors().get(bone_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, rotation.y * scale_factor, rotation.z * scale_factor))
            else:
                continue

            # Smoothing
            if bone_name in self.previous_rotations:
                smoothing = 0.5
                rotation = Euler((
                    self.lerp(self.previous_rotations[bone_name].x, rotation.x, smoothing),
                    self.lerp(self.previous_rotations[bone_name].y, rotation.y, smoothing),
                    self.lerp(self.previous_rotations[bone_name].z, rotation.z, smoothing)
                ))

            self.previous_rotations[bone_name] = rotation
            quat = rotation.to_quaternion()
            self.pose_bones[full_bone_name].rotation_quaternion = quat

    def process_face_landmarks(self, landmarks):
        """Process face landmarks and apply to face rig/shape keys"""
        if not landmarks:
            print("[AniMateRigMapper] WARNING: No landmarks for face processing.")
            return
        
        # Get face mapping for this rig type
        face_mapping = self.mapping.get_face_mapping()
        
        # Process each mapped face bone
        for bone_name, landmark_indices in face_mapping.items():
            full_bone_name = self.prefix + bone_name
            if full_bone_name not in self.pose_bones:
                print(f"[AniMateRigMapper] WARNING: Face bone not found in armature: {full_bone_name}")
                continue
                
            # Convert landmarks to world space
            world_coords = {}
            for i, landmark in enumerate(landmarks.landmark):
                world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))
                
            # Calculate rotation from landmarks
            if len(landmark_indices) == 2:
                start_point = world_coords[landmark_indices[0]]
                end_point = world_coords[landmark_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                
                # Apply rotation limits and scale
                rotation = self.apply_rotation_limits(bone_name, rotation)
                scale_factor = self.mapping.get_bone_scale_factors().get(bone_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, 
                                rotation.y * scale_factor, 
                                rotation.z * scale_factor))
                                
                # Apply to bone
                print(f"[AniMateRigMapper] Updating face bone: {full_bone_name} with rotation {rotation}")
                self.pose_bones[full_bone_name].rotation_euler = rotation

    def process_hand_landmarks(self, landmarks, is_right_hand=True):
        """Process hand landmarks and apply to hand rig"""
        if not landmarks:
            print("[AniMateRigMapper] WARNING: No landmarks for hand processing.")
            return
            
        # Get hand mapping for this rig type
        hand_mapping = self.mapping.get_hand_mapping()
        
        # Convert landmarks to world space
        world_coords = {}
        for i, landmark in enumerate(landmarks.landmark):
            world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))
            
        # Process each finger
        for finger_name, joint_indices in hand_mapping.items():
            # Adjust bone name based on hand side
            bone_name = finger_name.replace('.L', '.R') if is_right_hand else finger_name
            full_bone_name = self.prefix + bone_name
            if full_bone_name not in self.pose_bones:
                print(f"[AniMateRigMapper] WARNING: Hand bone not found in armature: {full_bone_name}")
                continue
                
            # Calculate rotation from landmarks
            if len(joint_indices) == 2:
                start_point = world_coords[joint_indices[0]]
                end_point = world_coords[joint_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                
                # Apply rotation limits and scale
                rotation = self.apply_rotation_limits(bone_name, rotation)
                scale_factor = self.mapping.get_bone_scale_factors().get(bone_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, 
                                rotation.y * scale_factor, 
                                rotation.z * scale_factor))
                                
                # Apply to bone
                print(f"[AniMateRigMapper] Updating hand bone: {full_bone_name} with rotation {rotation}")
                self.pose_bones[full_bone_name].rotation_euler = rotation

    @staticmethod
    def lerp(a, b, t):
        """Linear interpolation between two values"""
        return a + (b - a) * t

    def update_rig(self, pose_landmarks=None, face_landmarks=None, left_hand_landmarks=None, right_hand_landmarks=None):
        """Update the entire rig with new landmark data"""
        if not self.armature:
            return

        # Ensure we're in pose mode
        if self.armature.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')

        # Get the pose data
        pose = self.armature.pose

        if pose_landmarks:
            self.process_pose_landmarks(pose_landmarks)
        if face_landmarks:
            self.process_face_landmarks(face_landmarks)
        # Ensure hand landmarks are processed if available
        if left_hand_landmarks:
            self.process_hand_landmarks(left_hand_landmarks, is_right_hand=False)
        if right_hand_landmarks:
            self.process_hand_landmarks(right_hand_landmarks, is_right_hand=True)
        
        # Get current frame
        current_frame = bpy.context.scene.frame_current
        
        # Update the pose using quaternions and insert keyframes
        for bone in pose.bones:
            quat = bone.rotation_quaternion
            bone.rotation_quaternion = quat
            bone.keyframe_insert(data_path="rotation_quaternion", frame=current_frame)
        
        bpy.context.view_layer.update()
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw() 
                    