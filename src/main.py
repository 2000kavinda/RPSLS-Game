import cv2
from src.gesture_recognition import detect_hand_gesture
from src.game_logic import generate_system_choice, determine_winner
from src.image_loader import load_images

images = load_images()

cap = cv2.VideoCapture(0)

prev_user_choice = None
system_choice = generate_system_choice()

screen_width = 1920 
screen_height = 1080

frame_width = int(screen_width * 0.5)
frame_height = int(screen_height * 0.5)

cv2.namedWindow("RPS Game", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("RPS Game", cv2.WND_PROP_FULLSCREEN, 0)  
cv2.resizeWindow("RPS Game", frame_width, frame_height)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  

    h, w, c = frame.shape

    user_choice = detect_hand_gesture(frame)

    if user_choice in ["Rock", "Paper", "Scissors"] and user_choice != prev_user_choice:
        system_choice = generate_system_choice()
        prev_user_choice = user_choice

    if system_choice in images:
        system_image = images[system_choice]
        system_image = cv2.resize(system_image, (150, 150))

        frame[20:170, w-170:w-20] = system_image

    cv2.putText(frame, f"Your Choice: {user_choice}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if user_choice in ["Rock", "Paper", "Scissors"]:
        result_text = determine_winner(user_choice, system_choice)
        cv2.putText(frame, result_text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

    cv2.imshow("RPS Game", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
