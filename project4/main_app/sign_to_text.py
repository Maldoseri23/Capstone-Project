import cv2
import mediapipe as mp
import math

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def classify_sign(landmarks):
    tips_ids = [8, 12, 16, 20]  # Fingertips except thumb
    folded = [landmarks[tip].y > landmarks[tip - 2].y for tip in tips_ids]  # True if finger folded

    thumb_extended = landmarks[4].x < landmarks[3].x  # thumb to left (right hand)

    # Helper checks:
    all_folded = all(folded)
    none_folded = not any(folded)

    # A: all fingers folded except thumb extended sideways (thumb tip left of IP joint)
    if all_folded and thumb_extended:
        return "A"

    # B: all fingers extended, thumb folded across palm (thumb tip below MCP)
    if none_folded and landmarks[4].y > landmarks[3].y:
        return "B"

    # C: curved fingers forming C
    dist_thumb_index = distance(landmarks[4], landmarks[8])
    if dist_thumb_index < 0.1 and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y:
        return "C"

    # D: index extended, others folded
    if folded.count(False) == 1 and not folded[0] and landmarks[8].y < landmarks[6].y:
        return "D"

    # E: all fingers folded with thumb curled over fingers
    if all_folded and landmarks[4].y < landmarks[3].y:
        return "E"

    # F: thumb and index tip touching, other fingers extended
    dist_thumb_index = distance(landmarks[4], landmarks[8])
    others_extended = not folded[1] and not folded[2] and not folded[3]
    if dist_thumb_index < 0.05 and others_extended:
        return "F"

    # G: index finger extended horizontal, thumb near index
    if folded[1] and folded[2] and folded[3] and landmarks[8].y < landmarks[6].y and abs(landmarks[4].y - landmarks[8].y) < 0.05:
        return "G"

    # H: index and middle extended horizontal, others folded
    if not folded[0] and not folded[1] and folded[2] and folded[3]:
        return "H"

    # I: pinky extended, others folded
    if folded[0] and folded[1] and folded[2] and not folded[3]:
        return "I"

    # J: pinky extended, move in a J motion (can't detect motion here, so treat as I)
    if folded[0] and folded[1] and folded[2] and not folded[3]:
        return "J"

    # K: index and middle extended, thumb between them
    if not folded[0] and not folded[1] and folded[2] and folded[3]:
        thumb_between = landmarks[4].y > landmarks[6].y and landmarks[4].y < landmarks[10].y
        if thumb_between:
            return "K"

    # L: index and thumb extended at right angle
    if not folded[0] and folded[1] and folded[2] and folded[3] and landmarks[4].x < landmarks[3].x:
        return "L"

    # M: thumb under three folded fingers (index, middle, ring)
    if folded[0] and folded[1] and folded[2] and folded[3] and landmarks[4].x > landmarks[3].x:
        return "M"

    # N: thumb under two folded fingers (index, middle)
    if folded[0] and folded[1] and not folded[2] and folded[3] and landmarks[4].x > landmarks[3].x:
        return "N"

    # O: all fingers and thumb curved forming circle
    dist_thumb_index = distance(landmarks[4], landmarks[8])
    dist_thumb_pinky = distance(landmarks[4], landmarks[20])
    if dist_thumb_index < 0.1 and dist_thumb_pinky < 0.15 and not all_folded:
        return "O"

    # P: like K but hand rotated downward (not detectable here), treat like K for now
    if not folded[0] and not folded[1] and folded[2] and folded[3]:
        return "P"

    # Q: like G but hand rotated downward, treat like G
    if folded[1] and folded[2] and folded[3] and landmarks[8].y < landmarks[6].y and abs(landmarks[4].y - landmarks[8].y) < 0.05:
        return "Q"

    # R: crossed index and middle finger
    crossed = landmarks[8].x > landmarks[12].x
    if not folded[0] and not folded[1] and folded[2] and folded[3] and crossed:
        return "R"

    # S: fist with thumb in front
    if all_folded and landmarks[4].x < landmarks[3].x:
        return "S"

    # T: fist with thumb between index and middle finger
    thumb_between = landmarks[4].x > landmarks[8].x and landmarks[4].x < landmarks[12].x
    if all_folded and thumb_between:
        return "T"

    # U: index and middle extended and together, others folded
    fingers_together = abs(landmarks[8].x - landmarks[12].x) < 0.05
    if not folded[0] and not folded[1] and folded[2] and folded[3] and fingers_together:
        return "U"

    # V: index and middle extended and apart, others folded
    fingers_apart = abs(landmarks[8].x - landmarks[12].x) > 0.1
    if not folded[0] and not folded[1] and folded[2] and folded[3] and fingers_apart:
        return "V"

    # W: index, middle, ring extended, pinky folded
    if not folded[0] and not folded[1] and not folded[2] and folded[3]:
        return "W"

    # X: index bent with thumb curled (hook shape)
    if folded[0] and folded[1] and folded[2] and folded[3] and landmarks[8].y < landmarks[6].y:
        return "X"

    # Y: thumb and pinky extended, others folded
    if folded[0] and folded[1] and folded[2] and not folded[3] and landmarks[4].x < landmarks[3].x:
        return "Y"

    # Z: index extended, draw Z shape (motion needed, so treat as D for static)
    if folded.count(False) == 1 and not folded[0] and landmarks[8].y < landmarks[6].y:
        return "Z"

    # Default unknown
    return "..."

# Mediapipe setup
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
            sign = classify_sign(hand_landmarks.landmark)

    cv2.putText(frame, f'Sign: {sign}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1.5, (0, 255, 0), 3)

    cv2.imshow("ASL Letters Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
