from mastermind.logic import Mastermind
from mastermind.bot import Bot


class TerminalUI:
    # Initializes the TerminalUI with a game instance and optional bot support
    def __init__(self, game=None, bot_assistance=False):
        self.game = game if game is not None else Mastermind()
        self.bot_assistance = bot_assistance
        self.bot = Bot(self.game) if bot_assistance else None

    # Allows the user to select colors for their code
    def user_pick(self):
        code_range_length = len(self.game.code_range)
        menu_string = "Please select colors from list:\n"

        # Creates and displays the color selection menu
        for i in range(1, len(self.game.color_menu) + 1, 2):
            first_color = f"[{i}] {self.game.color_menu[i].title()}"
            second_color = f"[{i + 1}] {self.game.color_menu[i + 1].title()}"
            menu_string += f"  {first_color:15} {second_color}\n"
        print(menu_string)

        # Prompting the user to select colors for each position
        for space in self.game.code_user:
            if self.game.code_user[space] is None:
                while True:
                    user_input = input(f"Please select a color for {space}: ")
                    if self.game.is_valid_input(user_input):
                        self.game.code_user[space] = int(user_input)
                        self.game.menu_swap()
                        break
                    else:
                        print(f"Invalid input. Please enter a number between 1 and {code_range_length}.")

    # Displays the history of moves to provide feedback to the user
    def display_history(self):
        max_color_length = max(len(color) for color in self.game.color_menu.values())
        for round_number, (code, feedback) in enumerate(self.game.history, 1):
            code_str = ' | '.join([f"{color.title():<{max_color_length}}" for color in code.values()])
            print(f"Round {round_number}: {code_str} - Correct: {feedback[0]}, Incorrect: {feedback[1]}")

    # Handles the gameplay in the terminal
    def play_terminal(self):
        self.game.cpu_pick()
        
        # If bot assistance is enabled, initializes the possible codes dictionary
        if self.bot_assistance:
            self.bot.possible_codes_dict()

        # print(f"\nThe CPU's code is {', '.join(self.game.code_cpu.values()).title()}\n") #---------------------------------------------------For Testing
        
        # Main loop for each attempt of the game
        for _ in range(1, self.game.tries + 1):
            player_made_choice = True
            if self.bot_assistance:
                bot_decision = input("Do you want to use the bot's pick for this round? (y/n): ").lower()
                if bot_decision == 'y':
                    self.game.code_user = self.bot.code_bot()
                    player_made_choice = False

            # User makes a choice if bot assistance is not used or declined for the round
            if player_made_choice:
                self.user_pick()

            correct_position, incorrect_position = self.game.color_check()

            # Update the bot's dictionary of possible codes based on the latest feedback
            if self.bot_assistance:
                self.bot.act_possible_codes(self.game.code_user)
            print()
            self.game.add_to_history(self.game.code_user, (correct_position, incorrect_position))

            self.display_history()

            # Check if the user has guessed the correct code
            if correct_position == Mastermind().code_length:
                print(f"\nYou won in {self.game.round} tries!\n")
                break

            print(f"\nYou have {self.game.tries - self.game.round} tries left.\n")

            # Reset the user's code for the next attempt
            self.game.code_user = self.game.code_build().copy()
        else:
            print(f"You lost! The correct colors were: {', '.join(self.game.code_cpu.values()).title()}")
    
    def get_player_name(self):

        # Asks the player for their name and returns it.
        while True:
            name = input("Please enter your name: ").strip()
            if name:
                return name
            else:
                print("Name cannot be empty. Please enter a valid name.")
    
    # Allows the Codemaker to set up a custom code in two-player mode
    def get_codemaker_code(self):
        code = {}
        menu_string = "CODEBREAKER PLEASE LOOK AWAY!\n\nCodemaker, please select colors for the code:\n"
        for i in range(1, len(self.game.color_menu) + 1, 2):
            first_color = f"[{i}] {self.game.color_menu[i].title()}"
            second_color = f"[{i + 1}] {self.game.color_menu[i + 1].title()}"
            menu_string += f"  {first_color:15} {second_color}\n"
        print(menu_string)

        # Codemaker selects colors for each space in the code
        for i in range(1, self.game.code_length + 1):
            while True:
                user_input = input(f"Select a color for Space {i}: ")
                if self.game.is_valid_input(user_input):
                    code[f"Space {i}"] = self.game.color_menu[int(user_input)]
                    break
                else:
                    print("\nInvalid input. Please enter a number from the menu.")
        return code