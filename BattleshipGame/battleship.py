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


# Initialize the game by setting up boards and placing ships for both players.
def initialize_game():
    player1_board = Board()
    player2_board = Board()

    # Ask the players how many ships they want to play with making sure that the number of ships is within the given limit and erroring if not.
    while True:
        try:
            num_ships = int(input("Enter the number of ships (1 to 5): "))
            if num_ships < 1 or num_ships > 5:
                print("Please enter a number between 1 and 5.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 5.")

    # Create ships based on the number chosen
    ships = [Ship(f"Ship {i}", i) for i in range(1, num_ships + 1)]

    # Player 1 places ships
    print("\nPlayer 1, place your ships:")
    for ship in ships:
        place_ship_manually(player1_board, ship)

    # Clear the screen or add some delay to avoid Player 2 seeing Player 1's board
    clear_screen()  # This clears the screen

    # Player 2 places ships
    print("\nPlayer 2, place your ships:")
    for ship in ships:
        place_ship_manually(player2_board, ship)
    clear_screen()
    return player1_board, player2_board

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
def game_loop(player1_board, player2_board):
    turn = 1
    recent_move_message = ""  # Variable to store the recent move message

    while True:
        print(f"\n--- Turn {turn} ---")

        # Player 1's turn
        if turn % 2 != 0:
            # Display the result of the last turn if available
            if recent_move_message:
                print(recent_move_message)

            print("\nPlayer 1's turn:")
            print("Your board:")
            player1_board.display(show_ships=True)  # Show Player 1's board with their ships
            print("\nOpponent's board (Player 2):")
            player2_board.display()  # Show Player 2's board without revealing ships

            # Player 1 makes a move
            recent_move_message = player_turn(player2_board, "Player 1")
            print(recent_move_message)  # Show result of Player 1's turn

            # ends the game if all of player 2's ships are sunk
            if all(ship.is_sunk() for ship in player2_board.ships):
                print("Player 1 wins! Congratulations!")
                break

        # Player 2's turn
        else:
            # Display the result of the last turn if available
            if recent_move_message:
                print(recent_move_message)

            print("\nPlayer 2's turn:")
            print("Your board:")
            player2_board.display(show_ships=True)  # Show Player 2's board with their ships
            print("\nOpponent's board (Player 1):")
            player1_board.display()  # Show Player 1's board without revealing ships

            # Player 2 makes a move
            recent_move_message = player_turn(player1_board, "Player 2")
            print(recent_move_message)  # Show result of Player 2's turn

            # ends the game if all of player 1's ships are sunk
            if all(ship.is_sunk() for ship in player1_board.ships):
                print("Player 2 wins! Congratulations!")
                break

        # Add a line break after each turn to avoid overlap
        clear_screen()
        
        #increments the amount of turns the game has lasted
        turn += 1


# Player's turn to fire a shot.
def player_turn(opponent_board, player_name):
    while True:
        # prompts the player to enter the coordinates of where they want to fire
        print(f"\n{player_name}, it's your turn to fire.")
        shot = input("Enter coordinates to fire (e.g., A5): ").upper()

        # determines if the given coordinates are a valid input, prompting the player to try again if they are not.
        if len(shot) < 2 or not shot[0].isalpha() or not shot[1:].isdigit():
            print("Invalid input! Please enter a valid position like 'A5'.")
            continue

        col = ord(shot[0]) - 65  # Convert 'A' to 0, 'B' to 1, etc.
        row = int(shot[1:]) - 1  # Convert '5' to 4, etc.

        # determines if the coordinates are within the size of the board
        if row < 0 or row >= opponent_board.size or col < 0 or col >= opponent_board.size:
            print("Position out of bounds! Please try again.")
            continue

        # Fire at the opponent's board
        result = opponent_board.fire(row, col)

        # displays which player shot and where, stating if the spot was a hit or a miss
        # the player is also prompted to try again if they have already fired on the spot they are trying to target.
        if result == 1:
            # print(f"{player_name} chose {shot} and hit!")
            sleep(1)
            clear_screen()
            return f"{player_name} chose {shot} and hit!"
        elif result == 2:
            print("You've already fired at this location!")
            continue
        else:
            # print(f"{player_name} chose {shot} and missed!")
            sleep(1)
            clear_screen()
            return f"{player_name} chose {shot} and missed."

# clears the screen to keep players from seeing eachother's screens. 
def clear_screen():
    system('cls' if name == 'nt' else 'clear')

# Main function to start the game, creates the boards and begins the game loop.
if __name__ == "__main__":
    player_board, opponent_board = initialize_game()
    game_loop(player_board, opponent_board)
