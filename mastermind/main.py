from logic import Mastermind

# Start the game loop
game_terminal = Mastermind()
while True:
    game_terminal.play_terminal()
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again == "n":
        break
    elif play_again == "y":
        game_terminal = Mastermind() # Reset the game state