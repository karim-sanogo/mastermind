from itertools import product
import copy
import random
from mastermind.logic import Mastermind


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

    def possible_codes_dict(self, allow_duplicates=True):

        #--de------------ die product funktion generiert eine Menge mit allen Tupeln, die sich aus code_range und code_lenght, diese ist aber nicht subscriptable, daher die Umwandlung in eine Liste
        #--en------------ the product function generates a set with all tuples resulting from code_range and code_lenght, but this is not subscriptable, hence the conversion to a list
        possible_codes = [i for i in product(self.code_range, repeat=self.code_length)]

        #--de-- Es wird ein nested dictionary erstellt, das auf der ersten Ebene einen Key mit dem Namen "Code {i+1}" für jedes in possible_codes enthaltenes Tupel. Diesem Key wird ein leeres dictionary zugeordnet. Auf der zweiten Ebene wird für jedes Element in einem dieser Tupel ein Key mit dem Namen "Space {j+1}" erzeugt und ihm der Wert des entsprechenden Elementes zugewiesen.
        #------ multi_color_key speichert keys zu Codes, in denen Farben mehfach verwendet
        #------ used_colors speichert Farben, die in einem Code bereits verwendet wurden
        #--en-- A nested dictionary is created that contains a key with the name "Code {i+1}" on the first level for each tuple contained in possible_codes. An empty dictionary is assigned to this key. At the second level, a key with the name "Space {j+1}" is created for each element in one of these tuples and the value of the corresponding element is assigned to it.
        #------ multi_color_key stores keys for codes in which colors are used multiple times.
        #------ used_colors saves colors that have already been used in a code
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

        #--de--- if Abfrage, die die in multi_color_keys gespeicherten Keys aus dem possible_codes_dict löscht, falls keine Mehrfachfarben erlaubt sind
        #--en--- if query that deletes the keys stored in multi_color_keys from the possible_codes_dict if no multiple colors are allowed
        if allow_duplicates == False:
            for key in multi_color_key:
                del possible_codes_dict[key]

        self.possible_codes = possible_codes_dict
        # print("possible_codes erstellt; Länge:", len(self.possible_codes)) #------------------for Testing
        #print(self.possible_codes)------------------------------------------------------For Testing


    def act_possible_codes(self, pick_user):
        wrong_codes = set()

        # print(f"correct, incorrect:{Mastermind.check}") #----------------------------------for Testing
        # print(f"Usercode: {pick_user}") #----------------------------------for Testing
        # print(f"CPU-Code: {self.code_cpu}") #----------------------------------for Testing
        for code in self.possible_codes:
            mastercode = copy.deepcopy(self.possible_codes[code])
            pick = copy.deepcopy(pick_user)
            correct_position_bot = 0
            incorrect_position_bot = 0
            for key in mastercode:
                if mastercode[key] == pick[key]:
                    correct_position_bot += 1
                    mastercode[key] = "++"
                    pick[key] = "--"
                
            for key_m in mastercode:
                for key_b in pick:
                    if mastercode[key_m] == pick[key_b]:
                        incorrect_position_bot += 1
                        mastercode[key_m] = "+"
                        pick[key_b] = "-"
            
            if (correct_position_bot, incorrect_position_bot) != Mastermind.check:
                wrong_codes.add(code)
        
        for key in wrong_codes:
            del self.possible_codes[key]

        # print("possible_codes aktualisiert; Länge:", len(self.possible_codes)) #------------------for Testing
        # print(f"Mastercode: {mastercode}")---------------------------------------------------for Testing

    ###-de- Funktion wählt einen zufälligen code aus possible_codes als pick aus
    ###-en- Function selects a random code from possible_codes as pick

    def code_bot(self):
        #--de-- Stellen Sie sicher, dass self.possible_codes initialisiert ist
        #--en-- Make sure that self.possible_codes is initialized
        if not self.possible_codes:
            self.possible_codes_dict()

        #--de-- Wählen Sie einen zufälligen Code aus den möglichen Codes
        #--en-- Select a random code from the possible codes
        pick = random.choice(list(self.possible_codes.values()))
        print(f"Bot wählt: {pick}")
        return pick