import cv2
import mediapipe as mp
import numpy as np
import time

class MotionCapture:
    def __init__(self):
        # Initialize MediaPipe solutions
        self.mp_pose = mp.solutions.pose
        self.mp_face = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize detectors
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.face_mesh = self.mp_face.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Store previous landmark positions for visualization
        self.previous_landmarks = None
        
        # Detection flags
        self.detection_flags = {
            'pose': True,
            'face': True,
            'hands': True
        }
        
    def process_frame(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = {
            'pose': None,
            'face': None,
            'hands': None,
            'pose_landmarks': None
        }
        
        # Process with enabled detectors
        if self.detection_flags['pose']:
            results['pose'] = self.pose.process(rgb_frame)
            if results['pose'].pose_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    results['pose'].pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_draw.DrawingSpec(color=(255,0,0))
                )
                
                # Store landmarks for movement vectors
                if self.previous_landmarks:
                    self.draw_movement_vectors(frame, results['pose'].pose_landmarks)
                self.previous_landmarks = results['pose'].pose_landmarks
                
                # Calculate and draw angles
                self.draw_joint_angles(frame, results['pose'].pose_landmarks)
                results['pose_landmarks'] = results['pose'].pose_landmarks
        
        if self.detection_flags['face']:
            results['face'] = self.face_mesh.process(rgb_frame)
            if results['face'].multi_face_landmarks:
                for face_landmarks in results['face'].multi_face_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame,
                        face_landmarks,
                        self.mp_face.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self.mp_draw.DrawingSpec(color=(0,255,0), thickness=1)
                    )
        
        if self.detection_flags['hands']:
            results['hands'] = self.hands.process(rgb_frame)
            if results['hands'].multi_hand_landmarks:
                for hand_landmarks in results['hands'].multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=self.mp_draw.DrawingSpec(color=(0,0,255))
                    )
        
        return frame, results
    
    def draw_movement_vectors(self, frame, current_landmarks):
        h, w, _ = frame.shape
        for i, (curr, prev) in enumerate(zip(current_landmarks.landmark, 
                                           self.previous_landmarks.landmark)):
            # Convert normalized coordinates to pixel coordinates
            cx, cy = int(curr.x * w), int(curr.y * h)
            px, py = int(prev.x * w), int(prev.y * h)
            
            # Draw movement vector if significant movement detected
            if abs(cx - px) > 2 or abs(cy - py) > 2:
                cv2.arrowedLine(frame, (px, py), (cx, cy), (0, 255, 0), 2)
    
    def draw_joint_angles(self, frame, landmarks):
        h, w, _ = frame.shape
        
        # Define joint triplets for angle calculation
        joints = {
            'right_elbow': [12, 14, 16],  # shoulder, elbow, wrist
            'left_elbow': [11, 13, 15],
            'right_knee': [24, 26, 28],   # hip, knee, ankle
            'left_knee': [23, 25, 27]
        }
        
        for joint_name, (p1, p2, p3) in joints.items():
            angle = self.calculate_angle(landmarks.landmark[p1],
                                      landmarks.landmark[p2],
                                      landmarks.landmark[p3])
            
            # Get middle point (joint position) for text
            x = int(landmarks.landmark[p2].x * w)
            y = int(landmarks.landmark[p2].y * h)
            
            # Draw angle
            cv2.putText(frame, f'{int(angle)}°', (x, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    @staticmethod
    def calculate_angle(p1, p2, p3):
        # Convert landmarks to numpy arrays
        v1 = np.array([p1.x, p1.y])
        v2 = np.array([p2.x, p2.y])
        v3 = np.array([p3.x, p3.y])
        
        # Calculate vectors
        v21 = v1 - v2
        v23 = v3 - v2
        
        # Calculate angle
        cosine = np.dot(v21, v23) / (np.linalg.norm(v21) * np.linalg.norm(v23))
        angle = np.arccos(np.clip(cosine, -1.0, 1.0))
        
        return np.degrees(angle)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    
    mocap = MotionCapture()
    p_time = 0
    window_name = 'Motion Capture Test'
    
    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read from camera")
            break
            
        # Flip frame horizontally for more natural movement
        frame = cv2.flip(frame, 1)
        
        # Process frame
        frame, results = mocap.process_frame(frame)
        
        # Calculate and display FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        
        # Display FPS and detection status
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        
        # Display detection status
        y_offset = 60
        for det_type, is_enabled in mocap.detection_flags.items():
            status = "ON" if is_enabled else "OFF"
            color = (0, 255, 0) if is_enabled else (0, 0, 255)
            cv2.putText(frame, f"{det_type}: {status}", (10, y_offset),
                       cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
            y_offset += 30
        
        # Display frame
        cv2.imshow(window_name, frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:  # ESC or window closed
            break
        elif key == ord('p'):  # Toggle pose detection
            mocap.detection_flags['pose'] = not mocap.detection_flags['pose']
        elif key == ord('f'):  # Toggle face detection
            mocap.detection_flags['face'] = not mocap.detection_flags['face']
        elif key == ord('h'):  # Toggle hand detection
            mocap.detection_flags['hands'] = not mocap.detection_flags['hands']
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 