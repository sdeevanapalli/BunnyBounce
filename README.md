# Terminal Game

This is a simple terminal-based game implemented in Python using the `curses` library.

## How to Run

To run the game, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/sdeevanapalli/TerminalGame.git
    ```

2. Navigate to the game directory:

    ```bash
    cd TerminalGame
    ```

3. Execute the shell script `run_game.sh`:

    ```bash
    python3 game.py
    ```

This script will automatically change the directory to the game's location and run the Python script. Ensure that you have Python installed on your system before running the game.


## Overview

The game involves navigating a rabbit through a grid-based map containing carrots and holes. The goal of the game is to collect all the carrots.

## How to Play

1. **Setup**: Upon launching the game, you will be prompted to enter the width and height of the game grid, as well as the number of carrots and holes to be placed randomly on the map.

2. **Controls**: You can control the rabbit using the following keys:
   - `w`: Move up
   - `a`: Move left
   - `s`: Move down
   - `d`: Move right
   - `wa`, `aw`: Move diagonally up-left
   - `wd`, `dw`: Move diagonally up-right
   - `sa`, `as`: Move diagonally down-left
   - `sd`, `ds`: Move diagonally down-right
   - `j`: Jump over a hole (if possible)
   - `p`: Pick up or deposit a carrot
   - `q`: Quit the game

3. **Objective**: Navigate the rabbit to collect all the carrots while avoiding falling into holes.

4. **Game Status**: The game will display the current grid state, including the position of the rabbit, carrots, and holes.

5. **Winning**: You win the game when all the carrots are collected. 


## Game Mechanics

- **Rabbit**: Represented by the letter `r` on the grid. Can move in four cardinal directions and diagonally.
- **Carrot**: Represented by the letter `c` on the grid. Can be picked up by the rabbit.
- **Hole**: Represented by the letter `O` on the grid. If the rabbit falls into a hole while carrying a carrot, the carrot is deposited into the hole, removing it from the grid.
- **Movement**: Use the arrow keys to move the rabbit. Press `j` to jump over a hole (if there is a clear pathway on the other side).

## Enjoy the Game!

Have fun playing the Terminal Game and see if you can collect all the carrots without falling into any holes!

