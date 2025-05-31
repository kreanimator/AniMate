bl_info = {
    "name": "AniMate Motion Capture",
    "author": "Valentin Bakin",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AniMate",
    "description": "Real-time motion capture using webcam",
    "category": "Animation",
}

import bpy
from bpy.props import BoolProperty, FloatProperty
import cv2
import mediapipe as mp
import threading
import time
from mathutils import Vector, Euler

class ANIMATE_OT_start_capture(bpy.types.Operator):
    bl_idname = "animate.start_capture"
    bl_label = "Start Capture"
    bl_description = "Start motion capture from webcam"
    
    _timer = None
    _capture_thread = None
    _running = False
    _pose_data = None
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            if self._pose_data:
                self.apply_pose(context, self._pose_data)
            
        if not self._running:
            self.cleanup(context)
            return {'CANCELLED'}
            
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        self._running = True
        
        # Add timer for modal
        wm = context.window_manager
        self._timer = wm.event_timer_add(1.0 / 30.0, window=context.window)
        wm.modal_handler_add(self)
        
        # Start capture thread
        self._capture_thread = threading.Thread(target=self.capture_thread)
        self._capture_thread.daemon = True
        self._capture_thread.start()
        
        return {'RUNNING_MODAL'}
    
    def cleanup(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        self._timer = None
        self._running = False
        return {'CANCELLED'}
    
    def capture_thread(self):
        # Initialize MediaPipe
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Start video capture
        cap = cv2.VideoCapture(0)
        
        while self._running:
            success, image = cap.read()
            if not success:
                continue
                
            # Process image
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            
            if results.pose_landmarks:
                self._pose_data = results.pose_landmarks
        
        cap.release()
        pose.close()
    
    def apply_pose(self, context, pose_data):
        # Get the active armature
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return
            
        # Simple bone mapping (just hips and spine for now)
        bone_mapping = {
            'spine': ([23, 24], [11, 12]),  # hips to shoulders
            'neck': ([11, 12], [0]),       # shoulders to nose
        }
        
        for bone_name, (start_ids, end_ids) in bone_mapping.items():
            if bone_name not in armature.pose.bones:
                continue
                
            # Calculate average positions
            start_pos = Vector((0, 0, 0))
            end_pos = Vector((0, 0, 0))
            
            # Average start points
            for idx in start_ids:
                landmark = pose_data.landmark[idx]
                start_pos += Vector((landmark.x, landmark.y, landmark.z))
            start_pos /= len(start_ids)
            
            # Average end points
            for idx in end_ids:
                landmark = pose_data.landmark[idx]
                end_pos += Vector((landmark.x, landmark.y, landmark.z))
            end_pos /= len(end_ids)
            
            # Calculate bone direction
            direction = (end_pos - start_pos).normalized()
            
            # Apply simple rotation
            bone = armature.pose.bones[bone_name]
            bone.rotation_euler = direction.to_track_quat('-Y', 'Z').to_euler()

class ANIMATE_PT_motion_capture(bpy.types.Panel):
    bl_label = "AniMate Motion Capture"
    bl_idname = "ANIMATE_PT_motion_capture"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AniMate'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("animate.start_capture", text="Start Capture")
        layout.operator("animate.stop_capture", text="Stop Capture")

class ANIMATE_OT_stop_capture(bpy.types.Operator):
    bl_idname = "animate.stop_capture"
    bl_label = "Stop Capture"
    bl_description = "Stop motion capture"
    
    def execute(self, context):
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for operator in area.operator_properties:
                        if operator.bl_idname == "animate.start_capture":
                            operator._running = False
                            break
        return {'FINISHED'}

classes = (
    ANIMATE_OT_start_capture,
    ANIMATE_OT_stop_capture,
    ANIMATE_PT_motion_capture,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register() 