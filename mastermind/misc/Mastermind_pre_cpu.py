import random
#import pandas as pd
import copy
import os
import time

#class Code:
#    def __init__(self,p1="",p2="",p3="",p4=""):
#        self.p1=p1
#        self.p2=p2
#        self.p3=p3
#        self.p4=p4
#
#    def __str__(self):0
#        return "p1={},p2={},p3={},p4={}".format(self.p1,self.p2,self.p3,self.p4)

def check(i,j):
    master = copy.deepcopy(i)
    code = copy.deepcopy(j)
    bewertung = []
    for n in range(4):
        if code[n]==master[n]:
            bewertung.append("r")
            code[n] = "-"
            master[n] = "+"
    for o in range(4):
        for p in range(4):
            if code[o]==master[p]:
                bewertung.append("w")
                code[o] = "--"
                master[p] = "++"
    return bewertung

def guess_npc(colours):
    code = []
    for i in range(4):
        code.append(random.choice(colours))
    return code
    
def master_npc(colours):
    mastercode = []
    for i in range(4):
        mastercode.append(random.choice(colours))
    return mastercode

def master(c):
    mastercode = []
    print(f"Die Verfügbaren Farben sind: ")
    for i in range(6):
        print(f"{i} : {c[i]}")
    for i in range(4):
        while True:
            x = input(f"Bitte geben sie jetzt die Ziffer für die gewünschte Farbe des Steckplatzes {i+1} ein")
            if x in ["0","1","2","3","4","5"]:
                mastercode.append(c[int(x)])
                break
            else: print("Ihr Eintrag verweist auf keine gültige Zahl.")
    return mastercode
        
def p_is_h():
    x = input("Wenn der Code vom Computer gelöst werden soll, geben Sie [0] ein: ")
    if x == "0":
        return False
    else:
        return True
    
def m_is_h():
    x = input("Wenn der Code vom Computer generiert werden soll, geben Sie [0] ein: ")
    if x == "0":
        return False
    else:
        return True



colours = ["Blau","Grün","Gelb","Rot","Orange","Lila"]

if m_is_h():
    mastercode = master(colours)

else:
    mastercode = master_npc(colours)

game_mode = p_is_h()
game_round = 1


print(mastercode)
while game_round <=12:
    print(f"Runde {game_round}")
    if game_mode:
        guess = master(colours)
    else:
        guess = guess_npc(colours)

    print(guess)

    if guess == mastercode:
        print("gewonnen")
        break

    bewertung = check(mastercode,guess)
    print(bewertung)

    game_round +=1

    input("Bereit für die nächste Runde?")

print("Schleife funktioniert")


#-----------------------------------------Code für eine Highscore-Liste
### ----- ist aus einem anderen Projekt von mir raus kopiert, lässt sich aber hier denke ich auch gut einsetzen
r"""
import os
import pandas as pd

op_dir = os.getcwd()

if "scores.csv" in os.listdir(path=op_dir):
    scores = pd.read_csv("scores.csv",sep=";")

else:
    scores = {
        "Name":["","","","","","","","","",""],
        "Aufgaben":["","","","","","","","","",""],
        "Quote[%]":["","","","","","","","","",""],
        "Zeit[s]":["","","","","","","","","",""],
        "Score":[0,0,0,0,0,0,0,0,0,0],
        "Datum":["","","","","","","","","",""]
        }
    
    scores = pd.DataFrame(scores)
scores = scores.set_axis(["Platz 1","Platz 2","Platz 3","Platz 4","Platz 5","Platz 6","Platz 7","Platz 8","Platz 9","Platz 10"], axis=0)






for i in range(10):
        if score > scores.iat[i,4]:
            for y in range (9,i,-1):
                scores.iloc[y] = scores.iloc[y-1]
            scores.iloc[i]=[name,aufgabe,p,tot_sec,score,date]
            break
    

            
scores.to_csv("scores.csv", sep=";", index=False)

"""