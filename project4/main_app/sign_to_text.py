import cv2
import mediapipe as mp
import math

# === Helper function for distance between two landmarks ===
def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# === Detect ASL letter ===
def classify_sign(landmarks):
    tips_ids = [8, 12, 16, 20]  # Fingertips except thumb
    folded = [landmarks[tip].y > landmarks[tip - 2].y for tip in tips_ids]
    thumb_extended = landmarks[4].x < landmarks[3].x
    all_folded = all(folded)
    none_folded = not any(folded)

    if all_folded and thumb_extended:
        return "A"
    if none_folded and landmarks[4].y > landmarks[3].y:
        return "B"
    dist_thumb_index = distance(landmarks[4], landmarks[8])
    if dist_thumb_index < 0.1 and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y:
        return "C"
    if folded.count(False) == 1 and not folded[0] and landmarks[8].y < landmarks[6].y:
        return "D"
    if all_folded and landmarks[4].y < landmarks[3].y:
        return "E"
    dist_thumb_index = distance(landmarks[4], landmarks[8])
    others_extended = not folded[1] and not folded[2] and not folded[3]
    if dist_thumb_index < 0.05 and others_extended:
        return "F"
    if folded[1] and folded[2] and folded[3] and landmarks[8].y < landmarks[6].y and abs(landmarks[4].y - landmarks[8].y) < 0.05:
        return "G"
    if not folded[0] and not folded[1] and folded[2] and folded[3]:
        return "H"
    if folded[0] and folded[1] and folded[2] and not folded[3]:
        return "I"
    if folded[0] and folded[1] and folded[2] and not folded[3]:
        return "J"
    if not folded[0] and not folded[1] and folded[2] and folded[3]:
        thumb_between = landmarks[4].y > landmarks[6].y and landmarks[4].y < landmarks[10].y
        if thumb_between:
            return "K"
    if not folded[0] and folded[1] and folded[2] and folded[3] and landmarks[4].x < landmarks[3].x:
        return "L"
    if folded[0] and folded[1] and folded[2] and folded[3] and landmarks[4].x > landmarks[3].x:
        return "M"
    if folded[0] and folded[1] and not folded[2] and folded[3] and landmarks[4].x > landmarks[3].x:
        return "N"
    dist_thumb_index = distance(landmarks[4], landmarks[8])
    dist_thumb_pinky = distance(landmarks[4], landmarks[20])
    if dist_thumb_index < 0.1 and dist_thumb_pinky < 0.15 and not all_folded:
        return "O"
    if not folded[0] and not folded[1] and folded[2] and folded[3]:
        return "P"
    if folded[1] and folded[2] and folded[3] and landmarks[8].y < landmarks[6].y and abs(landmarks[4].y - landmarks[8].y) < 0.05:
        return "Q"
    crossed = landmarks[8].x > landmarks[12].x
    if not folded[0] and not folded[1] and folded[2] and folded[3] and crossed:
        return "R"
    if all_folded and landmarks[4].x < landmarks[3].x:
        return "S"
    thumb_between = landmarks[4].x > landmarks[8].x and landmarks[4].x < landmarks[12].x
    if all_folded and thumb_between:
        return "T"
    fingers_together = abs(landmarks[8].x - landmarks[12].x) < 0.05
    if not folded[0] and not folded[1] and folded[2] and folded[3] and fingers_together:
        return "U"
    fingers_apart = abs(landmarks[8].x - landmarks[12].x) > 0.1
    if not folded[0] and not folded[1] and folded[2] and folded[3] and fingers_apart:
        return "V"
    if not folded[0] and not folded[1] and not folded[2] and folded[3]:
        return "W"
    if folded[0] and folded[1] and folded[2] and folded[3] and landmarks[8].y < landmarks[6].y:
        return "X"
    if folded[0] and folded[1] and folded[2] and not folded[3] and landmarks[4].x < landmarks[3].x:
        return "Y"
    if folded.count(False) == 1 and not folded[0] and landmarks[8].y < landmarks[6].y:
        return "Z"

    return "..."

# === Detect whole-word gestures ===
def classify_word(landmarks):
    tips = [8, 12, 16, 20]
    folded = [landmarks[tip].y > landmarks[tip - 2].y for tip in tips]

    # YES: thumbs up + all fingers folded
    if landmarks[4].y < landmarks[3].y and all(folded):
        return "YES"

    # NO: thumbs down + all fingers folded
    if landmarks[4].y > landmarks[3].y and all(folded):
        return "NO"

    # HELLO: all fingers extended
    if all(landmarks[tip].y < landmarks[tip - 2].y for tip in tips) and landmarks[4].x < landmarks[3].x:
        return "HELLO"

    # I LOVE YOU: thumb, index, pinky extended
    up = lambda tip: landmarks[tip].y < landmarks[tip - 2].y
    if up(4) and up(8) and up(20) and not up(12) and not up(16):
        return "I LOVE YOU"

    return None

# === Mediapipe setup ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    sign = "..."

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Try to classify a whole word gesture first
            word = classify_word(hand_landmarks.landmark)
            if word:
                sign = word
            else:
                sign = classify_sign(hand_landmarks.landmark)

    cv2.putText(frame, f'Sign: {sign}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1.5, (0, 255, 0), 3)

    cv2.imshow("ASL Letters & Words Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()