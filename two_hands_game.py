import cv2
from src.gesture_recognition import detect_hand_gesture
from src.game_logic import determine_winner
from src.gesture_recognition import preprocess_frame

cap = cv2.VideoCapture(0)

frame_width, frame_height = 960, 540
cv2.namedWindow("Rock, Paper, Scissors, Lizard, Spock", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Rock, Paper, Scissors, Lizard, Spock", cv2.WND_PROP_FULLSCREEN, 0)
cv2.resizeWindow("Rock, Paper, Scissors, Lizard, Spock", frame_width, frame_height)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    
    h, w, c = frame.shape
    
    gestures = detect_hand_gesture(frame)
    
    if len(gestures) == 2:  
        left_hand_gesture = gestures[0]  
        right_hand_gesture = gestures[1]  

        if left_hand_gesture == "Unknown" or right_hand_gesture == "Unknown":
            result_text = "Invalid Gesture Detected"
        else:
            result_text = determine_winner(left_hand_gesture, right_hand_gesture)
            
            if left_hand_gesture == right_hand_gesture:
                result_text = "It's a Tie!"
            else:
                if "Win" in result_text:  
                    result_text = f"{left_hand_gesture} won"
                else:
                    result_text = f"{right_hand_gesture} won"
        
        cv2.putText(frame, result_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
    
    else:
        cv2.putText(frame, "No both hands detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Apply the thresholding and resize the thresholded image for both hands
    thresholded_hand = preprocess_frame(frame)  
    small_thresholded_hand = cv2.resize(thresholded_hand, (150, 150))  
    small_thresholded_hand = cv2.cvtColor(small_thresholded_hand, cv2.COLOR_GRAY2BGR) 

    bottom_right_x = w - 170  
    bottom_right_y = h - 170  
    frame[bottom_right_y:bottom_right_y+150, bottom_right_x:bottom_right_x+150] = small_thresholded_hand  

    cv2.imshow("Rock, Paper, Scissors, Lizard, Spock", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
