import bpy
from bpy.props import BoolProperty, PointerProperty, StringProperty, EnumProperty
from bpy.types import PropertyGroup

class AniMateProperties(PropertyGroup):
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
        default=False
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
    #new code
    source_type: EnumProperty(
        name="Source Type",
        description="Select the input sourec formotion capture",
        items=[
            ('WEBCAM',"Webcam","Use live webcam feed"),
            ('IMAGE',"Image File","Use a static image file from the disk"),
            ('VIDEO',"Video File","Use a video file from the disk")
        ],
        default='WEBCAM'
    )

    image_filepath: StringProperty(
        name='Image File',
        description='Path to the image file for capture',
        subtype='FILE_PATH'
    )

    video_filepath: StringProperty(
        name='Video File',
        description='Path to the video file for capture',
        subtype='FILE_PATH'
    )