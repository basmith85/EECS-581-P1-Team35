"""
Battleship Game
This program implements a two-player Battleship game with manual ship placement. Players take turns firing
shots at each other's board, and the first player to sink all the opponent's ships wins.
Inputs: Player inputs for placing ships and firing shots
Output: Hits, misses, ship status (sunk or not)
Author: Darshil Patel, Blake Smith, Ike Phillips, Brady Holland, Kansas Lees
Created on: 09/13/24
"""
from os import system, name
from time import sleep
import random

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
            row = [self.grid[i][j] if show_ships or self.grid[i][j] not in 'S' else '~' for j in range(self.size)] # prints the rows as either ships or water
            print(f"{i + 1:2} " + " ".join(row))

    # places ships on the board at the given row and column, boolean value to determine if the ship is placed horizontally or not.
    def place_ship(self, ship, start_row, start_col, horizontal=True):
        """Place a ship on the board at the specified row and column."""
        if horizontal: #horizontal ship
            if start_col + ship.size > self.size:
                return False  # Ship would go out of bounds horizontally
            for i in range(ship.size):
                if self.grid[start_row][start_col + i] != '~':
                    return False  # Space is already taken
            for i in range(ship.size):
                self.grid[start_row][start_col + i] = 'S'
                ship.coordinates.append((start_row, start_col + i)) # adds the ships coordinates to the board's list
        else: # vertical ship
            if start_row + ship.size > self.size:
                return False  # Ship would go out of bounds vertically
            for i in range(ship.size):
                if self.grid[start_row + i][start_col] != '~':
                    return False  # Space is already taken
            for i in range(ship.size):
                self.grid[start_row + i][start_col] = 'S'
                ship.coordinates.append((start_row + i, start_col)) # adds the ships coordinates to the board's list

        self.ships.append(ship) # adds the ship to the list of ships on the board
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
            return 1
        else:
            print("Miss!")
            self.grid[row][col] = 'O'  # Mark miss on the board
            return False


# AI class for the opponent.
class AI:
    def __init__(self, board, difficulty):
        self.board = board
        self.difficulty = difficulty
        self.last_shot = None
        self.previous_shots = []

    def make_move(self):
        """AI makes a move based on difficulty."""
        if self.difficulty == 'easy':
            return self._easy_move()
        elif self.difficulty == 'medium':
            return self._medium_move()
        elif self.difficulty == 'hard':
            return self._hard_move()

    def _easy_move(self):
        """Easy AI makes random moves."""
        # INSERT

    def _medium_move(self):
        """Medium AI makes semi-random moves, prioritizing areas with hits."""
        # INSERT

    def _hard_move(self):
        """Hard AI uses a more strategic approach."""
        # INSERT


def initialize_game():
    """Initialize the game: prompt for difficulty, place ships for player and AI."""
    clear_screen()
    print("Welcome to Battleship!")
    print("Choose AI difficulty (easy, medium, hard):")
    
    while True:
        difficulty = input().lower()
        if difficulty in ['easy', 'medium', 'hard']:
            break
        print("Invalid choice! Please enter 'easy', 'medium', or 'hard'.")

    player_board = Board()
    ai_board = Board()
    ai = AI(ai_board, difficulty)

    while True:
        try:
            num_ships = int(input("Enter the number of ships (1 to 5): "))
            if num_ships < 1 or num_ships > 5:
                print("Please enter a number between 1 and 5.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 5.")

    ships = [Ship(f"Ship {i}", i) for i in range(1, num_ships + 1)]

    print("\nPlayer, place your ships:")
    for ship in ships:
        place_ship_manually(player_board, ship)

    print("\nAI is placing ships...")
    for ship in ships:
        while True:
            row = random.randint(0, ai_board.size - 1)
            col = random.randint(0, ai_board.size - 1)
            horizontal = random.choice([True, False])
            if ai_board.place_ship(ship, row, col, horizontal):
                break

    return player_board, ai_board, ai


def place_ship_manually(board, ship):
    """Allow player to place a ship on their board."""
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


def clear_screen():
    """Clear the console screen based on the operating system."""
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def play_game(player_board, ai_board, ai):
    """Start the game and manage turns between player and AI."""
    while True:
        print("\nPlayer's Board:")
        player_board.display(show_ships=True)
        print("\nAI's Board:")
        ai_board.display()

        print("\nYour turn! Enter the coordinates to fire (e.g., A5):")
        while True:
            pos = input().upper()
            if len(pos) < 2 or not pos[0].isalpha() or not pos[1:].isdigit():
                print("Invalid input format! Please enter a valid position like 'A5'.")
                continue

            col = ord(pos[0]) - 65
            row = int(pos[1:]) - 1

            if row < 0 or row >= player_board.size or col < 0 or col >= player_board.size:
                print("Position out of bounds! Please try again.")
                continue

            result = ai_board.fire(row, col)
            if result == 2:
                continue  # Position already shot
            break

        if all(ship.is_sunk() for ship in ai_board.ships):
            print("Congratulations! You've sunk all the AI's ships!")
            return

        print("\nAI's turn...")
        row, col = ai.make_move()
        print(f"AI fires at {chr(65 + col)}{row + 1}")
        result = player_board.fire(row, col)
        
        if all(ship.is_sunk() for ship in player_board.ships):
            print("AI wins! All your ships are sunk.")
            return

        sleep(1)  # Add delay for the AI's turn


def main():
    player_board, ai_board, ai = initialize_game()
    play_game(player_board, ai_board, ai)


if __name__ == "__main__":
    main()
