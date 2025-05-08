import random

choices = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]

# Generate the system's choice randomly
def generate_system_choice():
    return random.choice(choices)

# Determine the winner of the game based on the user's and system's choices
def determine_winner(user_choice, system_choice):
    if user_choice == system_choice:
        return "It's a Tie!"
    
    winning_cases = {
        "Rock": ["Scissors", "Lizard"],
        "Paper": ["Rock", "Spock"],
        "Scissors": ["Paper", "Lizard"],
        "Lizard": ["Spock", "Paper"],
        "Spock": ["Scissors", "Rock"]
    }

    if system_choice in winning_cases[user_choice]:
        return "You Win!"
    return "You Lose!"
