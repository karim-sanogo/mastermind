from itertools import product
import random
from logic import Mastermind

class Bot():

    def __init__(self, mastermind_instance):
        self.mastermind = mastermind_instance
        self.possible_codes = {}
        self.correct_position, self.incorrect_position = self.mastermind.color_check(count_round=False)
        self.code_range = self.mastermind.code_range
        self.code_length = self.mastermind.code_length
        self.code_cpu = self.mastermind.code_cpu
        self.code_user = self.mastermind.code_user
        self.bot_pick = {}

    def possible_codes_dict(self, allow_duplicates=False):

        #---------------- die product funktion generiert eine Menge mit allen Tupeln, die sich aus code_range und code_lenght, diese ist aber nicht subscriptable, daher die Umwandlung in eine Liste
        possible_codes = [i for i in product(self.code_range, repeat=self.code_length)]

        #------ Es wird ein nested dictionary erstellt, das auf der ersten Ebene einen Key mit dem Namen "Code {i+1}" für jedes in possible_codes enthaltenes Tupel. Diesem Key wird ein leeres dictionary zugeordnet. Auf der zweiten Ebene wird für jedes Element in einem dieser Tupel ein Key mit dem Namen "Space {j+1}" erzeugt und ihm der Wert des entsprechenden Elementes zugewiesen.
        #------ multi_color_key speichert keys zu Codes, in denen Farben mehfach verwendet
        #------ used_colors speichert Farben, die in einem Code bereits verwendet wurden
        possible_codes_dict = {}
        multi_color_key = set()
        for i in range(len(possible_codes)):
            possible_codes_dict[f"Code {i+1}"]={}
            used_colors = set()
            for j in range(self.code_length):
                possible_codes_dict[f"Code {i+1}"][f"Space {j+1}"]=possible_codes[i][j]
                if allow_duplicates == False:
                    if possible_codes[i][j] not in used_colors:
                        used_colors.add(possible_codes[i][j])
                    else:
                        multi_color_key.add(f"Code {i+1}")

        #------- if Abfrage, die die in multi_color_keys gespeicherten Keys aus dem possible_codes_dict löscht, falls keine Mehrfachfarben erlaubt sind                 
        if allow_duplicates == False:
            for key in multi_color_key:
                del possible_codes_dict[key]

        self.possible_codes = possible_codes_dict


    def act_possible_codes(self):
        wrong_codes = set()
        for code_name, code in self.possible_codes.items():
            if Mastermind.color_check(self.code_user, code) != self.correct_position:
                wrong_codes.add(code_name)
        for key in wrong_codes:
            del self.possible_codes[key]

    # def act_possible_codes(self):
    #     wrong_codes = set()   
    #     for code in self.possible_codes:
    #         if Mastermind.color_check(self.code_user, self.code_cpu) != Mastermind.color_check(self.code_user, self.code_cpu[code]):
    #             wrong_codes.add(code)
    #     for key in wrong_codes:
    #         del self.possible_codes[key]


    ###--- Funktion wählt einen zufälligen code aus possible_codes als pick aus

    def code_bot(self):
        # Stellen Sie sicher, dass self.possible_codes initialisiert ist
        if not self.possible_codes:
            self.possible_codes_dict()

        # Wählen Sie einen zufälligen Code aus den möglichen Codes
        pick = random.choice(list(self.possible_codes.values()))
        return pick