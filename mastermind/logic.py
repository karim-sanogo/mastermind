import random

class Mastermind:
    check = (0, 0)      # Stores the results of the color match check between user's guess and the actual code

    def __init__(self):
        self.code_range = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white"]        # Defines the available colors in the game
        self.round = 0      # Tracks the current round of the game
        self.tries = 9      # Sets the maximum number of attempts for the user
        self.code_length = 4        # The length of the secret code to be guessed
        self.color_menu = {index + 1: color for index, color in enumerate(self.code_range)}     # Maps color choices to menu numbers for user selection
        self.history = []       # A list to keep track of the history of moves

        # Initializes the secret code and the user's code as empty dictionaries
        self.code_cpu = self.code_build().copy()
        self.code_user = self.code_build().copy()

    def code_build(self):
        # Generates an empty code structure based on the code length
        return {f"Space {i+1}": None for i in range(self.code_length)}

    def cpu_pick(self, allow_duplicates=True):
        # CPU randomly selects colors for the code, with an option to allow duplicates
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
        # Converts color indices in the user's code to their corresponding color names
        for space, color_index in self.code_user.items():
            if color_index in self.color_menu:
                self.code_user[space] = self.color_menu[color_index]

    def is_valid_input(self, user_input):
        # Checks if the user's input is a valid menu number
        try:
            return 1 <= int(user_input) <= len(self.color_menu)
        except ValueError:
            return False

    def color_check(self, count_round=True):
        # Compares user's guess with the CPU's code to determine correct and misplaced colors
        if count_round:
            self.round += 1
        color_match_cpu = {}
        correct_position = 0 
        incorrect_position = 0   

        # Counting how many times each color appears in the CPU's code
        for color in self.code_cpu.values():
            color_match_cpu[color] = color_match_cpu.get(color, 0) + 1

        # Checks for colors in the correct position
        for space in self.code_user:
            user_color = self.code_user[space]
            cpu_color = self.code_cpu[space]
            if user_color == cpu_color:
                correct_position += 1
                color_match_cpu[cpu_color] -= 1

        # Checking for misplaced but existing colors
        for space in self.code_user:
            user_color = self.code_user[space]
            cpu_color = self.code_cpu[space]
            if user_color != cpu_color and color_match_cpu.get(user_color, 0) > 0:
                incorrect_position += 1
                color_match_cpu[user_color] -= 1

        # Storing the results in the class variable 'check'
        Mastermind.check = (correct_position, incorrect_position)
        return correct_position, incorrect_position
    
    def add_to_history(self, code_user, feedback):
        # Adds the current move to the game history
        self.history.append((code_user.copy(), feedback))
        
    def get_game_status(self):
        # Returns the current status of the game
        return {
            "cpu_code": self.code_cpu,
            "user_code": self.code_user,
            "round": self.round,
            "tries": self.tries
        }
    
