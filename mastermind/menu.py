from singleplayer import singleplayer
from twoplayer import twoplayer

def main_menu():
    while True:
        print("""
        Welcome to MASTERMIND

        Please select one of the following options:

        [1] Singleplayer
        [2] Two Player
        [3] Quit Game
        """)

        choice = input("Enter your choice: ")
        if choice == "1":
            singleplayer()
        elif choice == "2":
            twoplayer()
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()