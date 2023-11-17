import random
import copy

def check_possibles(act_code,mastercode):
    global possible_codes
    #bewertung_act = bewertung
    possible_codes = [possible_codes[i] for i in range(len(possible_codes)) if check(possible_codes[i],act_code) == check(mastercode,act_code)]
    #for i in range(len(possible_codes)):
        #bewertung_try = check(possible_codes[i],act_code)
        #if bewertung_try != bewertung_act:
            ##possible_codes.remove(possible_codes[i])
            #possible_codes[i] = ""

def check(mastercode,act_code):
    m = copy.deepcopy(mastercode)
    s = copy.deepcopy(act_code)
    bewertung = []
    for i in range(4):
        if s[i] == m[i]:
            bewertung.append("r")
            m[i] = "+"
            s[i] = "-"
    for i in range(4):
        for j in range(4):
            if s[i] == m[j]:
                #print(f"{i}:{j}")
                m[j] = "++"
                s[i] = "--"
                bewertung.append("w")
                #print(f"{s}\n{m}")
    return bewertung
            
options = ["1","2","3","4","5","6"]
possible_codes = []
for a in options:
    for b in options:
        for c in options:
            for d in options:
                possible_codes.append([f"{a}",f"{b}",f"{c}",f"{d}"])
mastercode = random.choice(possible_codes)

#print(possible_codes)
print(len(possible_codes))
print(f"Mastercode: {mastercode}")
gameround = 1
while gameround <= 12:
    print(f"Runde: {gameround}")
    if gameround == 1:
        act_code = ["1","1","2","2"]
    else:
        act_code = random.choice(possible_codes)

    if act_code == mastercode:
        print("GEWONNEN")
        break

    
    bewertung = check(mastercode,act_code)
    print(bewertung)

    check_possibles(act_code,mastercode)
    print(len(possible_codes))

    gameround +=1
#print(possible_codes)


