import bpy
from bpy.types import Operator
import cv2
import mediapipe as mp
import numpy as np
from ..rig.blender_mapper import BlenderRigMapper
from .panels import split_and_set_image_editor
from ..utils.math_utils import mediapipe_to_blender_coords, mediapipe_to_blender_coords_pose

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class ANIMATE_OT_start_capture(Operator):
    """
    Start real-time motion capture and apply results to the selected rig.
    """
    bl_idname = "animate.start_capture"
    bl_label = "Start Capture"
    bl_description = "Start motion capture"

    _timer = None
    _cap = None
    _mapper = None
    mp_pose = None
    mp_face = None
    mp_hands = None

    def execute(self, context):
        props = context.scene.animate_properties
        if getattr(context.scene, 'animate_running', False):
            self.report({'WARNING'}, "Motion capture already running.")
            return {'CANCELLED'}
        # Check if we have a valid armature
        if not props.target_armature:
            self.report({'ERROR'}, "No armature selected. Please select a target armature.")
            return {'CANCELLED'}
        if props.target_armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Selected object is not an armature.")
            return {'CANCELLED'}

        # Initialize MediaPipe solutions (these are common for all sources, so they stay here)
        self.mp_pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_face = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Initialize the rig mapper (this is also common for all sources, so it stays here)
        self._mapper = BlenderRigMapper(props.target_armature, rig_type=props.rig_type)
        self._mapper.driver_manager.create_drivers()
        self._mapper.scan_rig()
        self._mapper.initialize_rig()
        self._mapper.store_original_pose()

        # --- Start Source Type Conditional Logic ---
        # This is where the 'if/elif/else' structure goes, based on props.source_type
        if props.source_type == 'WEBCAM':
            # This is your original webcam logic, now indented under 'if WEBCAM'
            print("[AniMate] Starting webcam capture...")

            self._cap = cv2.VideoCapture(0)
            if not self._cap.isOpened():
                self.report({'ERROR'}, "Could not open camera.")
                return {'CANCELLED'}
            # Create Blender image datablock if needed
            if "AniMateCameraPreview" not in bpy.data.images:
                bpy.data.images.new("AniMateCameraPreview", width=640, height=480, alpha=True, float_buffer=True, is_data=True)
            img = bpy.data.images["AniMateCameraPreview"]
            img.generated_width = 640
            img.generated_height = 480
            img.colorspace_settings.name = 'sRGB'
            img.use_fake_user = True
            # Split the view and set up the preview if enabled
            if props.show_camera_preview:
                split_and_set_image_editor("AniMateCameraPreview")
            context.scene.animate_running = True
            wm = context.window_manager
            self._timer = wm.event_timer_add(1/30, window=context.window)
            wm.modal_handler_add(self)
            self.report({'INFO'}, "Capture started")
            print("[AniMate] Capture started, modal operator running.")
            return {'RUNNING_MODAL'}

        elif props.source_type == 'IMAGE':
            print(f"[AniMate] Processing image: {props.image_filepath}")
            if not props.image_filepath:
                self.report({'ERROR'}, "No image file selected.")
                return {'CANCELLED'}

            try:
                image_bgr = cv2.imread(props.image_filepath)
                if image_bgr is None:
                    self.report({'ERROR'}, f"Failed to load image: {props.image_filepath}. Check path or file corruption.")
                    return {'CANCELLED'}

                # Convert to RGB, which MediaPipe expects
                image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

                # Create MediaPipe Image object
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

               
                print("[AniMate] Image processing placeholder executed.")

                self.report({'INFO'}, "Image processed successfully (placeholder).")
                return {'FINISHED'} # For image, we process once and finish

            except Exception as e:
                self.report({'ERROR'}, f"Error processing image: {e}")
                return {'CANCELLED'}

        elif props.source_type == 'VIDEO':
            print(f"[AniMate] Processing video: {props.video_filepath}")
            if not props.video_filepath:
                self.report({'ERROR'}, "No video file selected.")
                return {'CANCELLED'}

            try:
                self._cap = cv2.VideoCapture(props.video_filepath)
                if not self._cap.isOpened():
                    self.report({'ERROR'}, f"Failed to open video: {props.video_filepath}. Check path or file format.")
                    return {'CANCELLED'}

                # Similar to webcam, video processing is continuous, so setup modal
                # Create Blender image datablock if needed (for video preview)
                if "AniMateCameraPreview" not in bpy.data.images:
                    bpy.data.images.new("AniMateCameraPreview", width=640, height=480, alpha=True, float_buffer=True, is_data=True)
                img = bpy.data.images["AniMateCameraPreview"]
                img.generated_width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                img.generated_height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                img.colorspace_settings.name = 'sRGB'
                img.use_fake_user = True
                if props.show_camera_preview:
                    split_and_set_image_editor("AniMateCameraPreview")

                context.scene.animate_running = True
                wm = context.window_manager
                self._timer = wm.event_timer_add(1/30, window=context.window) # Adjust timer for video FPS if needed
                wm.modal_handler_add(self)
                self.report({'INFO'}, "Video capture started")
                print("[AniMate] Video capture started, modal operator running.")
                return {'RUNNING_MODAL'}

            except Exception as e:
                self.report({'ERROR'}, f"Error setting up video capture: {e}")
                if hasattr(self, '_cap') and self._cap:
                    self._cap.release()
                return {'CANCELLED'}

        else: # Fallback for unsupported source type
            self.report({'ERROR'}, "Unsupported source type selected.")
            return {'CANCELLED'}
        

    # In operators.py, inside the ANIMATE_OT_start_capture class

    def modal(self, context, event):
        props = context.scene.animate_properties # Get properties here

        # Check if the operator should stop
        if not getattr(context.scene, 'animate_running', False):
            return self.cancel(context)

        # Handle keyboard events (e.g., 'ESC' to stop)
        if event.type == 'ESC':
            self.report({'INFO'}, "Capture cancelled by user.")
            return self.cancel(context)

        # Only process on timer events for continuous sources
        if event.type == 'TIMER':
            if props.source_type == 'WEBCAM' or props.source_type == 'VIDEO':
                
                ret, frame = self._cap.read()
                if not ret:
                    self.report({'WARNING'}, "Failed to read frame from capture source.")
                    return self.cancel(context)

                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results_pose = self.mp_pose.process(image_rgb)
                results_face = self.mp_face.process(image_rgb)
                results_hands = self.mp_hands.process(image_rgb)

                # Update the rig in Blender's main thread
                bpy.context.view_layer.update() # Ensure Blender is updated for drawing

                def update_blender_rig():
                    if results_pose.pose_landmarks:
                        self._mapper.apply_pose_landmarks(results_pose.pose_landmarks)
                    if results_face.multi_face_landmarks:
                        self._mapper.apply_face_landmarks(results_face.multi_face_landmarks[0])
                    if results_hands.multi_hand_landmarks:
                        self._mapper.apply_hand_landmarks(results_hands.multi_hand_landmarks)

                    # Update the camera preview in Blender
                    if props.show_camera_preview:
                        img = bpy.data.images["AniMateCameraPreview"]
                        # Convert back to RGBA for Blender (or just RGB if alpha not needed)
                        # Ensure you handle the frame data correctly for Blender
                        # Example: flip and convert to 8-bit if it's float_buffer=True
                        if frame.shape[2] == 3: # RGB
                            img_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                        else: # Grayscale or other
                            img_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # Adjust as needed
                        img_display = cv2.flip(img_display, 0) # Flip vertically for Blender
                        img.pixels = np.array(img_display).flatten().astype(np.float32) / 255.0 # Normalize to 0-1

                bpy.app.timers.register(update_blender_rig)


                return {'RUNNING_MODAL'} # Keep running for webcam/video

            elif props.source_type == 'IMAGE':
                # Image processing is handled in execute and finishes.
                # If modal is somehow called for an image source, it means something went wrong,
                # or the operator wasn't properly cancelled. So we cancel here.
                self.report({'WARNING'}, "Modal operator unexpectedly running for IMAGE source. Cancelling.")
                return self.cancel(context)

            # If no timer event or unsupported source type in modal
            else:
                return {'PASS_THROUGH'}

        return {'PASS_THROUGH'} # Allow other events to pass through

    def cancel(self, context):
        # Clean up resources
        if self._timer:
            wm = context.window_manager
            wm.event_timer_remove(self._timer)
            self._timer = None
        if self._cap:
            self._cap.release()
            self._cap = None
        if self.mp_pose:
            self.mp_pose.close()
            self.mp_pose = None
        if self.mp_face:
            self.mp_face.close()
            self.mp_face = None
        if self.mp_hands:
            self.mp_hands.close()
            self.mp_hands = None
        if hasattr(self, '_mapper') and self._mapper:
            self._mapper.cleanup() # Ensure cleanup is called
            self._mapper = None
        context.scene.animate_running = False
        self.report({'INFO'}, "Motion capture stopped.")
        print("[AniMate] Motion capture stopped and resources released.")
        return {'CANCELLED'}

    def cancel(self, context):
        wm = context.window_manager
        if self._timer:
            wm.event_timer_remove(self._timer)
            self._timer = None
        if self._cap:
            self._cap.release()
            self._cap = None
        if self.mp_pose:
            self.mp_pose.close()
            self.mp_pose = None
        if self.mp_face:
            self.mp_face.close()
            self.mp_face = None
        if self.mp_hands:
            self.mp_hands.close()
            self.mp_hands = None
        if self._mapper:
            self._mapper.driver_manager.cleanup()
            self._mapper = None
        context.scene.animate_running = False
        self.report({'INFO'}, "Capture stopped")
        print("[AniMate] Capture stopped and cleaned up.")

class ANIMATE_OT_stop_capture(Operator):
    bl_idname = "animate.stop_capture"
    bl_label = "Stop Capture"
    bl_description = "Stop motion capture"

    def execute(self, context):
        context.scene.animate_running = False
        self.report({'INFO'}, "Capture stopped")
        print("[AniMate] animate_running set to False by stop operator.")
        return {'FINISHED'} 