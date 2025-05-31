__author__ = "Valentin Bakin"

import cv2
from utils.pose_detection import PoseDetector
from utils.face_detection import FaceMeshDetector
from utils.hands_detection import HandDetector
from rig.rig_mapper import map_landmarks_to_rig
from rig.animator import animate_rig
from data.landmark_structure import landmarks
import time

# Initialize detectors
pose_detector = PoseDetector()
face_detector = FaceMeshDetector()
hand_detector = HandDetector()

# Detection flags (for future UI toggle)
detection_flags = {
    'pose': True,
    'face': True,
    'hands': True
}

def main():
    cap = initialize_camera()
    p_time = 0  # For FPS calculation

    while cap.isOpened():
        try:
            success, img = cap.read()
            if not success:
                print("Failed to read from camera")
                break

            # Flip the image horizontally for a more natural view
            img = cv2.flip(img, 1)

            # Process all detections if enabled
            if detection_flags['pose']:
                img = process_pose(img, pose_detector)
            if detection_flags['face']:
                img = process_face(img, face_detector)
            if detection_flags['hands']:
                img = process_hands(img, hand_detector)

            # Calculate and display FPS
            fps, p_time = get_fps(p_time)
            cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

            # Add detection status indicators
            y_offset = 60
            for detector_type, is_enabled in detection_flags.items():
                status = "ON" if is_enabled else "OFF"
                color = (0, 255, 0) if is_enabled else (0, 0, 255)
                cv2.putText(img, f"{detector_type}: {status}", (10, y_offset), 
                           cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
                y_offset += 30

            display_frame(img)

            # Handle keyboard input for toggling detections
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('p'):  # 'p' for pose
                detection_flags['pose'] = not detection_flags['pose']
            elif key == ord('f'):  # 'f' for face
                detection_flags['face'] = not detection_flags['face']
            elif key == ord('h'):  # 'h' for hands
                detection_flags['hands'] = not detection_flags['hands']

            if cv2.getWindowProperty("AniMate", cv2.WND_PROP_VISIBLE) < 1:
                break

        except Exception as e:
            print(f"Error in main loop: {e}")
            continue

    cap.release()
    cv2.destroyAllWindows()


def initialize_camera(width=1280, height=720):
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    return cap


def process_pose(img, detector):
    try:
        img = detector.find_pose(img)
    except Exception as e:
        print(f"Error in pose detection: {e}")
    return img


def process_hands(img, detector):
    try:
        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=True)  # Get and draw hand landmarks
    except Exception as e:
        print(f"Error in hand detection: {e}")
    return img


def process_face(img, detector):
    try:
        img, faces = detector.find_face_mesh(img)
    except Exception as e:
        print(f"Error in face detection: {e}")
    return img


def display_frame(img):
    cv2.imshow('AniMate', img)


def get_fps(p_time):
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    return fps, c_time


if __name__ == "__main__":
    main()
