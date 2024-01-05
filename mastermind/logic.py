import random

class Mastermind:
    # Klassenvariable, um die Ergebnisse der Farbüberprüfung zu speichern
    check = (0, 0)
     
    def __init__(self):
        # Initialisierung der Mastermind-Klasse mit notwendigen Attributen
        # Liste der verfügbaren Farben im Spiel
        self.code_range = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white"]
        self.round = 0  # Aktuelle Spielrunde
        self.tries = 9  # Maximale Anzahl an Versuchen
        self.code_length = 4  # Länge des zu erratenden Codes
        # Erstellen des Geheimcodes und des Benutzercodes als leere Wörterbücher
        self.code_cpu = self.code_build().copy()
        self.code_user = self.code_build().copy()
        # Zuordnung von Farben zu Menünummern für die Benutzerauswahl
        self.color_menu = {index + 1: color for index, color in enumerate(self.code_range)}
        self.history = []  # Liste für die Historie der Spielzüge

    def code_build(self):
        # Erzeugen eines leeren Codes basierend auf der Code-Länge
        return {f"Space {i+1}": None for i in range(self.code_length)}

    def cpu_pick(self, allow_duplicates=True):
        # CPU wählt zufällige Farben für den Code, mit oder ohne Duplikate
        used_colors = set()
        for key in self.code_cpu:
            if self.code_cpu[key] is None:
                if allow_duplicates:
                    color = random.choice(self.code_range)
                else:
                    # Wählen einer Farbe, die noch nicht verwendet wurde
                    color = random.choice([c for c in self.code_range if c not in used_colors])
                    used_colors.add(color)
                self.code_cpu[key] = color

    def menu_swap(self):
        # Ersetzen der Farbnummern im Benutzercode durch tatsächliche Farbnamen
        for space, color_index in self.code_user.items():
            if color_index in self.color_menu:
                self.code_user[space] = self.color_menu[color_index]

    def is_valid_input(self, user_input):
        # Überprüft, ob die Benutzereingabe eine gültige Nummer im Farbmenü ist
        try:
            return 1 <= int(user_input) <= len(self.color_menu)
        except ValueError:
            return False

    def color_check(self, count_round=True):
        # Überprüfen der Übereinstimmung zwischen Benutzer- und CPU-Code
        if count_round:
            self.round += 1
        color_match_cpu = {}
        correct_position = 0 
        incorrect_position = 0   

        # Zählt, wie oft jede Farbe im CPU-Code vorkommt
        for color in self.code_cpu.values():
            color_match_cpu[color] = color_match_cpu.get(color, 0) + 1

        # Überprüft Farben in korrekter Position und aktualisiert Zähler
        for space in self.code_user:
            user_color = self.code_user[space]
            cpu_color = self.code_cpu[space]
            if user_color == cpu_color:
                correct_position += 1
                color_match_cpu[cpu_color] -= 1

        # Überprüfen der inkorrekt positionierten, aber vorhandenen Farben
        for space in self.code_user:
            user_color = self.code_user[space]
            cpu_color = self.code_cpu[space]
            if user_color != cpu_color and color_match_cpu.get(user_color, 0) > 0:
                incorrect_position += 1
                color_match_cpu[user_color] -= 1

        # Speichern der Ergebnisse in der Klassenvariable 'check'
        Mastermind.check = (correct_position, incorrect_position)
        return correct_position, incorrect_position
    
    def add_to_history(self, code_user, feedback):
        # Fügt den aktuellen Spielzug zur Spielhistorie hinzu
        self.history.append((code_user.copy(), feedback))
        
    def get_game_status(self):
        # Gibt den aktuellen Status des Spiels zurück
        return {
            "cpu_code": self.code_cpu,
            "user_code": self.code_user,
            "round": self.round,
            "tries": self.tries
        }
    
