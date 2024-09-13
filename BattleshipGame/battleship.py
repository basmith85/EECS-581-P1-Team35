"""
Battleship Game
This program implements a two-player Battleship game with manual and random ship placement. Players take turns firing
shots at each other's board, and the first player to sink all the opponent's ships wins.
Inputs: Player inputs for placing ships and firing shots
Output: Hits, misses, ship status (sunk or not)
Author: Darshil Patel, (add your names)
Created on: 09/13/24
"""

import random


# Ship class represents a ship's properties: name, size, coordinates, and hits it has taken.
class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []  # List of tuples for the ship's coordinates
        self.hits = 0  # Track the number of hits on the ship

    def is_sunk(self):
        """Returns True if the ship is fully sunk (i.e., hits equal its size)."""
        return self.hits == self.size


# Board class represents the game board for both the player and opponent.
class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]  # '~' represents water
        self.ships = []  # List of ships placed on the board
        self.shots = set()  # Keep track of fired shots

    def display(self, show_ships=False):
        """Display the board, optionally showing the ships."""
        print("  " + " ".join([chr(65 + i) for i in range(self.size)]))  # Print columns A-J
        for i in range(self.size):
            row = [self.grid[i][j] if show_ships or self.grid[i][j] not in 'S' else '~' for j in range(self.size)]
            print(f"{i + 1:2} " + " ".join(row))

    def place_ship(self, ship, start_row, start_col, horizontal=True):
        """Place a ship on the board at the specified row and column."""
        if horizontal:
            if start_col + ship.size > self.size:
                return False  # Ship would go out of bounds horizontally
            for i in range(ship.size):
                if self.grid[start_row][start_col + i] != '~':
                    return False  # Space is already taken
            for i in range(ship.size):
                self.grid[start_row][start_col + i] = 'S'
                ship.coordinates.append((start_row, start_col + i))
        else:
            if start_row + ship.size > self.size:
                return False  # Ship would go out of bounds vertically
            for i in range(ship.size):
                if self.grid[start_row + i][start_col] != '~':
                    return False  # Space is already taken
            for i in range(ship.size):
                self.grid[start_row + i][start_col] = 'S'
                ship.coordinates.append((start_row + i, start_col))

        self.ships.append(ship)
        return True

    def fire(self, row, col):
        """Fire a shot at the opponent's board and determine hit or miss."""
        if (row, col) in self.shots:
            print("Already fired at this location!")
            return False
        self.shots.add((row, col))
        if self.grid[row][col] == 'S':
            print("Hit!")
            self.grid[row][col] = 'X'  # Mark hit on the board
            for ship in self.ships:
                if (row, col) in ship.coordinates:
                    ship.hits += 1
                    if ship.is_sunk():
                        print(f"{ship.name} is sunk!")
            return True
        else:
            print("Miss!")
            self.grid[row][col] = 'O'  # Mark miss on the board
            return False


# Initialize the game by setting up boards and placing ships for both players.
def initialize_game():
    player_game_board = Board()
    opponent_game_board = Board()

    # Define ships for both players
    ships = [
        Ship("Destroyer", 2),
        Ship("Submarine", 3),
        Ship("Cruiser", 3),
        Ship("Battleship", 4),
        Ship("Carrier", 5)
    ]

    # Player places ships manually, while the opponent places ships randomly.
    for ship in ships:
        place_ship_manually(player_game_board, ship)
        place_ship_randomly(opponent_game_board, ship)

    return player_game_board, opponent_game_board


# Place ships randomly for the opponent.
def place_ship_randomly(board, ship):
    placed = False
    while not placed:
        row, col = random.randint(0, board.size - 1), random.randint(0, board.size - 1)
        horizontal = random.choice([True, False])
        placed = board.place_ship(ship, row, col, horizontal)


# Allow the player to manually place their ships on the board.
def place_ship_manually(board, ship):
    board.display(show_ships=True)
    print(f"\nPlace your {ship.name} (size {ship.size})")

    while True:
        pos = input("Enter starting position (e.g., A5): ").upper()
        if len(pos) < 2:
            print("Invalid input! Please try again.")
            continue

        col = ord(pos[0]) - 65  # Convert 'A' to 0, 'B' to 1, etc.
        row = int(pos[1:]) - 1  # Convert '5' to 4, etc.

        if row < 0 or row >= board.size or col < 0 or col >= board.size:
            print("Position out of bounds! Please try again.")
            continue

        orientation = input("Horizontal or Vertical (H/V): ").upper()
        if orientation not in ('H', 'V'):
            print("Invalid orientation! Please enter 'H' or 'V'.")
            continue

        horizontal = orientation == 'H'
        if board.place_ship(ship, row, col, horizontal):
            print(f"{ship.name} placed successfully!")
            break
        else:
            print("Invalid position or out of bounds! Try again.")


# Main game loop that alternates turns between the player and the opponent.
def game_loop(player_board, opponent_board):
    turn = 1
    while True:
        print("\nYour board:")
        player_board.display(show_ships=True)
        print("\nOpponent's board:")
        opponent_board.display()

        # Player's turn
        if turn % 2 != 0:
            print("\nPlayer's turn!")
            if player_turn(player_board, opponent_board):
                if all(ship.is_sunk() for ship in opponent_board.ships):
                    print("Congratulations! You win!")
                    break
        # Opponent's turn
        else:
            print("\nOpponent's turn!")
            if opponent_turn(opponent_board, player_board):
                if all(ship.is_sunk() for ship in player_board.ships):
                    print("Opponent wins! Better luck next time.")
                    break

        turn += 1


# Player's turn to fire a shot.
def player_turn(player_game_board, opponent_game_board):
    while True:
        shot = input("Enter coordinates to fire (e.g., A5): ").upper()
        if len(shot) < 2:
            print("Invalid input! Please try again.")
            continue

        col = ord(shot[0]) - 65  # Convert 'A' to 0, 'B' to 1, etc.
        row = int(shot[1:]) - 1  # Convert '5' to 4, etc.

        if row < 0 or row >= opponent_game_board.size or col < 0 or col >= opponent_game_board.size:
            print("Position out of bounds! Please try again.")
            continue

        return opponent_game_board.fire(row, col)


# Opponent's turn to fire randomly at the player's board.
def opponent_turn(opponent_game_board, player_game_board):
    row, col = random.randint(0, player_game_board.size - 1), random.randint(0, player_game_board.size - 1)
    print(f"Opponent fires at {chr(col + 65)}{row + 1}!")
    return player_game_board.fire(row, col)


# Main function to start the game.
if __name__ == "__main__":
    player_board, opponent_board = initialize_game()
    game_loop(player_board, opponent_board)
