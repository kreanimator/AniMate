__author__ = "Valentin Bakin"

import cv2
from utils.pose_detection import PoseDetector
from utils.face_detection import FaceMeshDetector
from utils.hands_detection import HandDetector
from rig.rig_mapper import map_landmarks_to_rig
from rig.animator import animate_rig
from data.landmark_structure import landmarks


# Initialize detectors
pose_detector = PoseDetector()
face_detector = FaceMeshDetector()
hand_detector = HandDetector()


def main():
    cap = initialize_camera()

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break

        # img = process_pose(img, pose_detector)
        # img = process_face(img, face_detector)
        img = process_hands(img, hand_detector)

        display_frame(img)

        if cv2.waitKey(1) & 0xFF == 27:
            break
        if cv2.getWindowProperty("AniMate", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


def initialize_camera(width=1280, height=720):
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    return cap


def process_pose(img, detector):
    img = detector.find_pose(img)
    img = detector.find_face(img)  # If needed; otherwise, keep it separate
    img = detector.find_left_hand(img)
    img = detector.find_right_hand(img)
    return img


def process_hands(img, detector):
    img = detector.find_hands(img)

    return img


def process_face(img, detector):
    img, _ = detector.find_face_mesh(img)
    return img


def display_frame(img):
    cv2.imshow('AniMate', img)


if __name__ == "__main__":
    main()
