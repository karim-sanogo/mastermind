import random

class Mastermind:

    check = (0, 0)
     
    def __init__(self):
        self.code_range = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white"]
        self.round = 0
        self.tries = 9
        self.code_length = 4
        self.code_cpu = self.code_build().copy()
        self.code_user = self.code_build().copy()
        self.color_menu = {index + 1: color for index, color in enumerate(self.code_range)}
        self.history = []

    

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
        for space, color_index in self.code_user.items():
            if color_index in self.color_menu:
                self.code_user[space] = self.color_menu[color_index]

    def is_valid_input(self, user_input):
        try:
            return 1 <= int(user_input) <= len(self.color_menu)
        except ValueError:
            return False

    def color_check(self, count_round=True):
        if count_round:
            self.round += 1
        color_match_cpu = {}
        correct_position = 0 
        incorrect_position = 0   

        # Zählen der Farben im CPU-Code
        for color in self.code_cpu.values():
            color_match_cpu[color] = color_match_cpu.get(color, 0) + 1

        # Korrekt positionierte Farben überprüfen und Zähler aktualisieren
        for space in self.code_user:
            user_color = self.code_user[space]
            cpu_color = self.code_cpu[space]
            if user_color == cpu_color:
                correct_position += 1
                color_match_cpu[cpu_color] -= 1

        # Inkorrekt positionierte Farben überprüfen
        for space in self.code_user:
            user_color = self.code_user[space]
            cpu_color = self.code_cpu[space]
            if user_color != cpu_color and color_match_cpu.get(user_color, 0) > 0:
                incorrect_position += 1
                color_match_cpu[user_color] -= 1

        Mastermind.check = (correct_position, incorrect_position)
        return correct_position, incorrect_position
    
    def add_to_history(self, code_user, feedback):
        self.history.append((code_user.copy(), feedback))
        
    def get_game_status(self):
        return {
            "cpu_code": self.code_cpu,
            "user_code": self.code_user,
            "round": self.round,
            "tries": self.tries
        }
    
