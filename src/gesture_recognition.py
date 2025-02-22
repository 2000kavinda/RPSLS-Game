import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1)

def preprocess_frame(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding
    _, binary = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Erosion & Dilation
    kernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=2)

    # Extract hand boundary using Canny edge detection
    edges = cv2.Canny(dilated, 100, 200)

    # Fill small gaps using Region Filling (Morphological Operations)
    filled = dilated.copy()
    h, w = filled.shape
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(filled, mask, (0, 0), 255)
    filled_inv = cv2.bitwise_not(filled)
    region_filled = dilated | filled_inv

    return region_filled

def get_gesture(landmarks, w, h):
    #*********************************Need to more improve******************************************
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

    fingers = [
        thumb_tip[0] > thumb_ip[0],  
        index_tip[1] < index_pip[1],  
        middle_tip[1] < middle_pip[1],  
        ring_tip[1] < ring_pip[1],  
        pinky_tip[1] < pinky_pip[1]  
    ]

    if all(fingers[1:]):  
        return "Paper"
    elif not any(fingers[1:]):  
        return "Rock"
    elif fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:  
        return "Scissors"
    return "Unknown"

def detect_hand_gesture(frame):
    h, w, c = frame.shape

    processed_frame = preprocess_frame(frame)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
            return get_gesture(landmarks, w, h)

    return "None"
