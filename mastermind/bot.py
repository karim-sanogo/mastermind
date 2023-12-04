from itertools import product
round=0
code_range = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white"]
code_lenght = 4

def possible_codes_dict(code_range, code_lenght, allow_duplicates=False):
    
    #---------------- die product funktion generiert eine Menge mit allen Tupeln, die sich aus code_range und code_lenght, diese ist aber nicht subscriptable, daher die Umwandlung in eine Liste
    possible_codes = [i for i in product(code_range, repeat=code_lenght)]
    
    #------ Es wird ein nested dictionary erstellt, das auf der ersten Ebene einen Key mit dem Namen "Code {i+1}" für jedes in possible_codes enthaltenes Tupel. Diesem Key wird ein leeres dictionary zugeordnet. Auf der zweiten Ebene wird für jedes Element in einem dieser Tupel ein Key mit dem Namen "Space {j+1}" erzeugt und ihm der Wert des entsprechenden Elementes zugewiesen.
    #------ multi_color_key speichert keys zu Codes, in denen Farben mehfach verwendet
    #------ used_colors speichert Farben, die in einem Code bereits verwendet wurden
    possible_codes_dict = {}
    multi_color_key = set()
    for i in range(len(possible_codes)):
        possible_codes_dict[f"Code {i+1}"]={}
        used_colors = set()
        for j in range(code_lenght):
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
            
    return possible_codes_dict
    
possible_codes = possible_codes_dict(code_range,code_lenght,True)

## ----- Zu Testzwecken eingefügt.
print(len(possible_codes))

code_cpu = {"Space 1":"red","Space 2":"green","Space 3":"purple","Space 4":"black"}

code_user = {"Space 1":"red","Space 2":"blue","Space 3":"green","Space 4":"yellow"}

# Checking colors
def color_check(code_user, code_cpu):
    global round
    color_match_cpu = {}
    correct_position = 0 
    incorrect_position = 0   

    # Count the frequency of each color in the CPU's code
    for color in code_cpu.values():
        color_match_cpu[color] = color_match_cpu.get(color, 0) + 1
    
    # First, count correctly positioned colors
    for space in code_user:
        user_color = code_user[space]
        cpu_color = code_cpu[space]
        if user_color == cpu_color:
            correct_position += 1
            color_match_cpu[cpu_color] -= 1
    
    # Then, count incorrectly positioned colors
    for space in code_user:
        user_color = code_user[space]
        cpu_color = code_cpu[space]
        # Only count as incorrect if the color is in the CPU's code and not already matched
        if user_color != cpu_color and color_match_cpu.get(user_color, 0) > 0:
            incorrect_position += 1
            color_match_cpu[user_color] -= 1
    
    round += 1
    return correct_position, incorrect_position
    
###--- Funktion aktualisiert das possible_codes_dict
#----- Für jeden Code in possible_codes_dict wird überprüft, ob die Bewertung ausgegeben wird, wenn man den Code mit der Usereingabe vergleicht
#----- Wenn ein "possible Code" zu einer anderen Bewertung führt, wird er in wrong_codes gespeichert
#----- Im Nachgang werden die Codes aus wrong_codes aus dem possible_code_dict gelöscht

def act_possible_codes(possible_codes,code_user,code_cpu):
    wrong_codes = set()   
    for code in possible_codes:
        if color_check(code_user, code_cpu) != color_check(code_user, possible_codes[code]):
            wrong_codes.add(code)
    for key in wrong_codes:
        del possible_codes[key]
        
    return possible_codes

possible_codes = act_possible_codes(possible_codes,code_user,code_cpu)
print(len(possible_codes))
    
    