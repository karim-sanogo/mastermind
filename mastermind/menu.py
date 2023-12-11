from singleplayer import singleplayer
from twoplayer import twoplayer

def main_menu():
    while True:
        print(f"""
        Welcome to MASTERMIND

        Please select one of the following options:

        [1] Singleplayer
        [2] Two Player
        [3] Toggle Bot Assistance for 1p (Currently: {"ON" if bot_assistance else "OFF"})
        [4] Quit Game
        """)

        choice = input("Enter your choice: ")
        if choice == "1":
            singleplayer()
        elif choice == "2":
            twoplayer()
        elif choice == "3":
            toggle_bot_assistance()
        elif choice == "4":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()


bot_assistance = False

def toggle_bot_assistance():
    global bot_assistance
    bot_assistance = not bot_assistance
    status = "enabled" if bot_assistance else "disabled"
    print(f"Bot assistance has been {status}.")