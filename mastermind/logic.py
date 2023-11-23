import random

class Mastermind:
    def __init__(self):
        self.code_range = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white"]
        self.round = 0
        self.tries = 9
        self.code_length = 4
        self.code_cpu = self.code_build().copy()
        self.code_user = self.code_build().copy()
        self.color_menu = {index + 1: color for index, color in enumerate(self.code_range)}

    def code_build(self):
        return {f"Space {i+1}": None for i in range(self.code_length)}

    def cpu_pick(self, allow_duplicates=True):
        used_colors = set()
        for key in self.code_cpu:
            if self.code_cpu[key] is None:
                if allow_duplicates:
                    color = random.choice(self.code_range)
                else:
                    color = random.choice([c for c in self.code_range if c not in used_colors])
                    used_colors.add(color)
                self.code_cpu[key] = color

    def menu_swap(self):
        for space, color_keys in self.code_user.items():
            if color_keys in self.color_menu:
                self.code_user[space] = self.color_menu[color_keys]

    def is_valid_input(self, user_input):
        try:
            return 1 <= int(user_input) <= len(self.color_menu)
        except ValueError:
            return False

    def user_pick(self):
        menu_string = "Please select colors from list:\n"
        for i in range(1, len(self.color_menu) + 1, 2):
            first_color = f"[{i}] {self.color_menu[i].title()}"
            second_color = f"[{i + 1}] {self.color_menu[i + 1].title()}"
            menu_string += f"  {first_color:15} {second_color}\n"
        print(menu_string)

        for space in self.code_user:
            if self.code_user[space] is None:
                while True:
                    user_input = input(f"Please select a color for {space}: ")
                    if self.is_valid_input(user_input):
                        self.code_user[space] = int(user_input)
                        self.menu_swap()
                        break
                    else:
                        print("Invalid input. Please enter a number between 1 and 8.")

    def color_check(self):
        self.round += 1
        color_match_cpu = {}
        color_match_user = {}
        correct_position = 0 
        incorrect_position = 0   

        for color in self.code_cpu.values():
            color_match_cpu[color] = color_match_cpu.get(color, 0) + 1

        for space in self.code_user:
            user_color = self.code_user[space]
            cpu_color = self.code_cpu[space]
            color_match_user[user_color] = color_match_user.get(user_color, 0) + 1
            
            if user_color == cpu_color:
                correct_position += 1
                color_match_cpu[cpu_color] -= 1

        for user_color, count in color_match_user.items():
            incorrect_position += min(count, color_match_cpu.get(user_color, 0))

        return correct_position, incorrect_position

    def play_terminal(self):
        self.cpu_pick()
        print(">>> Welcome to Mastermind! <<<\n")
        print(f"The CPU's code is {', '.join(self.code_cpu.values()).title()}\n")
        
        for _ in range(1, self.tries + 1):
            self.user_pick()
            correct_position, incorrect_position = self.color_check()
            if correct_position == 4:
                print(f"\nYou won in {self.round} tries!\n")
                break
            print(f"\nCorrect position: {correct_position}")
            print(f"Incorrect position: {incorrect_position}\n")
            print(f"You have {self.tries - self.round} tries left.\n")

            self.code_user = self.code_build().copy()
        else:
            print(f"You lost! The correct colors were: {', '.join(self.code_cpu.values()).title()}")