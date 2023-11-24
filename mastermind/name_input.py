def get_player_name():

    # Asks the player for their name and returns it.
    # This function can be reused for multiple game modes and different UIs.

    while True:
        name = input("Please enter your name: ").strip()
        if name:
            return name
        else:
            print("Name cannot be empty. Please enter a valid name.")