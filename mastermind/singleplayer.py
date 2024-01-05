from mastermind.terminal_ui import TerminalUI


def singleplayer(bot_assistance):
    ui = TerminalUI(bot_assistance=bot_assistance)
    player_name = ui.get_player_name()
    print(f"\nWelcome to Mastermind, {player_name}!\n")
    
    # Initialisieren des TerminalUI-Objekts mit dem aktuellen Status der Bot-Unterstützung
    ui.play_terminal()