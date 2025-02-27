import math
import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1)

def preprocess_frame(frame):
    """
    Preprocess the input frame for better hand detection.
    Includes grayscale conversion, thresholding, morphological operations.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding
    _, binary = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Erosion & Dilation to remove noise
    kernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=2)

    # Edge Detection
    edges = cv2.Canny(dilated, 100, 200)

    # Region Filling (Morphological Closing)
    filled = dilated.copy()
    h, w = filled.shape
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(filled, mask, (0, 0), 255)
    filled_inv = cv2.bitwise_not(filled)
    region_filled = dilated | filled_inv

    return region_filled

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


import math

def calculate_angle(a, b, c):
    """
    Calculate the angle (in degrees) between three points.
    Ensures cos_theta remains within valid range [-1, 1].
    """
    ab = (b[0] - a[0], b[1] - a[1])  # Vector AB
    bc = (c[0] - b[0], c[1] - b[1])  # Vector BC

    dot_product = ab[0] * bc[0] + ab[1] * bc[1]  # Dot product
    mag_ab = math.sqrt(ab[0]**2 + ab[1]**2)  # Magnitude of AB
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)  # Magnitude of BC

    if mag_ab == 0 or mag_bc == 0:
        return 0  # Avoid division by zero (returns 0°)

    cos_theta = dot_product / (mag_ab * mag_bc)  # Cosine rule

    # 🔹 Ensure cos_theta is in the range [-1, 1] to avoid math domain error
    cos_theta = max(-1, min(1, cos_theta))

    angle = math.degrees(math.acos(cos_theta))  # Convert to degrees
    return angle

def get_gesture(landmarks,w,h):
    """
    Identify the hand gesture based on finger positions and angles.
    """
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

    wrist = landmarks[0]  # Base of the hand

    # Calculate distances between fingers
    gap_middle_ring = calculate_distance(middle_tip, ring_tip)
    gap_index_middle = calculate_distance(index_tip, middle_tip)
    gap_ring_pinky = calculate_distance(ring_tip, pinky_tip)

    # Calculate angles for each finger
    angle_index = calculate_angle(index_mcp, index_pip, index_tip)
    angle_middle = calculate_angle(middle_mcp, middle_pip, middle_tip)
    angle_ring = calculate_angle(ring_mcp, ring_pip, ring_tip)
    angle_pinky = calculate_angle(pinky_mcp, pinky_pip, pinky_tip)
    angle_thumb = calculate_angle(thumb_mcp, thumb_ip, thumb_tip)

    # Determine if fingers are extended based on angles
    fingers = [
        #thumb_tip[0] > thumb_ip[0],  # Thumb extended (left/right check)
        angle_thumb < 30,
        angle_index < 30,  # Index finger extended
        angle_middle < 30,  # Middle finger extended
        angle_ring < 30,  # Ring finger extended
        angle_pinky < 30  # Pinky finger extended
    ]

    # Gesture Recognition
    if  fingers[0] and fingers[1] and fingers[2] and  fingers[3] and  fingers[4]:  
        if gap_middle_ring > gap_index_middle * 1.5 and gap_middle_ring > gap_ring_pinky * 1.5:
            return "Spock"  
        return "Paper"  # All fingers extended
    elif not any(fingers[1:]):
        if thumb_tip[1]>index_tip[1]:
            return "Lizard"
        return "Rock"  # No fingers extended
    elif not fingers[0] and fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:  
        return "Scissors"  # Only index & middle extended
    

    return "Unknown"


def detect_hand_gesture(frame):
    """
    Detect the hand and recognize its gesture.
    """
    h, w, c = frame.shape

    # Preprocess the frame for better detection
    processed_frame = preprocess_frame(frame)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

            return get_gesture(landmarks, w, h)

    return "None"
