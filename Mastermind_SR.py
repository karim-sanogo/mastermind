import random

# Codecolors range
code_range = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white"]

# Rounds counter def value
round = 0

# Max tries in game
tries = 9

# Define lenght of code spaces
code_lenght = 4

# Code building dictionary for holding the same structure as player and CPU, flexible for future changes
def code_build():
    code_dict = {}
    for i in range(code_lenght):
        code_dict[f"Space {i+1}"] = None
    return code_dict
# Example for code_lenght 4: code_dict = {"Space 1": None, "Space 2": None, "Space 3": None, "Space 4": None}

# Generate random Code CPU
code_cpu = code_build().copy()

# Creating a dict to link menu indexes to color values
color_menu = {}

for index, color in enumerate(code_range):
    color_menu[index + 1] = color

# Generate code for CPU, allow_duplicates=True allows for duplicate colors in code
def cpu_pick(allow_duplicates=True):
    used_colors = set()
    for keys in code_cpu:
        if code_cpu[keys] is None:
            if allow_duplicates:
                color = random.choice(code_range)
            else:
                # Filter out used colors
                color = random.choice([color for color in code_range if color not in used_colors])
                used_colors.add(color)
            code_cpu[keys] = color
            continue
    return code_cpu

# Generate blank user code
code_user = code_build().copy()

# Option to disable duplicates in CPU code
cpu_pick(allow_duplicates=True)

# Insert picked colors from menu into code_user
def menue_swap():
    for space, color_keys in code_user.items():
        if color_keys in color_menu:
            code_user[space] = color_menu[color_keys]
    return code_user


# Check if user input is valid
def is_valid_input(user_input):
    try:
        return 1 <= int(user_input) <= color_menu.__len__()
    except ValueError:
        return False


def user_pick(code_user):
    # Variable menu for selecting colors
    menu_string = "Please select colors from list:\n"

    for i in range(1, len(color_menu) + 1, 2):
        # Per line two colors with their index
        first_color = f"[{i}] {color_menu[i].title()}"
        second_color = f"[{i + 1}] {color_menu[i + 1].title()}"
        # Add both colors and indexes as a line to menu_string with first item in a 15 character wide column
        menu_string += f"  {first_color:15} {second_color}\n"

    print(menu_string)

    for space in code_user:
        if code_user[space] is None:
            while True:
                user_input = input(f"Please select a color for {space}: ")
                if is_valid_input(user_input):
                    code_user[space] = int(user_input)
                    menue_swap()
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 8.")
    return code_user


# Checking colors
def color_check(code_user, code_cpu):
    global round
    color_match_cpu = {}
    color_match_user = {}
    correct_position = 0 
    incorrect_position = 0   

    # Check if color value is in code_cpu, if so add color to color_match dict
    for color in code_cpu.values():
        color_match_cpu[color] = color_match_cpu.get(color, 0) + 1
    
    # Count correct positioned colors
    for space in code_user:
        # Get color from code_user and code_cpu
        user_color = code_user[space]
        cpu_color = code_cpu[space]
        # Count colors in code_user, if color is not in dict, add it with value 0
        color_match_user[user_color] = color_match_user.get(user_color, 0) + 1
        
        if user_color == cpu_color:
            # If color matches, add 1 to correct_position and subtract 1 from color_match_cpu, because color is already matched
            correct_position += 1
            color_match_cpu[cpu_color] -= 1
    
    # Count incorrect positioned colors
    # For every color in code_user, check if color is in code_cpu, if so, add the lower value of both to incorrect_position
    for user_color, count in color_match_user.items():
        incorrect_position += min(count, color_match_cpu.get(user_color, 0))
    
    round += 1
    return correct_position, incorrect_position


# Main game loop
def mastermind():
    cpu_pick()
    print(">>> Welcome to Mastermind! <<<\n")

    # For checking reasons only 
    print(f"The CPU's code is {', '.join(code_cpu.values()).title()}\n")
    
    for round in range(1, tries + 1):
        global code_user
        pick = user_pick(code_user)
        # Reset code_user every round
        code_user = code_build().copy()
        
        correct_position, incorrect_position = color_check(pick, code_cpu)
        if correct_position == 4:
            print(f"\nYou won in {round} tries!\n")
            break
        print(f"\nCorrect position: {correct_position}")
        print(f"Incorrect position: {incorrect_position}\n")
        print(f"You have {tries - round} tries left.\n")
    else:
        print(f"You lost! The correct colors were: {', '.join(code_cpu.values()).title()}")

# Start game loop and ask for replay
while True:
    mastermind()
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again == "n":
        break
    elif play_again == "y":
        # Set back CPU Code and round counter
        code_cpu = code_build().copy()
        round = 0
        continue