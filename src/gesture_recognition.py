import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

def get_gesture(landmarks, w, h):
    """
    Classifies the hand gesture based on finger positions.
    """
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]

    index_tip = landmarks[8]
    index_pip = landmarks[6]

    middle_tip = landmarks[12]
    middle_pip = landmarks[10]

    ring_tip = landmarks[16]
    ring_pip = landmarks[14]

    pinky_tip = landmarks[20]
    pinky_pip = landmarks[18]

    # Detect if fingers are up
    fingers = [
        thumb_tip[0] > thumb_ip[0],  
        index_tip[1] < index_pip[1],  
        middle_tip[1] < middle_pip[1],  
        ring_tip[1] < ring_pip[1],  
        pinky_tip[1] < pinky_pip[1]  
    ]

    # Classify based on fingers
    if all(fingers[1:]):  
        return "Paper"
    elif not any(fingers[1:]):  
        return "Rock"
    elif fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:  
        return "Scissors"
    return "Unknown"

def detect_hand_gesture(frame):
    """
    Detects hand gestures in a frame and returns the recognized gesture.
    """
    h, w, c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
            return get_gesture(landmarks, w, h)
    
    return "None"
