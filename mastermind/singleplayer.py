from name_input import get_player_name
from terminal_ui import start_terminal_game

def singleplayer():
    print()
    player_name = get_player_name()
    print(f"\n\nWelcome to Mastermind, {player_name}!\n")
    start_terminal_game()