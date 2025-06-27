# import cv2
# import mediapipe as mp
# import csv

# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# mp_drawing = mp.solutions.drawing_utils

# cap = cv2.VideoCapture(0)

# label = input("Enter the label for this gesture (e.g. hello, thanks, etc.): ")
# filename = f"{label}_data.csv"

# with open(filename, mode='w', newline='') as f:
#     csv_writer = csv.writer(f)
#     print("[INFO] Starting data collection. Press 'q' to stop.")

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame = cv2.flip(frame, 1)
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = hands.process(rgb)

#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
             
#                 row = []
#                 for lm in hand_landmarks.landmark:
#                     row.extend([lm.x, lm.y, lm.z])
#                 row.append(label)
#                 csv_writer.writerow(row)

#                 mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#         cv2.imshow("Collecting Data", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# cap.release()
# cv2.destroyAllWindows()
