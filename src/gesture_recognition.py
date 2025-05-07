import math
import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2)

def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=2)
    edges = cv2.Canny(dilated, 100, 200)
    filled = dilated.copy()
    h, w = filled.shape
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(filled, mask, (0, 0), 255)
    filled_inv = cv2.bitwise_not(filled)
    region_filled = dilated | filled_inv
    return region_filled

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def calculate_angle(a, b, c):
    ab = (b[0] - a[0], b[1] - a[1])  
    bc = (c[0] - b[0], c[1] - b[1])  
    dot_product = ab[0] * bc[0] + ab[1] * bc[1]  
    mag_ab = math.sqrt(ab[0]**2 + ab[1]**2) 
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2) 
    if mag_ab == 0 or mag_bc == 0:
        return 0 
    cos_theta = dot_product / (mag_ab * mag_bc)
    cos_theta = max(-1, min(1, cos_theta))
    angle = math.degrees(math.acos(cos_theta))
    return angle

def get_gesture(landmarks, w, h):
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    thumb_mcp = landmarks[2]
    index_tip = landmarks[8]
    index_pip = landmarks[6]
    index_mcp = landmarks[5]
    middle_tip = landmarks[12]
    middle_pip = landmarks[10]
    middle_mcp = landmarks[9]
    ring_tip = landmarks[16]
    ring_pip = landmarks[14]
    ring_mcp = landmarks[13]
    pinky_tip = landmarks[20]
    pinky_pip = landmarks[18]
    pinky_mcp = landmarks[17]
    wrist = landmarks[0]  

    gap_middle_ring = calculate_distance(middle_tip, ring_tip)
    gap_index_middle = calculate_distance(index_tip, middle_tip)
    gap_ring_pinky = calculate_distance(ring_tip, pinky_tip)

    angle_index = calculate_angle(index_mcp, index_pip, index_tip)
    angle_middle = calculate_angle(middle_mcp, middle_pip, middle_tip)
    angle_ring = calculate_angle(ring_mcp, ring_pip, ring_tip)
    angle_pinky = calculate_angle(pinky_mcp, pinky_pip, pinky_tip)
    angle_thumb = calculate_angle(thumb_mcp, thumb_ip, thumb_tip)

    fingers = [
        angle_thumb < 30,
        angle_index < 30,
        angle_middle < 30, 
        angle_ring < 30, 
        angle_pinky < 30 
    ]

    if  fingers[0] and fingers[1] and fingers[2] and  fingers[3] and  fingers[4]:  
        if gap_middle_ring > gap_index_middle * 1.5 and gap_middle_ring > gap_ring_pinky * 1.5:
            return "Spock"  
        return "Paper" 
    elif not any(fingers[1:]):
        if thumb_tip[1]>index_tip[1]:
            return "Lizard"
        return "Rock" 
    elif not fingers[0] and fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:  
        return "Scissors" 

    return "Unknown"

def detect_hand_gesture(frame):
    h, w, c = frame.shape
    processed_frame = preprocess_frame(frame)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    
    gestures = []  # List to hold the gestures of all detected hands
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
            gesture = get_gesture(landmarks, w, h)
            gestures.append(gesture)  # Append the gesture for each hand detected

    return gestures  # Return a list of gestures for all detected hands
