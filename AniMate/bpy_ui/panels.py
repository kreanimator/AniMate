import bpy
from bpy.types import Panel
from .properties import AniMateProperties

def split_and_set_image_editor(img_name):
    window = bpy.context.window
    screen = window.screen
    # Join all areas into the largest one
    areas = list(screen.areas)
    if len(areas) > 1:
        main_area = max(areas, key=lambda a: a.width * a.height)
        for area in areas:
            if area != main_area:
                override = {'window': window, 'area': area}
                try:
                    bpy.ops.screen.area_join(override, min_x=main_area.x, min_y=main_area.y, max_x=area.x, max_y=area.y)
                except Exception as e:
                    print(f"[AniMate] Area join failed: {e}")
    # Now only one area, split it by calling the operator directly
    try:
        bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)
        areas = sorted(screen.areas, key=lambda a: a.x)
        left_area, right_area = areas[0], areas[1]
        left_area.type = 'IMAGE_EDITOR'
        for space in left_area.spaces:
            if space.type == 'IMAGE_EDITOR':
                space.image = bpy.data.images[img_name]
                break
        right_area.type = 'VIEW_3D'
    except Exception as e:
        print(f"[AniMate] Area split failed: {e}. Switching largest area to IMAGE_EDITOR.")
        max_area = max(screen.areas, key=lambda a: a.width * a.height)
        max_area.type = 'IMAGE_EDITOR'
        for space in max_area.spaces:
            if space.type == 'IMAGE_EDITOR':
                space.image = bpy.data.images[img_name]
                break
    return None  # Only run once

class AniMateMainPanel(Panel):
    bl_label = "AniMate"
    bl_idname = "ANIMATE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AniMate'

    def draw(self, context):
        layout = self.layout
        props = context.scene.animate_properties
        layout.prop(props, "rig_type")
        layout.prop(props, "target_armature")
        box = layout.box()
        box.label(text="Detection Settings:")
        box.prop(props, "enable_pose")
        box.prop(props, "enable_face")
        box.prop(props, "enable_hands")
        box.prop(props, "camera_mirrored")
        box.prop(props, "show_camera_preview")
        layout.separator()
        row = layout.row()
        if getattr(context.scene, 'animate_running', False):
            row.operator("animate.stop_capture", text="Stop Capture", icon='CANCEL')
        else:
            row.operator("animate.start_capture", text="Start Capture", icon='REC') 