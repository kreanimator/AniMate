from .__dev_build__ import __dev_build__
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
bl_info["description"] += f" (Build: {__dev_build__}) | GitHub: https://github.com/kreanimator/AniMate | Docs: https://docs.sosw.app/contribution/index.html"


import bpy
from .bpy_ui.panels import AniMateMainPanel
from .bpy_ui.operators import (
    ANIMATE_OT_start_capture,
    ANIMATE_OT_stop_capture,
)
from .bpy_ui.properties import AniMateProperties

classes = (
    AniMateProperties,
    AniMateMainPanel,
    ANIMATE_OT_start_capture,
    ANIMATE_OT_stop_capture,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.animate_properties = bpy.props.PointerProperty(type=AniMateProperties)
    bpy.types.Scene.animate_running = bpy.props.BoolProperty(default=False)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.animate_properties
    if hasattr(bpy.types.Scene, 'animate_running'):
        del bpy.types.Scene.animate_running

if __name__ == "__main__":
    register() 