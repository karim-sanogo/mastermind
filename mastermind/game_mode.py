from mastermind.logic import Mastermind
from mastermind.terminal_ui import TerminalUI


class GameMode:
    def singleplayer(self, bot_assistance):
        ui = TerminalUI(bot_assistance=bot_assistance)
        player_name = ui.get_player_name()
        print(f"\nWelcome to Mastermind, {player_name}!\n")
        ui.play_terminal()

    def twoplayer(self):
        # while True:
        game = Mastermind()
        ui = TerminalUI(game)
        print("\nCodemaker:")
        codemaker_name = ui.get_player_name()
        print("\nCodebreaker:")
        codebreaker_name = ui.get_player_name()
        
        print(f"\n\nWelcome Codemaker {codemaker_name} and Codebreaker {codebreaker_name}!\n")
        custom_code = ui.get_codemaker_code()  # Using the new method in TerminalUI
        game.code_cpu = custom_code
        ui.play_terminal()

            # play_again = input("Do you want to play again? (y/n): ").lower()
            # if play_again == "y":
            #     ui.game = Mastermind()
            #     break
            # elif play_again == "n":
            #     return
            # else:
            #     print("Invalid input. Please enter 'y' or 'n'.")

