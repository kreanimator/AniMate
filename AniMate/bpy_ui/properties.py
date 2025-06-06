import bpy
from bpy.props import BoolProperty, PointerProperty, StringProperty, EnumProperty
from bpy.types import PropertyGroup

class AniMateProperties(PropertyGroup):
    debug_mode: BoolProperty(
        name="Debug Mode",
        description="Enable debug output in console",
        default=False
    )
    enable_pose: BoolProperty(
        name="Enable Pose",
        description="Enable pose detection",
        default=True
    )
    enable_face: BoolProperty(
        name="Enable Face",
        description="Enable face detection",
        default=False
    )
    enable_hands: BoolProperty(
        name="Enable Hands",
        description="Enable hand detection",
        default=True
    )
    show_camera_preview: BoolProperty(
        name="Show Camera Preview",
        description="Show the camera preview in the Image Editor",
        default=True
    )
    camera_mirrored: BoolProperty(
        name="Camera Mirrored",
        description="Is the camera preview mirrored? (Flip X coordinates)",
        default=True
    )
    target_armature: PointerProperty(
        name="Target Armature",
        description="Armature to animate",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    rig_type: EnumProperty(
        name="Rig Type",
        description="Type of rig to use",
        items=[
            ('MIXAMO', 'Mixamo', 'Mixamo Rig'),
            ('RIGIFY', 'Rigify', 'Blender Rigify Rig'),
            ('MAYA', 'Maya', 'Maya Rig'),
        ],
        default='MIXAMO',
    )
    animate_last_workspace: StringProperty(
        name="Last Workspace",
        description="Workspace to restore after capture",
        default=""
    ) 
