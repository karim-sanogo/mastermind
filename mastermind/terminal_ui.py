from logic import Mastermind

class TerminalUI:
    def __init__(self, game=None):
        self.game = game if game is not None else Mastermind()

    def user_pick(self):
        menu_string = "Please select colors from list:\n"
        for i in range(1, len(self.game.color_menu) + 1, 2):
            first_color = f"[{i}] {self.game.color_menu[i].title()}"
            second_color = f"[{i + 1}] {self.game.color_menu[i + 1].title()}"
            menu_string += f"  {first_color:15} {second_color}\n"
        print(menu_string)

        for space in self.game.code_user:
            if self.game.code_user[space] is None:
                while True:
                    user_input = input(f"Please select a color for {space}: ")
                    if self.game.is_valid_input(user_input):
                        self.game.code_user[space] = int(user_input)
                        self.game.menu_swap()
                        break
                    else:
                        print("Invalid input. Please enter a number between 1 and 8.")

    def display_history(self):
        max_color_length = max(len(color) for color in self.game.color_menu.values())
        for round_number, (code, feedback) in enumerate(self.game.history, 1):
            code_str = ' | '.join([f"{color.title():<{max_color_length}}" for color in code.values()])
            print(f"Round {round_number}: {code_str} - Correct: {feedback[0]}, Incorrect: {feedback[1]}")

    def play_terminal(self):
        self.game.cpu_pick()
        print(f"\nThe CPU's code is {', '.join(self.game.code_cpu.values()).title()}\n")
        
        for _ in range(1, self.game.tries + 1):
            self.user_pick()
            correct_position, incorrect_position = self.game.color_check()
            print()
            self.game.add_to_history(self.game.code_user, (correct_position, incorrect_position))

            self.display_history()
            if correct_position == 4:
                print(f"\nYou won in {self.game.round} tries!\n")
                break

            print(f"\nYou have {self.game.tries - self.game.round} tries left.\n")

            self.game.code_user = self.game.code_build().copy()
        else:
            print(f"You lost! The correct colors were: {', '.join(self.game.code_cpu.values()).title()}")
    

def start_terminal_game():
    ui = TerminalUI()
    while True:
        ui.play_terminal()
        while True:
            play_again = input("Do you want to play again? (y/n): ").lower()
            if play_again == "y":
                ui.game = Mastermind()
                break
            elif play_again == "n":
                return
            else:
                print("Invalid input. Please enter 'y' or 'n'.")