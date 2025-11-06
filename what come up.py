
import random

civilian = ["ebenezer", "selamawit", "fikadu"]
imposter = ["eyosias", "yanet"]
user_score = 0
computer_score = 0
chances = 5

print("Pick from the following names: eyosias, ebenezer, selamawit, yanet, fikadu")
print("Type 'quit' to get out of the game\n")

while chances > 0:
    user = input("Your choice: ").strip().lower()

    if user == 'quit':
        print("\nGame over! You quit.")
        exit()

    if user not in civilian + imposter:
        print("Invalid choice. Try again.\n")
        continue

    computer = random.choice(civilian + imposter)
    print("Computer chose someone")

    if user in imposter and computer in imposter:
        print("It's a tie, both picked same identity.\n")
        
    elif user in civilian and computer in civilian:
        print("It's a tie, both picked same identity.\n")
        
    elif user in civilian and computer in imposter:
        print("User won this round!\n")
        user_score += 1
        chances -= 1
    
    elif user in imposter and computer in civilian:
        print("Computer won this round.\n")
        computer_score += 1
        chances -= 1

    print(f"Chances left: {chances}")
    print(f"Score -> User: {user_score}, Computer: {computer_score}\n")

if chances== 0:
    print("\nGame over!")
    
if user_score == computer_score:
    print(f"The game is a tie! User score: {user_score}, Computer score: {computer_score}")

elif user_score > computer_score:
    print(f"User won the game! User score: {user_score}, Computer score: {computer_score}")

else:
    print(f"Computer won the game! User score: {user_score}, Computer score: {computer_score}")

    
    
    
