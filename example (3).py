
import random

user_score = 0
computer_score = 0
chances = 3

print(">>> Let's begin the game <<<\n")
print("Remember, you only have three chances. GOOD LUCK!\n")
print("You can type 'quit' to log out of the game.\n")

options = ["rock", "paper", "scissor"]

while chances > 0:
    user = input("Please insert your choice (rock, paper, or scissor)\n:").strip().lower()

    if user == "quit":
        print(">>> Game over, you quit <<<")
        break

    if user not in options:
        print("Invalid input. Please choose 'rock', 'paper', or 'scissor'.")
        continue

    computer = random.choice(options)
    print(f"You chose '{user}', computer chose '{computer}'.")

    if user == computer:
        print(f"It's a draw! Both computer and user chose '{user}'.")
    elif (user == "rock" and computer == "scissor") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissor" and computer == "paper"):
        print("You won! You gain a point.")
        user_score += 1
        
    else:
        print("You lost. Computer wins this round.")
        computer_score += 1
        
    chances -= 1
    print(f"Remaining chances: {chances}\n")

if chances == 0:
    print(f"\n>>> Game over <<<\nYour score: {user_score} | Computer's score: {computer_score}")
    if user_score > computer_score:
        print("GREAT JOB, YOU HAVE WON THE GAME!")
    elif user_score < computer_score:
        print("YOU LOST. BETTER LUCK NEXT TIME.")
    else:
        print("	IT'S A TIE!")

    
    
        
    
    
        
    
    
