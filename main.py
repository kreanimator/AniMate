__author__ = "Valentin Bakin"

import cv2
from utils.pose_detection import PoseDetector
from utils.face_detection import FaceMeshDetector
from utils.hands_detection import HandDetector
from rig.rig_mapper import map_landmarks_to_rig
from rig.animator import animate_rig


w_cam, h_cam = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, w_cam)
cap.set(4, h_cam)

pose_detector = PoseDetector()
face_detector = FaceMeshDetector()
hand_detector = HandDetector()

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img = pose_detector.find_pose(img)
    img = pose_detector.find_face(img)
    img = pose_detector.find_left_hand(img)
    img = pose_detector.find_right_hand(img)

    # Uncomment if needed
    # face_landmarks = face_detector.find_face(img)
    # hand_landmarks = hand_detector.find_hand(img)

    # Uncomment if needed
    # map_landmarks_to_rig(pose_landmarks, face_landmarks, hand_landmarks)
    # animate_rig()

    cv2.imshow('AniMate', img)

    if cv2.waitKey(1) & 0xFF == 27:
        break
    if cv2.getWindowProperty("AniMate", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
