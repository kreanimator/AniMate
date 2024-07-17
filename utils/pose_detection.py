__author__ = "Valentin Bakin"

import csv
import cv2
import mediapipe as mp
import time
import math


class PoseDetector:
    def __init__(self, mode=False,
                 complexity=1,
                 smooth_landmarks=True,
                 enable_segmentation=False,
                 smooth_segmentation=True,
                 refine_face_landmarks=False,
                 detection_confidence=0.5,
                 tracking_confidence=0.5):

        self.results = None
        self.mode = mode
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.refine_face_landmarks = refine_face_landmarks
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=self.mode,
            model_complexity=self.complexity,
            smooth_landmarks=self.smooth_landmarks,
            enable_segmentation=self.enable_segmentation,
            smooth_segmentation=self.smooth_segmentation,
            refine_face_landmarks=self.refine_face_landmarks,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )

        # Initialize dictionaries to store landmark positions
        self.body_landmarks = []
        self.face_landmarks = []
        self.left_hand_landmarks = []
        self.right_hand_landmarks = []

    def find_pose(self, img, draw=True):
        # Convert the BGR image to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the RGB image with the Holistic model
        self.results = self.holistic.process(img_rgb)

        # Draw pose landmarks

        if self.results.pose_landmarks:
            if draw:
                self.draw_landmarks(img, self.results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS, (255, 0, 0),
                                    draw)
        self.store_landmarks(img, self.results.pose_landmarks, 'body')

        return img

    def find_face(self, img, draw=True):
        # Process the RGB image with the Holistic model (removed redundant code)
        results = self.holistic.process(img)  # Use the processed image directly
        if draw:
            if results.face_landmarks:
                self.draw_landmarks(img, results.face_landmarks, None, (0, 255, 0), draw, radius=2)
                self.store_landmarks(img, results.face_landmarks, 'face')

        return img

    def find_left_hand(self, img, draw=True):
        # Process the RGB image with the Holistic model (removed redundant code)
        results = self.holistic.process(img)  # Use the processed image directly
        if draw:
            if results.left_hand_landmarks:
                self.draw_landmarks(img, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, (0, 0, 255),
                                    draw)
                self.store_landmarks(img, results.left_hand_landmarks, 'left_hand')

        return img

    def find_right_hand(self, img, draw=True):
        # Process the RGB image with the Holistic model (removed redundant code)
        results = self.holistic.process(img)  # Use the processed image directly
        if draw:
            if results.right_hand_landmarks:
                self.draw_landmarks(img, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, (255, 0, 0),
                                    draw)
                self.store_landmarks(img, results.right_hand_landmarks, 'right_hand')

        return img

    def draw_landmarks(self, img, landmarks, connections, color, draw=True, radius=4):
        if draw:
            self.mp_draw.draw_landmarks(img, landmarks, connections,
                                        landmark_drawing_spec=self.mp_draw.DrawingSpec(color=color, thickness=1,
                                                                                       circle_radius=radius))

    def store_landmarks(self, img, landmarks, part) -> list:
        lm_list = []
        h, w, c = img.shape  # Get image dimensions

        for lm_id, lm in enumerate(landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append([lm_id, cx, cy])

        # Store landmarks based on part
        if part == 'body':
            self.body_landmarks = lm_list
        elif part == 'face':
            self.face_landmarks = lm_list
        elif part == 'left_hand':
            self.left_hand_landmarks = lm_list
        elif part == 'right_hand':
            self.right_hand_landmarks = lm_list

        return lm_list

    def get_all_landmarks(self):
        return {
            'body': self.body_landmarks,
            'face': self.face_landmarks,
            'left_hand': self.left_hand_landmarks,
            'right_hand': self.right_hand_landmarks
        }

    @staticmethod
    def write_landmarks_to_csv(landmarks, filename='landmarks.csv'):
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['Part', 'ID', 'X', 'Y']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for part, lm_lists in landmarks.items():
                for lm in lm_lists:
                    if len(lm) == 3:  # Ensure lm has exactly three elements [lm_id, x, y]
                        lm_id, x, y = lm  # Unpack lm [lm_id, x, y]
                        writer.writerow({
                            'Part': part,
                            'ID': lm_id,
                            'X': x,
                            'Y': y
                        })
                        # print(f"Writing: Part={part}, ID={lm_id}, X={x}, Y={y}")  # Debug print
                    else:
                        print(f"Skipping invalid landmark format: {lm}")

    def find_angle(self, img, p1, p2, p3, draw=True):
        lm_dict = self.get_all_landmarks()
        body_landmarks = lm_dict.get('body', [])
        angle = None

        # Check if the body landmarks list is not empty and contains the necessary points
        if len(body_landmarks) > max(p1, p2, p3):
            # Get the landmarks
            x1, y1 = body_landmarks[p1][1:]
            x2, y2 = body_landmarks[p2][1:]
            x3, y3 = body_landmarks[p3][1:]

            # Calculate the angle
            angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                 math.atan2(y1 - y2, x1 - x2))
            if angle < 0:
                angle += 360

            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)

                cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (0, 0, 255), 3)
                cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (0, 0, 255), 3)
                cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x3, y3), 15, (0, 0, 255), 3)
                #  Display the angle
                # cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                #             cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                # print(f'Print angle from find_angle func {angle}')
        else:
            print("Insufficient body landmarks to calculate angle")

        return angle


def main():
    cap = cv2.VideoCapture(0)
    p_time = 0

    # Initialize detectors
    pose_detector = PoseDetector()

    while True:
        success, img = cap.read()
        if not success:
            break

        # Flip the image horizontally to mirror it
        img = cv2.flip(img, 1)
        # Process the image once and reuse the processed image
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect pose and draw landmarks
        pose_detector.find_pose(processed_img)
        # Detect face and draw landmarks
        pose_detector.find_face(processed_img)
        # Detect and draw left hand landmarks
        pose_detector.find_left_hand(processed_img)
        # Detect and draw right hand landmarks
        pose_detector.find_right_hand(processed_img)

        lm_list = pose_detector.get_all_landmarks()

        # Convert processed image back to BGR for display
        img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR)

        # Calculate and display FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(img, "FPS: " + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        # Display the image
        cv2.imshow("Pose detection test", img)

        # Break the loop if 'Esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            PoseDetector.write_landmarks_to_csv(lm_list)
            break
        # Check if the window is closed by looking if any windows are still open
        if cv2.getWindowProperty("Pose detection test", cv2.WND_PROP_VISIBLE) < 1:
            PoseDetector.write_landmarks_to_csv(lm_list)
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
