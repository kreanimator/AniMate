"""
Blender rig mapper for motion capture.
"""
import bpy
import math
from mathutils import Vector, Matrix, Euler
from .mappings.mapping_factory import RigMappingFactory

class BlenderRigMapper:
    def __init__(self, armature_obj=None, rig_type='MIXAMO'):
        self.armature = armature_obj
        self.pose_bones = {}
        self.previous_rotations = {}
        self.mapping = RigMappingFactory.create_mapping(rig_type)
        if armature_obj:
            self.setup_armature(armature_obj)

    def setup_armature(self, armature_obj):
        """Initialize the armature and store references to bones"""
        self.armature = armature_obj
        if not self.armature or self.armature.type != 'ARMATURE':
            raise ValueError("Invalid armature object")
        
        # Store pose bones for quick access
        self.pose_bones = {bone.name: bone for bone in self.armature.pose.bones}
        
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
            return

        # Convert landmarks to world space coordinates
        world_coords = {}
        for i, landmark in enumerate(landmarks.landmark):
            # Convert from MediaPipe's coordinate system to Blender's
            world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))

        # Get pose mapping for this rig type
        pose_mapping = self.mapping.get_pose_mapping()
        
        # Process each mapped bone
        for bone_name, landmark_indices in pose_mapping.items():
            if bone_name not in self.pose_bones:
                continue

            bone = self.pose_bones[bone_name]
            
            # Calculate bone orientation from landmarks
            if len(landmark_indices) == 2:
                start_point = world_coords[landmark_indices[0]]
                end_point = world_coords[landmark_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                
                # Apply rotation limits
                rotation = self.apply_rotation_limits(bone_name, rotation)
                
                # Apply scale factor
                scale_factor = self.mapping.get_bone_scale_factors().get(bone_name, 1.0)
                rotation = Euler((rotation.x * scale_factor, 
                                rotation.y * scale_factor, 
                                rotation.z * scale_factor))
            else:
                # Handle special cases (like single-point landmarks)
                continue

            # Apply rotation with smoothing
            if bone_name in self.previous_rotations:
                smoothing = 0.5  # Adjust smoothing factor as needed
                rotation = Euler((
                    self.lerp(self.previous_rotations[bone_name].x, rotation.x, smoothing),
                    self.lerp(self.previous_rotations[bone_name].y, rotation.y, smoothing),
                    self.lerp(self.previous_rotations[bone_name].z, rotation.z, smoothing)
                ))

            # Store rotation for next frame
            self.previous_rotations[bone_name] = rotation
            
            # Apply rotation to bone
            bone.rotation_euler = rotation

    def process_face_landmarks(self, landmarks):
        """Process face landmarks and apply to face rig/shape keys"""
        if not landmarks:
            return
        
        # Get face mapping for this rig type
        face_mapping = self.mapping.get_face_mapping()
        
        # Process each mapped face bone
        for bone_name, landmark_indices in face_mapping.items():
            if bone_name not in self.pose_bones:
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
                self.pose_bones[bone_name].rotation_euler = rotation

    def process_hand_landmarks(self, landmarks, is_right_hand=True):
        """Process hand landmarks and apply to hand rig"""
        if not landmarks:
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
            if bone_name not in self.pose_bones:
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
                self.pose_bones[bone_name].rotation_euler = rotation

    @staticmethod
    def lerp(a, b, t):
        """Linear interpolation between two values"""
        return a + (b - a) * t

    def update_rig(self, pose_landmarks=None, face_landmarks=None, left_hand_landmarks=None, right_hand_landmarks=None):
        """Update the entire rig with new landmark data"""
        if pose_landmarks:
            self.process_pose_landmarks(pose_landmarks)
        if face_landmarks:
            self.process_face_landmarks(face_landmarks)
        if left_hand_landmarks:
            self.process_hand_landmarks(left_hand_landmarks, is_right_hand=False)
        if right_hand_landmarks:
            self.process_hand_landmarks(right_hand_landmarks, is_right_hand=True)
        
        # Ensure the viewport updates
        bpy.context.view_layer.update() 