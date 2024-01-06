
# Mastermind Game with Bot Algorithm in Python

## Introduction
This Mastermind game is a Python-based project developed as part of the "Programming concepts" (in german: "Konzepte der Programmierung") module at the FOM Hochschule Hochschulzentrum Hamburg. The project aims to provide a practical application of object oriented programming concepts learned in the course. The game, designed with a terminal-based user interface, offers an engaging way to understand and apply programming logic, algorithms, and user interface design.

## Installation
To get started with this game, clone the repository to your local machine. Ensure you have Python installed on your system. The game is developed using Python's standard library, so no additional installations are required.

```bash
git clone https://github.com/karim-sanogo/mastermind-kpd-projekt.git
cd mastermind-kpd-projekt
```

## Usage
To play the game, navigate to the project directory and run the `__main__.py` file:

```bash
python __main__.py
```

Follow the on-screen instructions to choose a game mode and start playing.

## How to Play

Mastermind is a classic code-breaking game. The objective is to guess the correct sequence of colors within a limited number of tries. 

### Game Modes
- **Singleplayer**: Play against the computer.
- **Two Player**: Challenge a friend. Create a custom code, which the opponent needs to solve.
- **Bot-Toggle**: Activates a supporting bot in singleplayer mode, which asks before each round whether it should play the round.

## Possible Extensions

Possible extensions are already planned in the code. Here are a few ideas:
- **Leaderboard**: There is already a name query before each round.
- **Difficulty adjustment**: There are already interfaces for *variable changes to the code length*, *adding additional colors* and adjusting whether or not *duplicates of colors* may be used in the generated code
- **GUI**: A graphical UI with, for example, the pygame library would be conceivable. The logic of the basic game can still be used here.

## Contributing
Contributions to the project are welcome. If you have a suggestion that would improve the game, please fork the repository and create a pull request. 

## License
Distributed under the MIT License. See `LICENSE` for more information.
