import random

def generate_system_choice():
    return random.choice(["Rock", "Paper", "Scissors"])

def determine_winner(user_choice, system_choice):
    if user_choice == system_choice:
        return "It's a Tie!"
    elif (user_choice == "Rock" and system_choice == "Scissors") or \
         (user_choice == "Scissors" and system_choice == "Paper") or \
         (user_choice == "Paper" and system_choice == "Rock"):
        return "You Win!"
    return "System Wins!"
