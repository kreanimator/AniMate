__author__ = "Valentin Bakin"

import cv2
import mediapipe as mp
import time


class FaceMeshDetector:
    def __init__(self, static_mode=False,
                 num_faces=1,
                 refine_landmarks=False,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.static_image_mode = static_mode
        self.max_num_faces = num_faces
        self.refine_landmarks = refine_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mp_faceMesh = mp.solutions.face_mesh
        self.mp_draw = mp.solutions.drawing_utils
        self.face_detection = self.mp_faceMesh.FaceMesh(static_image_mode=self.static_image_mode,
                                                        max_num_faces=self.max_num_faces,
                                                        refine_landmarks=self.refine_landmarks,
                                                        min_detection_confidence=self.min_detection_confidence,
                                                        min_tracking_confidence=self.min_tracking_confidence)
        self.draw_specs = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

    def find_face_mesh(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(img_rgb)
        faces = []
        if results.multi_face_landmarks:

            for face_lms in results.multi_face_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, face_lms, self.mp_faceMesh.FACEMESH_CONTOURS,
                                                landmark_drawing_spec=self.draw_specs)
                    face = []
                    for id, lm in enumerate(face_lms.landmark):
                        ih, iw, ic = img.shape
                        x, y = int(lm.x * iw), int(lm.y * ih)
                        face.append([x, y])
                        # Display id number of every dot
                        # cv2.putText(img, f'{str(id)}', (x, y), cv2.FONT_HERSHEY_PLAIN,
                        #             0.5, (0, 255, 0), 1)

                    faces.append(face)
        return img, faces


def main():
    cap = cv2.VideoCapture(0)
    p_time = 0

    detector = FaceMeshDetector()

    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    # cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        success, img = cap.read()
        img, faces = detector.find_face_mesh(img)
        if len(faces) != 0:
            print(len(faces[0]))
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 0), 2)

        cv2.imshow("Face detection test", img)
        cv2.waitKey(1)

        # Break the loop if 'Esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break
        # Check if the window is closed by looking if any windows are still open
        if cv2.getWindowProperty("Face detection test", cv2.WND_PROP_VISIBLE) < 1:
            break


if __name__ == "__main__":
    main()
