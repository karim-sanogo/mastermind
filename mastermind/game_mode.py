from mastermind.logic import Mastermind
from mastermind.terminal_ui import TerminalUI
import os


class GameMode:
    def singleplayer(self, bot_assistance):
        ui = TerminalUI(bot_assistance=bot_assistance)
        # Prompts the player for their name and welcomes them
        player_name = ui.get_player_name()
        print(f"\nWelcome to Mastermind, {player_name}!\n")
        ui.play_terminal()      # Starts the singleplayer game

    def twoplayer(self):
        game = Mastermind()
        ui = TerminalUI(game)

        # Getting names of the players and setting up the game for the Codemaker and Codebreaker
        print("\nCodemaker:")
        codemaker_name = ui.get_player_name()
        print("\nCodebreaker:")
        codebreaker_name = ui.get_player_name()
        print(f"\n\nWelcome Codemaker {codemaker_name} and Codebreaker {codebreaker_name}!\n")

        custom_code = ui.get_codemaker_code()       # Using the new method in TerminalUI
        game.code_cpu = custom_code     # Setting the custom code as the CPU's code

        os.system('cls')    # clears Terminal so that the Codebreaker can't see the Codemaker's code

        print ("The Codemaker has chosen his code. Now it's your turn, Codebreaker!\n")
        ui.play_terminal()      # Starts the two-player game
