"""
AniMate - Blender Motion Capture Addon
"""

bl_info = {
    "name": "AniMate",
    "author": "Valentin Bakin",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AniMate",
    "description": "Motion capture and animation using MediaPipe",
    "warning": "Under development",
    "doc_url": "",
    "category": "Animation",
}

import bpy
from bpy.props import (
    BoolProperty,
    PointerProperty,
    StringProperty
)
from bpy.types import (
    Panel,
    Operator,
    PropertyGroup
)

class AniMateProperties(PropertyGroup):
    """Properties for the AniMate addon."""
    enable_pose: BoolProperty(
        name="Enable Pose",
        description="Enable pose detection",
        default=True
    )
    enable_face: BoolProperty(
        name="Enable Face",
        description="Enable face detection",
        default=True
    )
    enable_hands: BoolProperty(
        name="Enable Hands",
        description="Enable hand detection",
        default=True
    )
    target_armature: PointerProperty(
        name="Target Armature",
        description="Armature to animate",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )

class ANIMATE_PT_main_panel(Panel):
    """Main panel for AniMate."""
    bl_label = "AniMate"
    bl_idname = "ANIMATE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AniMate'

    def draw(self, context):
        layout = self.layout
        props = context.scene.animate_properties

        # Armature selection
        layout.prop(props, "target_armature")

        # Detection toggles
        box = layout.box()
        box.label(text="Detection Settings:")
        box.prop(props, "enable_pose")
        box.prop(props, "enable_face")
        box.prop(props, "enable_hands")

        # Start/Stop capture
        row = layout.row()
        if not context.scene.animate_running:
            row.operator("animate.start_capture", text="Start Capture")
        else:
            row.operator("animate.stop_capture", text="Stop Capture")

class ANIMATE_OT_start_capture(Operator):
    """Start motion capture."""
    bl_idname = "animate.start_capture"
    bl_label = "Start Capture"
    bl_description = "Start motion capture"

    def execute(self, context):
        # TODO: Implement capture start
        context.scene.animate_running = True
        return {'FINISHED'}

class ANIMATE_OT_stop_capture(Operator):
    """Stop motion capture."""
    bl_idname = "animate.stop_capture"
    bl_label = "Stop Capture"
    bl_description = "Stop motion capture"

    def execute(self, context):
        # TODO: Implement capture stop
        context.scene.animate_running = False
        return {'FINISHED'}

classes = (
    AniMateProperties,
    ANIMATE_PT_main_panel,
    ANIMATE_OT_start_capture,
    ANIMATE_OT_stop_capture,
)

def register():
    """Register the addon."""
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.animate_properties = PointerProperty(type=AniMateProperties)
    bpy.types.Scene.animate_running = BoolProperty(default=False)

def unregister():
    """Unregister the addon."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.animate_properties
    del bpy.types.Scene.animate_running

if __name__ == "__main__":
    register() 