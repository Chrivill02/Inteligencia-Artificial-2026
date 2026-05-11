import cv2
import mediapipe as mp
import math
import numpy as np
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode

MIN_DIST = 20
MAX_DIST = 200

MODEL_PATH = "hand_landmarker.task"

prev_time = 0

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = HandLandmarkerOptions(
    base_options=base_options,
    running_mode=RunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

with HandLandmarker.create_from_options(options) as detector:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        results = detector.detect(mp_image)

        percentage = 0

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:

                x1 = int(hand_landmarks[4].x * width)
                y1 = int(hand_landmarks[4].y * height)

                x2 = int(hand_landmarks[8].x * width)
                y2 = int(hand_landmarks[8].y * height)

                dx = x2 - x1
                dy = y2 - y1
                distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

                percentage = np.interp(distance, [MIN_DIST, MAX_DIST], [0, 100])
                percentage = int(np.clip(percentage, 0, 100))

                if distance < 40:
                    line_color = (0, 0, 255)
                else:
                    line_color = (0, 255, 0)

                cv2.line(frame, (x1, y1), (x2, y2), line_color, 2)
                cv2.circle(frame, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 8, (255, 0, 255), cv2.FILLED)

                for lm in hand_landmarks:
                    cx = int(lm.x * width)
                    cy = int(lm.y * height)
                    cv2.circle(frame, (cx, cy), 3, (200, 200, 200), cv2.FILLED)

        bar_x = 50
        bar_y_top = 100
        bar_y_bottom = 350
        bar_width = 30

        cv2.rectangle(frame, (bar_x, bar_y_top), (bar_x + bar_width, bar_y_bottom), (50, 50, 50), 2)

        fill_y = int(np.interp(percentage, [0, 100], [bar_y_bottom, bar_y_top]))
        cv2.rectangle(frame, (bar_x + 2, fill_y), (bar_x + bar_width - 2, bar_y_bottom), (0, 200, 100), cv2.FILLED)

        cv2.putText(frame, f'{percentage}%', (bar_x - 5, bar_y_bottom + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.putText(frame, 'Air Controller', (width // 2 - 100, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time

        cv2.putText(frame, f'FPS: {int(fps)}', (width - 120, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)

        cv2.imshow('Air Controller', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()