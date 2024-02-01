from mastermind.game_mode import GameMode


class MainMenu:
    def __init__(self):
        self.bot_assistance = False     # Determines whether the bot assistance is enabled in singleplayer mode
        self.game_mode = GameMode()     # Instance of the GameMode class to handle different game modes like singleplayer and two player


    # Displays the main menu and handles the user interaction
    def display_main_menu(self):
        while True:
            print(f"""
Welcome to MASTERMIND

Please select one of the following options:

[1] Singleplayer
[2] Two Player
[3] Toggle Bot Assistance for SP (Currently: {"ON" if self.bot_assistance else "OFF"})
[4] Quit Game
            """)

            choice = input("Enter your choice: ")
            if choice == "1":
                self.game_mode.singleplayer(self.bot_assistance)
            elif choice == "2":
                self.game_mode.twoplayer()
            elif choice == "3":
                self.toggle_bot_assistance()    # Toggles the bot assistance option for singleplayer mode
            elif choice == "4":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

    # Switches the state of bot assistance and informs the user
    def toggle_bot_assistance(self):
        self.bot_assistance = not self.bot_assistance
        status = "enabled" if self.bot_assistance else "disabled"
        print(f"\nBot assistance has been {status}.")