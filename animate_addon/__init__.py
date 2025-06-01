"""
AniMate - Blender Motion Capture Addon
"""

import sys
import site
# Remove user site-packages from sys.path to avoid confusion
if hasattr(site, 'getusersitepackages'):
    user_site = site.getusersitepackages()
    if user_site in sys.path:
        sys.path.remove(user_site)

import subprocess
# TODO: Need to find a way to automatically install dependencies with plugin
def ensure_package(package, import_name=None):
    try:
        if import_name is None:
            import_name = package
        __import__(import_name)
    except ImportError:
        python_exe = sys.executable
        try:
            subprocess.check_call([python_exe, "-m", "pip", "install", package])
            # Try importing again after install
            if import_name in sys.modules:
                del sys.modules[import_name]
            __import__(import_name)
        except Exception as e:
            print(f"[AniMate] Failed to install or import {package}: {e}")
            raise

# Ensure all required packages at the very top, before any other imports
ensure_package("packaging")
ensure_package("opencv-python", "cv2")
ensure_package("mediapipe")

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

# Now import everything else
import math
import bpy
from bpy.props import (
    BoolProperty,
    PointerProperty,
    StringProperty,
    EnumProperty
)
from bpy.types import (
    Panel,
    Operator,
    PropertyGroup,
    ImageUser
)
from threading import Thread
import time
import bpy.utils.previews
import bpy.app.timers
import cv2
import mediapipe as mp
import numpy as np

def get_rig_types(self, context):
    return [
        ('MIXAMO', 'Mixamo', 'Mixamo Rig'),
        ('RIGIFY', 'Rigify', 'Blender Rigify Rig'),
        ('MAYA', 'Maya', 'Maya Rig'),
        # Add more rig types here in the future
    ]

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
    rig_type: EnumProperty(
        name="Rig Type",
        description="Type of rig to use",
        items=[
            ('MIXAMO', 'Mixamo', 'Mixamo Rig'),
            ('RIGIFY', 'Rigify', 'Blender Rigify Rig'),
            ('MAYA', 'Maya', 'Maya Rig'),
        ],
        default='MIXAMO'
    )
    camera_preview_running: BoolProperty(
        name="Camera Preview Running",
        description="Is the camera preview running?",
        default=False
    )
    camera_preview_image: StringProperty(
        name="Camera Preview Image",
        description="Name of the Blender image datablock for preview",
        default="AniMateCameraPreview"
    )

class DummyImageUser:
    frame_current = 1

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

        # Rig type dropdown
        layout.prop(props, "rig_type")

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

class ANIMATE_PT_camera_preview(Panel):
    bl_label = "Camera Preview"
    bl_idname = "ANIMATE_PT_camera_preview"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AniMate'
    bl_parent_id = 'ANIMATE_PT_main_panel'

    def draw(self, context):
        layout = self.layout
        props = context.scene.animate_properties
        row = layout.row()
        if not props.camera_preview_running:
            row.operator("animate.start_camera_preview", text="Start Camera Preview")
        else:
            row.operator("animate.stop_camera_preview", text="Stop Camera Preview")
        layout.label(text="The live camera feed will appear on a plane in the 3D View.")
        layout.label(text="Switch to Material Preview or Rendered view to see it.")
        layout.label(text="You can move/scale the plane as needed.")

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

class ANIMATE_OT_start_camera_preview(Operator):
    bl_idname = "animate.start_camera_preview"
    bl_label = "Start Camera Preview"
    bl_description = "Start the camera preview and show it on a plane in the 3D View"

    _timer = None
    _cap = None
    _img_name = "AniMateCameraPreview"
    _plane_name = "AniMateCameraPlane"
    _mat_name = "AniMateCameraMaterial"

    def modal(self, context, event):
        if not context.scene.animate_properties.camera_preview_running:
            self.cancel(context)
            return {'CANCELLED'}
        if event.type == 'TIMER':
            ret, frame = self._cap.read()
            if not ret or frame is None:
                print("[AniMate] Failed to read frame from camera.")
                return {'PASS_THROUGH'}
            frame = cv2.flip(frame, 0)  # Flip vertically for Blender
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            # Draw MediaPipe landmarks
            props = context.scene.animate_properties
            if not hasattr(self, 'mp_pose'):
                self.mp_pose = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
                self.mp_face = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, min_detection_confidence=0.5)
                self.mp_hands = mp.solutions.hands.Hands(static_image_mode=False, min_detection_confidence=0.5)
                self.mp_drawing = mp.solutions.drawing_utils
                self.mp_drawing_styles = mp.solutions.drawing_styles
            results_pose = results_face = results_hands = None
            if props.enable_pose:
                results_pose = self.mp_pose.process(frame)
                if results_pose.pose_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        results_pose.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS,
                        self.mp_drawing_styles.get_default_pose_landmarks_style())
            if props.enable_face:
                results_face = self.mp_face.process(frame)
                if results_face.multi_face_landmarks:
                    for face_landmarks in results_face.multi_face_landmarks:
                        self.mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            self.mp_face.FACEMESH_TESSELATION,
                            self.mp_drawing_styles.get_default_face_mesh_tesselation_style())
            if props.enable_hands:
                results_hands = self.mp_hands.process(frame)
                if results_hands.multi_hand_landmarks:
                    for hand_landmarks in results_hands.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style())
            # Add alpha channel
            h, w, _ = frame.shape
            alpha = np.ones((h, w, 1), dtype=np.uint8) * 255
            frame_rgba = np.concatenate((frame, alpha), axis=2)
            frame_flat = (frame_rgba / 255.0).astype(np.float32).flatten()
            img = bpy.data.images.get(self._img_name)
            if img and len(frame_flat) == img.size[0] * img.size[1] * img.channels:
                img.pixels = frame_flat.tolist()
                img.update()
        return {'PASS_THROUGH'}

    def execute(self, context):
        if not hasattr(sys.modules[__name__], 'np'):
            import numpy as np
            sys.modules[__name__].np = np
        props = context.scene.animate_properties
        if props.camera_preview_running:
            self.report({'WARNING'}, "Camera preview already running.")
            return {'CANCELLED'}
        props.camera_preview_running = True
        # Open camera
        self._cap = cv2.VideoCapture(0)
        if not self._cap.isOpened():
            self.report({'ERROR'}, "Could not open camera.")
            props.camera_preview_running = False
            return {'CANCELLED'}
        # Create Blender image datablock if needed
        if self._img_name not in bpy.data.images:
            bpy.data.images.new(self._img_name, width=640, height=480, alpha=True, float_buffer=True)
        img = bpy.data.images[self._img_name]
        img.generated_width = 640
        img.generated_height = 480
        img.colorspace_settings.name = 'sRGB'
        # Create plane if not present
        if self._plane_name not in bpy.data.objects:
            bpy.ops.mesh.primitive_plane_add(size=4, location=(0, -2, 1))
            plane = context.active_object
            plane.name = self._plane_name
            plane.rotation_euler = (math.radians(90), 0, 0)
        else:
            plane = bpy.data.objects[self._plane_name]
            plane.location = (0, -2, 1)
            plane.rotation_euler = (math.radians(90), 0, 0)
        # Create material if not present
        if self._mat_name not in bpy.data.materials:
            mat = bpy.data.materials.new(self._mat_name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get('Principled BSDF')
            tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
            tex_image.image = img
            mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
        else:
            mat = bpy.data.materials[self._mat_name]
            # Update image node if needed
            tex_image = None
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    tex_image = node
                    break
            if tex_image is None:
                tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
                bsdf = mat.node_tree.nodes.get('Principled BSDF')
                mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
            tex_image.image = img
        # Assign material to plane
        if plane.data.materials:
            plane.data.materials[0] = mat
        else:
            plane.data.materials.append(mat)
        # Add modal timer
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.03, window=context.window)
        wm.modal_handler_add(self)
        self.report({'INFO'}, "Camera preview started. Switch to Material Preview or Rendered view to see the feed on the plane.")
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        props = context.scene.animate_properties
        props.camera_preview_running = False
        if self._cap:
            self._cap.release()
        wm = context.window_manager
        if self._timer:
            wm.event_timer_remove(self._timer)
        self._timer = None
        self._cap = None
        self.report({'INFO'}, "Camera preview stopped.")
        return {'CANCELLED'}

class ANIMATE_OT_stop_camera_preview(Operator):
    bl_idname = "animate.stop_camera_preview"
    bl_label = "Stop Camera Preview"
    bl_description = "Stop the camera preview"

    def execute(self, context):
        context.scene.animate_properties.camera_preview_running = False
        return {'FINISHED'}

classes = (
    AniMateProperties,
    ANIMATE_PT_main_panel,
    ANIMATE_PT_camera_preview,
    ANIMATE_OT_start_capture,
    ANIMATE_OT_stop_capture,
    ANIMATE_OT_start_camera_preview,
    ANIMATE_OT_stop_camera_preview,
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