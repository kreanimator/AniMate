import bpy
import math
from mathutils import Vector, Matrix, Euler

class BlenderRigMapper:
    # MediaPipe pose landmarks to Blender bone mapping
    POSE_LANDMARKS_TO_BONES = {
        # Torso
        'hips': [23, 24],           # Left and right hip
        'spine': [11, 12],          # Left and right shoulder
        'neck': [11, 12],           # Shoulders midpoint to head
        'head': [0],                # Nose
        
        # Arms
        'left_shoulder': [11],
        'left_upper_arm': [11, 13],
        'left_lower_arm': [13, 15],
        'left_hand': [15, 17],
        
        'right_shoulder': [12],
        'right_upper_arm': [12, 14],
        'right_lower_arm': [14, 16],
        'right_hand': [16, 18],
        
        # Legs
        'left_upper_leg': [23, 25],
        'left_lower_leg': [25, 27],
        'left_foot': [27, 31],
        
        'right_upper_leg': [24, 26],
        'right_lower_leg': [26, 28],
        'right_foot': [28, 32]
    }

    # MediaPipe face landmarks to Blender shape keys/bones
    FACE_LANDMARKS_TO_BONES = {
        'jaw': [0, 17, 57, 287],  # Jaw opening
        'mouth_left': [61, 291],   # Mouth corner L
        'mouth_right': [291, 61],  # Mouth corner R
        'eyebrow_left': [70, 63, 105, 66, 107],  # Left eyebrow
        'eyebrow_right': [336, 296, 334, 293, 300]  # Right eyebrow
    }

    # MediaPipe hand landmarks to Blender finger bones
    HAND_LANDMARKS_TO_BONES = {
        'thumb': [1, 2, 3, 4],
        'index': [5, 6, 7, 8],
        'middle': [9, 10, 11, 12],
        'ring': [13, 14, 15, 16],
        'pinky': [17, 18, 19, 20]
    }

    def __init__(self, armature_obj=None):
        self.armature = armature_obj
        self.pose_bones = {}
        self.previous_rotations = {}
        if armature_obj:
            self.setup_armature(armature_obj)

    def setup_armature(self, armature_obj):
        """Initialize the armature and store references to bones"""
        self.armature = armature_obj
        if not self.armature or self.armature.type != 'ARMATURE':
            raise ValueError("Invalid armature object")
        
        # Store pose bones for quick access
        self.pose_bones = {bone.name: bone for bone in self.armature.pose.bones}

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

    def process_pose_landmarks(self, landmarks):
        """Process pose landmarks and apply to armature"""
        if not self.armature or not landmarks:
            return

        # Convert landmarks to world space coordinates
        world_coords = {}
        for i, landmark in enumerate(landmarks):
            # Convert from MediaPipe's coordinate system to Blender's
            world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))

        # Process each mapped bone
        for bone_name, landmark_indices in self.POSE_LANDMARKS_TO_BONES.items():
            if bone_name not in self.pose_bones:
                continue

            bone = self.pose_bones[bone_name]
            
            # Calculate bone orientation from landmarks
            if len(landmark_indices) == 2:
                start_point = world_coords[landmark_indices[0]]
                end_point = world_coords[landmark_indices[1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
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
        
        # Implementation will depend on your face rig setup
        pass

    def process_hand_landmarks(self, landmarks, is_right_hand=True):
        """Process hand landmarks and apply to hand rig"""
        if not landmarks:
            return
            
        prefix = "right_" if is_right_hand else "left_"
        
        # Convert landmarks to world space
        world_coords = {}
        for i, landmark in enumerate(landmarks):
            world_coords[i] = Vector((landmark.x, -landmark.z, landmark.y))
            
        # Process each finger
        for finger_name, joint_indices in self.HAND_LANDMARKS_TO_BONES.items():
            for i in range(len(joint_indices) - 1):
                bone_name = f"{prefix}{finger_name}_{i}"
                if bone_name not in self.pose_bones:
                    continue
                    
                start_point = world_coords[joint_indices[i]]
                end_point = world_coords[joint_indices[i + 1]]
                rotation = self.calculate_bone_rotation(start_point, end_point)
                
                # Apply rotation to finger bone
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