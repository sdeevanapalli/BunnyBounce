import curses
import random


# Constants
RABBIT_1 = "r"
RABBIT_2 = "R"
CARROT = "c"
HOLE = "O"
PATHWAY = "-"


def generate_map(width, height, num_carrots, num_holes):
    n = max(width, height)
    grid = [['-' for _ in range(n)] for _ in range(n)]
    chosen_positions = set()

    rabbit_positions = []
    carrot_positions = []
    hole_positions = []

    # Place Rabbit 1
    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)
    position = (x, y)
    chosen_positions.add(position)
    grid[x][y] = RABBIT_1
    rabbit_positions.append(position)

    # Place Carrots
    while len(chosen_positions) <= num_carrots:
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        position = (x, y)
        if position not in chosen_positions:
            chosen_positions.add(position)
            grid[x][y] = CARROT
            carrot_positions.append(position)

    # Place Holes
    while len(chosen_positions) <= num_carrots + num_holes:
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        position = (x, y)
        if position not in chosen_positions:
            chosen_positions.add(position)
            grid[x][y] = HOLE
            hole_positions.append(position)

    return grid, rabbit_positions, carrot_positions, hole_positions


def move_rabbit(kb, current_position, grid, carrot_picked_up):  # keybind
    x, y = current_position
    new_x, new_y = x, y

    if 'w' in kb:
        new_x -= 1
    if 'a' in kb:
        new_y -= 1
    if 's' in kb:
        new_x += 1
    if 'd' in kb:
        new_y += 1
    if 'wa' in kb or 'aw' in kb:
        new_x -= 1
        new_y -= 1
    if 'wd' in kb or 'dw' in kb:
        new_x -= 1
        new_y += 1
    if 'sa' in kb or 'as' in kb:
        new_x += 1
        new_y -= 1
    if 'sd' in kb or 'ds' in kb:
        new_x += 1
        new_y += 1

    n = len(grid)
    if 0 <= new_x < n and 0 <= new_y < n:
        if grid[new_x][new_y] == PATHWAY:
            grid[x][y] = PATHWAY
            grid[new_x][new_y] = RABBIT_1 if not carrot_picked_up else RABBIT_2
            return (new_x, new_y), grid
        else:
            print("Invalid move! Try again.")
            return current_position, grid
    else:
        print("Try again, it's out of limits.")
        return current_position, grid


def pick_up_or_deposit_carrot(current_position, grid, rabbit_character, carrot_picked_up):
    x, y = current_position
    n = len(grid)

    adjacent_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1),
                          (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]

    for pos_x, pos_y in adjacent_positions:
        if 0 <= pos_x < n and 0 <= pos_y < n:
            if carrot_picked_up and grid[pos_x][pos_y] == HOLE:
                grid[x][y] = RABBIT_1  # Mark the current position as a hole
                carrot_picked_up = False  # Reset carrot_picked_up flag
                print("Carrot deposited into the hole!")
                return True, grid, 'r', carrot_picked_up  # Change rabbit character to 'r'
            elif not carrot_picked_up and grid[pos_x][pos_y] == CARROT:
                if rabbit_character == RABBIT_2:
                    print("You are already carrying a carrot!")
                    return False, grid, rabbit_character, carrot_picked_up
                grid[pos_x][pos_y] = PATHWAY  # Remove the carrot from the grid
                grid[x][y] = RABBIT_2  # Change rabbit character to 'R'
                carrot_picked_up = True
                print("Carrot picked up!")
                return True, grid, RABBIT_2, carrot_picked_up

    if carrot_picked_up:
        print("No hole nearby to deposit the carrot!")
    else:
        print("No carrot nearby to pick up!")

    return False, grid, rabbit_character, carrot_picked_up


def jump_over_hole(current_position, grid, rabbit_character, carrot_picked_up):
    x, y = current_position
    n = len(grid)
    possible_jumps = []

    # Check for jump from top to bottom
    if x >= 2 and grid[x - 1][y] == HOLE and grid[x - 2][y] == PATHWAY:
        possible_jumps.append((x - 2, y))

    # Check for jump from bottom to top
    if x <= n - 3 and grid[x + 1][y] == HOLE and grid[x + 2][y] == PATHWAY:
        possible_jumps.append((x + 2, y))

    # Check for jump from left to right
    if y >= 2 and grid[x][y - 1] == HOLE and grid[x][y - 2] == PATHWAY:
        possible_jumps.append((x, y - 2))

    # Check for jump from right to left
    if y <= n - 3 and grid[x][y + 1] == HOLE and grid[x][y + 2] == PATHWAY:
        possible_jumps.append((x, y + 2))

    # Perform the jump if a valid jump is found
    if possible_jumps:
        new_x, new_y = possible_jumps[0]  # Just select the first valid jump
        grid[x][y] = PATHWAY
        grid[new_x][new_y] = rabbit_character
        current_position = (new_x, new_y)
        print("Successfully jumped over the hole!")
    else:
        print("No valid jump found!")

    return current_position, grid, rabbit_character, carrot_picked_up


def main(stdscr):
    curses.echo()  # Enable character echoing
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter width: ")
    stdscr.refresh()
    try:
        width = int(stdscr.getstr().decode('utf-8'))
    except ValueError:
        width = 0
    stdscr.addstr(1, 0, "Enter height: ")
    stdscr.refresh()
    try:
        height = int(stdscr.getstr().decode('utf-8'))
    except ValueError:
        height = 0
    stdscr.addstr(2, 0, "Enter number of carrots: ")
    stdscr.refresh()
    try:
        num_carrots = int(stdscr.getstr().decode('utf-8'))
    except ValueError:
        num_carrots = 0
    stdscr.addstr(3, 0, "Enter number of holes: ")
    stdscr.refresh()
    try:
        num_holes = int(stdscr.getstr().decode('utf-8'))
    except ValueError:
        num_holes = 0

    grid, rabbit_positions, carrot_positions, hole_positions = generate_map(width, height, num_carrots, num_holes)
    current_position = rabbit_positions[0]  # Assuming only one rabbit for now
    carrot_picked_up = False
    rabbit_character = RABBIT_1

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Current Grid:")
        for i, row in enumerate(grid):
            stdscr.addstr(i + 1, 0, ' '.join(row))
        stdscr.addstr(height + 2, 0, "Enter direction (w/a/s/d or combinations like wa/as/dw etc.), \n'j' to jump over the hole, \n'p' to pick up/deposit a carrot, or \n'q' to quit:")
        action = stdscr.getkey()
        try:
            if action == 'q':
                stdscr.addstr(height + 4, 0, "Exiting the game.")
                stdscr.refresh()
                break
            elif action in ['w', 'a', 's', 'd', 'wa', 'aw', 'wd', 'dw', 'as', 'sa', 'sd', 'ds']:
                current_position, grid = move_rabbit(action, current_position, grid, carrot_picked_up)
            elif action == 'p':
                success, grid, rabbit_character, carrot_picked_up = pick_up_or_deposit_carrot(current_position, grid, rabbit_character, carrot_picked_up)
            elif action == 'j':
                current_position, grid, rabbit_character, carrot_picked_up = jump_over_hole(current_position, grid, rabbit_character, carrot_picked_up)
            else:
                stdscr.addstr(height + 4, 0, "Invalid input! Please enter a valid action.")
        except Exception as e:
            stdscr.addstr(height + 4, 0, f"An error occurred: {str(e)}")
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
