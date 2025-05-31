import bpy
from mathutils import Vector, Matrix, Euler

class RigRetargeting:
    """Handle retargeting between different rig structures"""
    
    # Common bone naming conventions
    BONE_NAMING_CONVENTIONS = {
        'mixamo': {
            'hips': 'Hips',
            'spine': 'Spine',
            'neck': 'Neck',
            'head': 'Head',
            'left_shoulder': 'LeftShoulder',
            'left_upper_arm': 'LeftArm',
            'left_lower_arm': 'LeftForeArm',
            'left_hand': 'LeftHand',
            'right_shoulder': 'RightShoulder',
            'right_upper_arm': 'RightArm',
            'right_lower_arm': 'RightForeArm',
            'right_hand': 'RightHand',
            'left_upper_leg': 'LeftUpLeg',
            'left_lower_leg': 'LeftLeg',
            'left_foot': 'LeftFoot',
            'right_upper_leg': 'RightUpLeg',
            'right_lower_leg': 'RightLeg',
            'right_foot': 'RightFoot'
        },
        'rigify': {
            'hips': 'spine',
            'spine': 'spine.001',
            'neck': 'spine.004',
            'head': 'spine.006',
            'left_shoulder': 'shoulder.L',
            'left_upper_arm': 'upper_arm.L',
            'left_lower_arm': 'forearm.L',
            'left_hand': 'hand.L',
            'right_shoulder': 'shoulder.R',
            'right_upper_arm': 'upper_arm.R',
            'right_lower_arm': 'forearm.R',
            'right_hand': 'hand.R',
            'left_upper_leg': 'thigh.L',
            'left_lower_leg': 'shin.L',
            'left_foot': 'foot.L',
            'right_upper_leg': 'thigh.R',
            'right_lower_leg': 'shin.R',
            'right_foot': 'foot.R'
        },
        # Add more conventions as needed
    }

    def __init__(self):
        self.source_armature = None
        self.target_armature = None
        self.bone_mapping = {}
        self.rest_poses = {}

    def detect_rig_type(self, armature):
        """Attempt to automatically detect the rig type based on bone names"""
        if not armature or armature.type != 'ARMATURE':
            return None
            
        bone_names = set(bone.name for bone in armature.pose.bones)
        
        # Check against known conventions
        for rig_type, naming in self.BONE_NAMING_CONVENTIONS.items():
            matches = sum(1 for bone in naming.values() if bone in bone_names)
            if matches > len(naming) * 0.7:  # If more than 70% match
                return rig_type
                
        return 'custom'

    def setup_retargeting(self, source_armature, target_armature):
        """Setup retargeting between two armatures"""
        self.source_armature = source_armature
        self.target_armature = target_armature
        
        # Detect rig types
        source_type = self.detect_rig_type(source_armature)
        target_type = self.detect_rig_type(target_armature)
        
        # Create bone mapping
        self.create_bone_mapping(source_type, target_type)
        
        # Store rest poses
        self.store_rest_poses()

    def create_bone_mapping(self, source_type, target_type):
        """Create mapping between source and target bones"""
        self.bone_mapping.clear()
        
        if source_type in self.BONE_NAMING_CONVENTIONS and target_type in self.BONE_NAMING_CONVENTIONS:
            source_names = self.BONE_NAMING_CONVENTIONS[source_type]
            target_names = self.BONE_NAMING_CONVENTIONS[target_type]
            
            # Create mapping between corresponding bones
            for generic_name in source_names.keys():
                source_bone = source_names[generic_name]
                target_bone = target_names[generic_name]
                
                if (source_bone in self.source_armature.pose.bones and 
                    target_bone in self.target_armature.pose.bones):
                    self.bone_mapping[source_bone] = target_bone

    def store_rest_poses(self):
        """Store rest pose transforms for both armatures"""
        self.rest_poses = {
            'source': {},
            'target': {}
        }
        
        # Store source armature rest poses
        for bone in self.source_armature.pose.bones:
            self.rest_poses['source'][bone.name] = {
                'matrix': bone.matrix.copy(),
                'head': bone.head.copy(),
                'tail': bone.tail.copy()
            }
            
        # Store target armature rest poses
        for bone in self.target_armature.pose.bones:
            self.rest_poses['target'][bone.name] = {
                'matrix': bone.matrix.copy(),
                'head': bone.head.copy(),
                'tail': bone.tail.copy()
            }

    def retarget_pose(self, bone_name, rotation):
        """Retarget pose from source to target bones"""
        if bone_name not in self.bone_mapping:
            return None
            
        target_bone_name = self.bone_mapping[bone_name]
        target_bone = self.target_armature.pose.bones[target_bone_name]
        
        # Get rest poses
        source_rest = self.rest_poses['source'][bone_name]
        target_rest = self.rest_poses['target'][target_bone_name]
        
        # Calculate relative rotation
        source_rest_mat = source_rest['matrix']
        target_rest_mat = target_rest['matrix']
        
        # Create rotation matrix from euler
        rot_mat = rotation.to_matrix().to_4x4()
        
        # Calculate final rotation
        final_rot = target_rest_mat.inverted() @ source_rest_mat @ rot_mat @ source_rest_mat.inverted() @ target_rest_mat
        
        return final_rot.to_euler()

    def apply_pose(self, bone_rotations):
        """Apply retargeted pose to target armature"""
        for bone_name, rotation in bone_rotations.items():
            retargeted_rotation = self.retarget_pose(bone_name, rotation)
            if retargeted_rotation:
                target_bone_name = self.bone_mapping[bone_name]
                self.target_armature.pose.bones[target_bone_name].rotation_euler = retargeted_rotation
        
        # Update the viewport
        bpy.context.view_layer.update() 