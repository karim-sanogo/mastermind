from name_input import get_player_name
from terminal_ui import TerminalUI
import menu  

def singleplayer():
    player_name = get_player_name()
    print(f"\nWelcome to Mastermind, {player_name}!\n")
    
    # Initialisieren des TerminalUI-Objekts mit dem aktuellen Status der Bot-Unterstützung
    ui = TerminalUI(bot_assistance=menu.bot_assistance)
    ui.play_terminal()