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

        # Initialize MediaPipe solutions (these are moved here from __init__)
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

        # Handle different source types
        if props.source_type == 'WEBCAM':
            print("[AniMate] Starting webcam capture...")
            self._cap = cv2.VideoCapture(0)
            if not self._cap.isOpened():
                self.report({'ERROR'}, "Could not open camera.")
                return {'CANCELLED'}
            if "AniMateCameraPreview" not in bpy.data.images:
                bpy.data.images.new("AniMateCameraPreview", width=640, height=480, alpha=True, float_buffer=True, is_data=True) # CORRECTED LINE
            img = bpy.data.images["AniMateCameraPreview"]
            img.generated_width = 640
            img.generated_height = 480
            img.colorspace_settings.name = 'sRGB'
            img.use_fake_user = True

            # Start the modal operator
            context.scene.animate_running = True
            wm = context.window_manager
            self._timer = wm.event_timer_add(1/30, window=context.window)
            wm.modal_handler_add(self)
            self.report({'INFO'}, "Capture started")
            print("[AniMate] Capture started, modal operator running.")
            return {'RUNNING_MODAL'}

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
                if "AniMateCameraPreview" not in bpy.data.images:
                    bpy.data.images.new("AniMateCameraPreview", width=640, height=480, alpha=True, float_buffer=True, is_data=True) # CORRECTED LINE
                img = bpy.data.images["AniMateCameraPreview"]
                img.generated_width = 640
                img.generated_height = 480
                img.colorspace_settings.name = 'sRGB'
                img.use_fake_user = True

                # Start the modal operator for continuous video processing
                context.scene.animate_running = True
                wm = context.window_manager
                self._timer = wm.event_timer_add(1/30, window=context.window)
                wm.modal_handler_add(self)
                self.report({'INFO'}, "Video capture started")
                print("[AniMate] Video capture started, modal operator running.")
                return {'RUNNING_MODAL'}
            except Exception as e:
                self.report({'ERROR'}, f"Error opening video: {e}")
                return {'CANCELLED'}

        elif props.source_type == 'IMAGE':
            print(f"[AniMate] Processing image: {props.image_filepath}")
            if not props.image_filepath:
                self.report({'ERROR'}, "No image file selected.")
                return {'CANCELLED'}
            try:
                img_path = bpy.path.abspath(props.image_filepath)
                frame = cv2.imread(img_path)
                if frame is None:
                    self.report({'ERROR'}, f"Failed to load image: {props.image_filepath}. Check path or file format.")
                    return {'CANCELLED'}

                # Process the single image immediately
                # (You might want to add a proper image processing function here later)
                print("[AniMate] Image processed successfully (placeholder).") # Placeholder for actual image processing

                # Resize frame for MediaPipe if necessary
                frame = cv2.resize(frame, (640, 480))
                # Convert to RGB for MediaPipe
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process the image with MediaPipe
                results = self.mp_pose.process(frame_rgb)
                if results.pose_landmarks:
                    print("[AniMate] Pose landmarks detected from image.")
                    self._mapper = BlenderRigMapper(props.target_armature, rig_type=props.rig_type)
                    self._mapper.driver_manager.create_drivers()
                    self._mapper.scan_rig()
                    self._mapper.initialize_rig()
                    self._mapper.update_pose_from_landmarks(results.pose_landmarks)
                else:
                    print("[AniMate] No pose landmarks detected from image.")
                    self.report({'WARNING'}, "No pose detected in image.")

                # Clean up MediaPipe resources (important for static image mode)
                self.mp_pose.close()
                self.mp_face.close()
                self.mp_hands.close()

                self.report({'INFO'}, "Image processed. Pose applied.")
                return {'FINISHED'} # Image processing is a one-time operation
            except Exception as e: 
                self.report({'ERROR'}, f"Error processing image: {e}")
                return {'CANCELLED'}

        self.report({'ERROR'}, "Unknown source type selected.")
        return {'CANCELLED'}

    def modal(self, context, event):
        if event.type != 'TIMER':
            return {'PASS_THROUGH'}
        try:
            if not getattr(context.scene, 'animate_running', False):
                print("[AniMate] animate_running is False, cancelling modal.")
                self.cancel(context)
                return {'CANCELLED'}
            ret, frame = self._cap.read()
            if not ret:
                return {'PASS_THROUGH'}
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            props = context.scene.animate_properties
            pose_landmarks = None
            face_landmarks = None
            left_hand_landmarks = None
            right_hand_landmarks = None
            # MediaPipe detection with debug prints
            if props.enable_pose:
                results_pose = self.mp_pose.process(frame)
                print(f"[AniMate] Pose landmarks: {getattr(results_pose, 'pose_landmarks', None)}")
                if results_pose.pose_landmarks:
                    pose_landmarks = results_pose.pose_landmarks
            if props.enable_face:
                results_face = self.mp_face.process(frame)
                print(f"[AniMate] Face landmarks: {getattr(results_face, 'multi_face_landmarks', None)}")
                if results_face.multi_face_landmarks:
                    face_landmarks = results_face.multi_face_landmarks[0]
            if props.enable_hands:
                results_hands = self.mp_hands.process(frame)
                print(f"[AniMate] Hand landmarks: {getattr(results_hands, 'multi_hand_landmarks', None)}")
                if results_hands.multi_hand_landmarks:
                    if len(results_hands.multi_hand_landmarks) > 0:
                        left_hand_landmarks = results_hands.multi_hand_landmarks[0]
                    if len(results_hands.multi_hand_landmarks) > 1:
                        right_hand_landmarks = results_hands.multi_hand_landmarks[1]
            # Draw landmarks on the preview frame
            if pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    pose_landmarks,
                    mp.solutions.pose.POSE_CONNECTIONS,
                    mp_drawing_styles.get_default_pose_landmarks_style())
            if face_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp.solutions.face_mesh.FACEMESH_TESSELATION,
                    mp_drawing_styles.get_default_face_mesh_tesselation_style())
            if left_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    left_hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
            if right_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    right_hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
            # Convert pose landmarks with global rotation
            h, w, _ = frame.shape
            flip_x = props.camera_mirrored
            if pose_landmarks:
                for lm in pose_landmarks.landmark:
                    lm.x, lm.y, lm.z = mediapipe_to_blender_coords_pose(lm, w, h, flip_x=flip_x)
            if face_landmarks:
                for lm in face_landmarks.landmark:
                    lm.x, lm.y, lm.z = mediapipe_to_blender_coords(lm, w, h, flip_x=flip_x)
            if left_hand_landmarks:
                for lm in left_hand_landmarks.landmark:
                    lm.x, lm.y, lm.z = mediapipe_to_blender_coords(lm, w, h, flip_x=flip_x)
            if right_hand_landmarks:
                for lm in right_hand_landmarks.landmark:
                    lm.x, lm.y, lm.z = mediapipe_to_blender_coords(lm, w, h, flip_x=flip_x)
            # Debug print before rig update
            print(f"[AniMate] Updating rig: pose={pose_landmarks is not None}, face={face_landmarks is not None}, left_hand={left_hand_landmarks is not None}, right_hand={right_hand_landmarks is not None}")
            # Update the rig with the detected landmarks
            if self._mapper:
                self._mapper.update_rig(
                    pose_landmarks=pose_landmarks,
                    face_landmarks=face_landmarks,
                    left_hand_landmarks=left_hand_landmarks,
                    right_hand_landmarks=right_hand_landmarks
                )
            # Update the preview image
            alpha = np.ones((h, w, 1), dtype=np.uint8) * 255
            frame_rgba = np.concatenate((frame, alpha), axis=2)
            frame_rgba = np.flipud(frame_rgba)  # Flip vertically for Blender
            frame_flat = (frame_rgba / 255.0).astype(np.float32).flatten()
            img = bpy.data.images.get("AniMateCameraPreview")
            if img and len(frame_flat) == img.size[0] * img.size[1] * img.channels:
                img.pixels = frame_flat.tolist()
                img.update()
        except Exception as e:
            print(f"[AniMate] ERROR in modal: {e}")
        return {'RUNNING_MODAL'}

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