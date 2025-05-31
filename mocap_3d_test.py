import cv2
import mediapipe as mp
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use Agg backend (no window)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import threading
from queue import Queue

class MotionCapture:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize 2D window
        cv2.namedWindow('Motion Capture 2D')
        
        # Queue for communication between threads
        self.landmark_queue = Queue()
        self.running = True
        
        # Store 3D coordinates for visualization
        self.points_3d = None
    
    def process_frame(self, frame):
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.pose.process(rgb_frame)
        
        if results.pose_landmarks:
            # Draw 2D skeleton
            self.draw_2d_skeleton(frame, results.pose_landmarks)
            
            # Convert landmarks to 3D points
            points_3d = []
            for landmark in results.pose_landmarks.landmark:
                points_3d.append([landmark.x, landmark.y, landmark.z])
            self.points_3d = np.array(points_3d)
            
            # Draw 3D coordinates on frame
            self.draw_3d_coords(frame)
        
        return frame
    
    def draw_2d_skeleton(self, frame, landmarks):
        height, width, _ = frame.shape
        
        # Define connections for skeleton
        connections = [
            # Torso
            (11, 12), (12, 24), (24, 23), (23, 11),
            # Right arm
            (12, 14), (14, 16),
            # Left arm
            (11, 13), (13, 15),
            # Right leg
            (24, 26), (26, 28),
            # Left leg
            (23, 25), (25, 27)
        ]
        
        for connection in connections:
            start_point = landmarks.landmark[connection[0]]
            end_point = landmarks.landmark[connection[1]]
            
            start_point = (int(start_point.x * width), int(start_point.y * height))
            end_point = (int(end_point.x * width), int(end_point.y * height))
            
            cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
    
    def draw_3d_coords(self, frame):
        if self.points_3d is not None:
            height, width, _ = frame.shape
            padding = 10
            text_height = 15
            
            # Draw coordinate values for key points
            key_points = {
                "Head": 0,
                "Right Shoulder": 12,
                "Left Shoulder": 11,
                "Right Hip": 24,
                "Left Hip": 23
            }
            
            y_offset = padding
            for name, idx in key_points.items():
                point = self.points_3d[idx]
                text = f"{name}: X={point[0]:.2f}, Y={point[1]:.2f}, Z={point[2]:.2f}"
                cv2.putText(frame, text, (padding, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_offset += text_height + 5
    
    def run(self):
        # Start camera
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            # Process frame
            frame = cv2.flip(frame, 1)
            frame = self.process_frame(frame)
            
            # Display 2D view
            cv2.imshow('Motion Capture 2D', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            try:
                if key == 27 or cv2.getWindowProperty('Motion Capture 2D', cv2.WND_PROP_VISIBLE) < 1:  # ESC or window closed
                    break
            except cv2.error:
                # Window was closed
                break
        
        # Cleanup
        self.running = False
        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)  # Give time for windows to close properly

if __name__ == "__main__":
    mocap = MotionCapture()
    mocap.run() 