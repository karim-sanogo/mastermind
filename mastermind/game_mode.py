from mastermind.logic import Mastermind
from mastermind.terminal_ui import TerminalUI


def singleplayer(bot_assistance):
    ui = TerminalUI(bot_assistance=bot_assistance)
    player_name = ui.get_player_name()
    print(f"\nWelcome to Mastermind, {player_name}!\n")
    
    # Initialisieren des TerminalUI-Objekts mit dem aktuellen Status der Bot-Unterstützung
    ui.play_terminal()


def get_codemaker_code(game):
    code = {}
    menu_string = "CODEBREAKER PLEASE LOOK AWAY!\n\nCodemaker, please select colors for the code:\n"
    for i in range(1, len(game.color_menu) + 1, 2):
        first_color = f"[{i}] {game.color_menu[i].title()}"
        second_color = f"[{i + 1}] {game.color_menu[i + 1].title()}"
        menu_string += f"  {first_color:15} {second_color}\n"
    print(menu_string)

    for i in range(1, game.code_length + 1):
        while True:
            user_input = input(f"Select a color for Space {i}: ")
            if game.is_valid_input(user_input):
                code[f"Space {i}"] = game.color_menu[int(user_input)]
                break
            else:
                print("\nInvalid input. Please enter a number from the menu.")
    return code


def twoplayer():
    while True:
        game = Mastermind()
        ui = TerminalUI(game)
        print("\nCodemaker:")
        codemaker_name = ui.get_player_name()
        print("\nCodebreaker:")
        codebreaker_name = ui.get_player_name()
        
        print(f"\n\nWelcome Codemaker {codemaker_name} and Codebreaker {codebreaker_name}!\n")


        custom_code = get_codemaker_code(game)  # Codemaker wählt den Code
        game.code_cpu = custom_code  # Setzt den benutzerdefinierten Code


        ui.play_terminal()

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == "y":
            ui.game = Mastermind()
            break
        elif play_again == "n":
            return
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
