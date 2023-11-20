import random

# Codecolors range
code_range = ["Red", "Yellow", "Green", "Blue", "Orange", "Purple", "Brown", "White"]

# Code building dictionary for holding the same structure as player and CPU
code_dict = {"Space 1": None, "Space 2": None, "Space 3": None, "Space 4": None}

#creating a dict to link menue numbers to color values
color_menue = {
    1: "Red",
    2: "Yellow",
    3: "Green",
    4: "Blue",
    5: "Orange",
    6: "Purple",
    7: "Brown",
    8: "White"
}

# Generate random Code CPU
code_cpu = code_dict.copy()

def cpu_pick():
  for keys in code_cpu:
    if code_cpu[keys] is None:
        code_cpu[keys] = random.choice(code_range)
        continue
    return code_cpu

cpu_pick()

# For checking reasons only 
print(f"The CPU's code is {code_cpu['Space 1']}, {code_cpu['Space 2']}, {code_cpu['Space 3']}, {code_cpu['Space 4']}")

# User choice code
code_user = code_dict.copy()

def menue_swap():
    for space, color_keys in code_user.items():
        if color_keys in color_menue:
            code_user[space] = color_menue[color_keys]
    return code_user

def user_pick():
    print("""
      Please select colors from list
      [1] Red       [5] Orange
      [2] Yellow    [6] Purple
      [3] Green     [7] Brown
      [4] Blue      [8] White
      """)
    for keys in code_user:
        if code_user[keys] is None:
            code_user[keys] = int(input(f"Please select a color for {keys}: "))
        menue_swap()
    return code_user

user_pick()

# Rounds counter def value
c_rounds = 0

# Checking colors
def color_check():
    spaces_counter = 0      # checking matching keys
    color_counter = 0       # checking matching values

    for space_cc, color_cc in code_cpu.items():
        if space_cc in code_user:
            spaces_counter += 1

        if code_user[space_cc] == color_cc:
            color_counter += 1
    return spaces_counter, color_counter

print(color_check())