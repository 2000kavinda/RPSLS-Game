import cv2
from src.gesture_recognition import detect_hand_gesture
from src.game_logic import generate_system_choice, determine_winner
from src.image_loader import load_images

# Load images
images = load_images()

# Open webcam
cap = cv2.VideoCapture(0)

prev_user_choice = None
system_choice = generate_system_choice()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  
    user_choice = detect_hand_gesture(frame)

    if user_choice in ["Rock", "Paper", "Scissors"] and user_choice != prev_user_choice:
        system_choice = generate_system_choice()
        prev_user_choice = user_choice

    # Display system's choice image
    if system_choice in images:
        frame[100:300, 100:300] = images[system_choice]

    # Display user choice text
    cv2.putText(frame, f"Your Choice: {user_choice}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if user_choice in ["Rock", "Paper", "Scissors"]:
        result_text = determine_winner(user_choice, system_choice)
        cv2.putText(frame, result_text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

    cv2.imshow("Rock, Paper, Scissors", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
