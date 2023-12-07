import random

colors = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white"]
tries = 10

def player_choice():
    pick = input("Pick your colors: ").lower().split(" ")
    if len(pick) != 4:
        print("You have to pick 4 colors.")
        player_choice()

    for color in pick:
        if color not in colors:
            print("You have to pick a color from the list.")
            player_choice()

    return pick


def check_colors(pick, cp_pick):
    color_check = {}
    correct_position = 0
    incorrect_position = 0

    for color in cp_pick:
        if color not in color_check:
            color_check[color] = 0
        color_check[color] += 1

    for pick_color, cp_color in zip(pick, cp_pick):
        if pick_color == cp_color:
            correct_position += 1
            color_check[pick_color] -= 1

    for pick_color, cp_color in zip(pick, cp_pick):
        if pick_color in cp_color and color_check[pick_color] > 0:
            incorrect_position += 1
            color_check[pick_color] -= 1

    return correct_position, incorrect_position

def mastermind():
    computer_pick = random.sample(colors, 4)
    print("")
    print(">>> Welcome to Mastermind! <<<\n")
    print("You can use the following colors:")
    print(', '.join(colors).title())
    print("")
    print("Type in the colors using a space between each color.")
    print("You have 10 tries to guess the correct colors and positions.\n")
    # Just for testing purposes
    print("The computer picked the following colors:")
    print(', '.join(computer_pick).title())
    print("")
    for player_try in range(1, tries + 1):
        pick = player_choice()
        correct_position, incorrect_position = check_colors(pick, computer_pick)
        if correct_position == 4:
            print(f"You won in {player_try} tries!")
            break
        print(f"Correct position: {correct_position}")
        print(f"Incorrect position: {incorrect_position}")
        print(f"You have {tries - player_try} tries left.\n")
    else:
        print(f"You lost! The correct colors were: {', '.join(computer_pick).title()}")


while True:
    mastermind()
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again == "n":
        break