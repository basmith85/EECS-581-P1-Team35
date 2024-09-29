"""
Battleship Game
This program implements a two-player Battleship game with manual ship placement. Players take turns firing
shots at each other's board, and the first player to sink all the opponent's ships wins.
Inputs: Player inputs for placing ships and firing shots
Output: Hits, misses, ship status (sunk or not)
Author: Darshil Patel, Blake Smith, Ike Phillips, Brady Holland, Kansas Lees
Created on: 09/13/24
"""
from time import sleep
from random import randint, choice
directions = ['N', 'S', 'E', 'W']
import sys

DBG = False

# Ship class represents a ship's properties: name, size, coordinates, and hits it has taken.
class Ship:
    # creates the init function for the ship class defining name, size, coordinates, and hits.
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []  # List of tuples for the ship's coordinates
        self.hits = 0  # Track the number of hits on the ship

    # function to determine if a ship has been sunk or not.
    def is_sunk(self):
        """Returns True if the ship is fully sunk (i.e., hits equal its size)."""
        return self.hits == self.size


# Board class represents the game board for both the player and opponent.
class Board:
    # creates the init function for the board class defining size, grid, ships, and shots.
    def __init__(self, size=10):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]  # '~' represents water
        self.ships = []  # List of ships placed on the board
        self.shots = set()  # Keep track of fired shots

    def display(self, show_ships=False):
        """Display the board, optionally showing the ships."""
        print("   " + " ".join([chr(65 + i) for i in range(self.size)]))  # Print columns A-J
        for i in range(self.size):
            row = [self.grid[i][j] if show_ships or self.grid[i][j] not in 'S' else '~' for j in
                   range(self.size)]  # prints the rows as either ships or water
            print(f"{i + 1:2} " + " ".join(row))

    # places ships on the board at the given row and column, boolean value to determine if the ship is placed horizontally or not.
    def place_ship(self, ship, start_row, start_col, horizontal=True):
        """Place a ship on the board at the specified row and column."""
        if horizontal:  # horizontal ship
            if start_col + ship.size > self.size:
                return False  # Ship would go out of bounds horizontally
            for i in range(ship.size):
                if self.grid[start_row][start_col + i] != '~':
                    return False  # Space is already taken
            for i in range(ship.size):
                self.grid[start_row][start_col + i] = 'S'
                ship.coordinates.append((start_row, start_col + i))  # adds the ships coordinates to the board's list
        else:  # vertical ship
            if start_row + ship.size > self.size:
                return False  # Ship would go out of bounds vertically
            for i in range(ship.size):
                if self.grid[start_row + i][start_col] != '~':
                    return False  # Space is already taken
            for i in range(ship.size):
                self.grid[start_row + i][start_col] = 'S'
                ship.coordinates.append((start_row + i, start_col))  # adds the ships coordinates to the board's list

        self.ships.append(ship)  # adds the ship to the list of ships on the board
        return True

    def fire(self, row, col):
        """Fire a shot at the opponent's board and determine hit or miss."""
        # determines if a spot on the board has been fired on already by a player.
        if (row, col) in self.shots:
            print("Already fired at this location!")
            return 2
        # "fires" the shot on the board, determining if it is a hit or not and adding the shot to the boards list of shots.
        self.shots.add((row, col))
        if self.grid[row][col] == 'S':
            print("Hit!")
            self.grid[row][col] = 'X'  # Mark hit on the board
            for ship in self.ships:
                if (row, col) in ship.coordinates:
                    ship.hits += 1
                    if ship.is_sunk():
                        print(f"{ship.name} is sunk!")
                        return 3
            return 1
        else:
            print("Miss!")
            self.grid[row][col] = 'O'  # Mark miss on the board
            return False

class AI:
    def __init__(self, board, difficulty):
        self.board = board
        self.difficulty = difficulty
        self.last_hit = None
        self.possible_targets = []

    def place_ships(self, ships):
        print("\nAI is placing ships...")
        for ship in ships:
            placed = False
            while not placed:
                row = randint(0, self.board.size - 1)
                col = randint(0, self.board.size - 1)
                direction = choice(directions)
                placed = self.board.place_ship(ship, row, col, horizontal=(direction in ['E', 'W']))

    def fire(self, opponent_board):

        def get_random_shot():
            while True:
                row = randint(0, opponent_board.size - 1)
                col = randint(0, opponent_board.size - 1)
                if (row, col) not in opponent_board.shots:
                    return row, col

        def get_adjacent_shots(row, col):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            return [(row + dr, col + dc) for dr, dc in directions if
                    0 <= row + dr < opponent_board.size and 0 <= col + dc < opponent_board.size]

        match self.difficulty.lower():
            case 'easy':
                row, col = get_random_shot()
                return opponent_board.fire(row, col)
            case 'medium':
                if self.last_hit and not self.possible_targets:
                    self.possible_targets = get_adjacent_shots(*self.last_hit)
                if self.possible_targets:
                    row, col = self.possible_targets.pop(0)
                    while (row, col) in opponent_board.shots:
                        if not self.possible_targets:
                            row, col = get_random_shot()
                            break
                        row, col = self.possible_targets.pop(0)
                else:
                    row, col = get_random_shot()

                result = opponent_board.fire(row, col)
                if result == 1:
                    self.last_hit = (row, col)
                elif result == 3:
                    self.last_hit = None
                    self.possible_targets = []
                return result
            case 'hard':
                for ship in opponent_board.ships:
                    for row, col in ship.coordinates:
                        if (row, col) not in opponent_board.shots:
                            return opponent_board.fire(row, col)


# Initialize the game by setting up boards and placing ships for both players.
def initialize_game():
    player_board = Board()
    ai_board = Board()

    while True:
        try:
            difficulty = input("Enter AI difficulty ('Easy', 'Medium', 'Hard'): ").lower()
            if difficulty not in ('easy', 'medium', 'hard'):
                print("Invalid difficulty! Please enter 'Easy', 'Medium', or 'Hard'.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter 'Easy', 'Medium', or 'Hard'.")

    while True:
        try:
            num_ships = int(input("Enter the number of ships (1 to 5): "))
            if num_ships < 1 or num_ships > 5:
                print("Please enter a number between 1 and 5.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 5.")

    player_ships = [Ship(f"Ship {i}", i) for i in range(1, num_ships + 1)]

    print("\nPlayer, place your ships:")
    for ship in player_ships:
        place_ship_manually(player_board, ship)

    #clear_screen()

    ai_ships = [Ship(f"Ship {i}", i) for i in range(1, num_ships + 1)]

    ai = AI(ai_board, difficulty)
    ai.place_ships(ai_ships)
    if DBG:
        ai.board.display(show_ships=True)
    return player_board, ai_board, ai


# allows for ships to be manually placed on to the board by the players.
def place_ship_manually(board, ship):
    board.display(show_ships=True)
    print(f"\nPlace your {ship.name} (size {ship.size})")

    # allows for players to select the spot on the board for their ship to be placed, making sure that their position is a valid input.
    while True:
        pos = input("Enter starting position (e.g., A5): ").upper()
        if len(pos) < 2 or not pos[0].isalpha() or not pos[1:].isdigit():
            print("Invalid input format! Please enter a valid position like 'A5'.")
            continue

        col = ord(pos[0]) - 65  # Convert 'A' to 0, 'B' to 1, etc.
        row = int(pos[1:]) - 1  # Convert '5' to 4, etc.

        # checks to make sure that the given position is within bounds of the board size
        if row < 0 or row >= board.size or col < 0 or col >= board.size:
            print("Position out of bounds! Please try again.")
            continue

        # allows the user to pick the direction that their ship is facing, this step is skipped if their ship is a 1x1
        if ship.size == 1:
            if board.place_ship(ship, row, col, horizontal=True):
                print(f"{ship.name} placed successfully!")
                break
        else:
            # prompts the user to pick the cardinal direction of their ship.
            direction = input("Enter direction (North, South, East, West - N/S/E/W): ").upper()
            if direction not in ('N', 'S', 'E', 'W'):
                print("Invalid direction! Please enter 'N', 'S', 'E', or 'W'.")
                continue

            overlap = False  # Variable to track if there’s an overlap

            # code to place an East facing ship, making sure that the ship is not out of bounds or overlaps any other ship when facing this direction.
            # if the ship overlaps with another or is out of bounds the player is prompted to pick another direction.
            if direction == 'E':
                if col + ship.size > board.size:  # Out of bounds check for East
                    print("Ship goes out of bounds to the East! Please try again.")
                    continue
                # Check for overlap
                for i in range(ship.size):
                    if board.grid[row][col + i] != '~':
                        overlap = True
                        break
                if overlap:
                    print("Ship overlaps with another ship! Please try again.")
                    continue
                horizontal = True
                if board.place_ship(ship, row, col, horizontal):
                    print(f"{ship.name} placed successfully!")
                    break

            # implementation for if the player chooses for a ship to face West.
            elif direction == 'W':
                if col - (ship.size - 1) < 0:  # Out of bounds check for West
                    print("Ship goes out of bounds to the West! Please try again.")
                    continue
                # Check for overlap
                for i in range(ship.size):
                    if board.grid[row][col - i] != '~':
                        overlap = True
                        break
                if overlap:
                    print("Ship overlaps with another ship! Please try again.")
                    continue
                horizontal = True
                if board.place_ship(ship, row, col - (ship.size - 1), horizontal):
                    print(f"{ship.name} placed successfully!")
                    break

            # implementation for if a player chooses for a ship to face South
            elif direction == 'S':
                if row + ship.size > board.size:  # Out of bounds check for South
                    print("Ship goes out of bounds to the South! Please try again.")
                    continue
                # Check for overlap
                for i in range(ship.size):
                    if board.grid[row + i][col] != '~':
                        overlap = True
                        break
                if overlap:
                    print("Ship overlaps with another ship! Please try again.")
                    continue
                horizontal = False
                if board.place_ship(ship, row, col, horizontal):
                    print(f"{ship.name} placed successfully!")
                    break

            # implementation for if a player chooses for a ship to face North
            elif direction == 'N':
                if row - (ship.size - 1) < 0:  # Out of bounds check for North
                    print("Ship goes out of bounds to the North! Please try again.")
                    continue
                # Check for overlap
                for i in range(ship.size):
                    if board.grid[row - i][col] != '~':
                        overlap = True
                        break
                if overlap:
                    print("Ship overlaps with another ship! Please try again.")
                    continue
                horizontal = False
                if board.place_ship(ship, row - (ship.size - 1), col, horizontal):
                    print(f"{ship.name} placed successfully!")
                    break


# Main game loop that alternates turns between Player 1 and Player 2.
def game_loop(player_board, ai_board, ai):
    turn = 1
    recent_move_message = ""
    bomb_used = False  # Track if the bomb has been used

    while True:
        print(f"\n--- Turn {turn} ---")

        if turn % 2 != 0:
            if recent_move_message:
                print(recent_move_message)

            print("\nPlayer's turn:")
            print("Your board:")
            player_board.display(show_ships=True)
            print("\nOpponent's board (AI):")
            ai_board.display()

            recent_move_message = player_turn(ai_board, "Player", bomb_used)
            bomb_used = recent_move_message.get("bomb_used", bomb_used)  # Update bomb_used from player's turn message

            if all(ship.is_sunk() for ship in ai_board.ships):
                print("Player wins! Congratulations!")
                break
        else:
            print("\nAI's turn:")
            sleep(2)
            result = ai.fire(player_board)
            recent_move_message = "AI fired and " + ("hit!" if result == 1 or result == 3 else "missed.")
            print(recent_move_message)

            if all(ship.is_sunk() for ship in player_board.ships):
                print("AI wins! Better luck next time!")
                break

        sleep(2)
        turn += 1

# Function to handle bomb firing affecting the entire row and column
def fire_bomb(opponent_board, row, col):
    hits = []
    
    # Fire bomb in the entire row
    for c in range(opponent_board.size):  # Iterate over the entire row
        result = opponent_board.fire(row, c)
        if result in (1, 3):  # Hit
            hits.append((row, c))
    
    # Fire bomb in the entire column
    for r in range(opponent_board.size):  # Iterate over the entire column
        result = opponent_board.fire(r, col)
        if result in (1, 3):  # Hit
            hits.append((r, col))

    return hits

# Player's turn to fire a shot.
def player_turn(opponent_board, player_name, bomb_used):
    while True:
        print(f"\n{player_name}, it's your turn to fire.")

        # Prompt for action based on whether the bomb has been used
        if not bomb_used:
            choice = input("Choose to fire a shot or use a bomb (shot/bomb): ").lower()
        else:
            choice = "shot"  # Automatically set to shot if bomb is used

        if choice == "bomb":

            # Prompt for bomb coordinates
            shot = input("Enter coordinates to fire bomb (e.g., A5): ").upper()

            # Validate input
            if len(shot) < 2 or not shot[0].isalpha() or not shot[1:].isdigit():
                print("Invalid input! Please enter a valid position like 'A5'.")
                continue

            col = ord(shot[0]) - 65
            row = int(shot[1:]) - 1

            if row < 0 or row >= opponent_board.size or col < 0 or col >= opponent_board.size:
                print("Position out of bounds! Please try again.")
                continue

            # Fire the bomb
            hit_positions = fire_bomb(opponent_board, row, col)
            bomb_used = True  # Mark the bomb as used

            if hit_positions:
                hit_details = ", ".join([f"{chr(col + 65)}{row + 1}" for row, col in hit_positions])
                print(f"{player_name} used a bomb and hit: {hit_details}!")
            else:
                print(f"{player_name} used a bomb but missed all targets.")
            return {"bomb_used": bomb_used}  # End turn after bomb use

        elif choice == "shot":
            shot = input("Enter coordinates to fire (e.g., A5): ").upper()

            if len(shot) < 2 or not shot[0].isalpha() or not shot[1:].isdigit():
                print("Invalid input! Please enter a valid position like 'A5'.")
                continue

            col = ord(shot[0]) - 65
            row = int(shot[1:]) - 1

            if row < 0 or row >= opponent_board.size or col < 0 or col >= opponent_board.size:
                print("Position out of bounds! Please try again.")
                continue

            result = opponent_board.fire(row, col)

            if result == 1 or result == 3:
                print(f"{player_name} chose {shot} and hit!")
            elif result == 2:
                print("You've already fired at this location!")
                continue
            else:
                print(f"{player_name} chose {shot} and missed.")
            return {"bomb_used": bomb_used}  # End turn after regular shot

        else:
            print("Invalid choice! Please choose 'shot' or 'bomb'.")

# clears the screen to keep players from seeing each other's screens.
#def clear_screen():
    #system('cls' if name == 'nt' else 'clear')


# Main function to start the game, creates the boards and begins the game loop.
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        DBG = int(sys.argv[1]) == 1
    player_board, ai_board, ai = initialize_game()
    game_loop(player_board, ai_board, ai)