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

# Set window size
frame_width, frame_height = 960, 540
cv2.namedWindow("Rock, Paper, Scissors, Lizard, Spock", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Rock, Paper, Scissors, Lizard, Spock", cv2.WND_PROP_FULLSCREEN, 0)
cv2.resizeWindow("Rock, Paper, Scissors, Lizard, Spock", frame_width, frame_height)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Get frame dimensions
    h, w, c = frame.shape

    # Detect user hand gesture
    user_choice = detect_hand_gesture(frame)

    # Update system choice if user changes their gesture
    if user_choice in ["Rock", "Paper", "Scissors", "Lizard", "Spock"] and user_choice != prev_user_choice:
        system_choice = generate_system_choice()
        prev_user_choice = user_choice

    # Display system's choice image
    if system_choice in images:
        system_image = images[system_choice]
        system_image = cv2.resize(system_image, (150, 150))
        frame[20:170, w-170:w-20] = system_image

    # Display user choice text
    cv2.putText(frame, f"Your Choice: {user_choice}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display result if valid choice
    if user_choice in ["Rock", "Paper", "Scissors", "Lizard", "Spock"]:
        result_text = determine_winner(user_choice, system_choice)
        cv2.putText(frame, result_text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

    # Display the frame
    cv2.imshow("Rock, Paper, Scissors, Lizard, Spock", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
