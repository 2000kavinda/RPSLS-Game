import tkinter as tk
import subprocess
from PIL import Image, ImageTk

def show_loading_and_start_game(command, button, original_text):
    
    button.config(text="Loading...", state="disabled")
        
    root.after(10000, lambda: button.config(text=original_text, state="normal"))  
    
    root.after(10000, lambda: subprocess.call(command))  

def start_game_two_hands():
    original_text = button_two_hands.cget("text")  
    show_loading_and_start_game(["python", "two_hands_game.py"], button_two_hands, original_text)

def start_game_single_hand():
    original_text = button_single_hand.cget("text")  
    show_loading_and_start_game(["python", "single_hand_game.py"], button_single_hand, original_text)

root = tk.Tk()
root.title("Rock Paper Scissors Lizard Spock")
root.geometry("960x540+0+0")  
root.resizable(False, False)  

bg_image = Image.open("images/background.png")  
bg_image = bg_image.resize((960, 540), Image.Resampling.LANCZOS)  
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=960, height=540)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, anchor="nw", image=bg_photo)

button_two_hands = tk.Button(root, text="Multi-player Mode", width=20, height=2, command=start_game_two_hands)
button_two_hands.place(relx=0.5, rely=0.4, anchor="center")  

button_single_hand = tk.Button(root, text="Single-player Mode", width=20, height=2, command=start_game_single_hand)
button_single_hand.place(relx=0.5, rely=0.6, anchor="center")  

root.mainloop()
