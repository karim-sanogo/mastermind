from mastermind import MainMenu

# Entry point of the Mastermind game
def main():
    menu = MainMenu()     # MainMenu handles the user interaction for game mode selection and bot assistance.
    menu.display_main_menu()

if __name__ == "__main__":
    main()