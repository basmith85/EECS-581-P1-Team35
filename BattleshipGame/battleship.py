"""
Battleship Game
This program implements a two-player Battleship game with manual ship placement. Players take turns firing
shots at each other's board, and the first player to sink all the opponent's ships wins.
Inputs: Player inputs for placing ships and firing shots
Output: Hits, misses, ship status (sunk or not)
Author: Darshil Patel, Blake Smith, Ike Phillips, Brady Holland, Kansas Lees (add your names)
Created on: 09/13/24
"""

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
    player1_board = Board()
    player2_board = Board()

    # Ask the players how many ships they want to play with
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
    print("\n" * 50)  # This clears the screen

    # Player 2 places ships
    print("\nPlayer 2, place your ships:")
    for ship in ships:
        place_ship_manually(player2_board, ship)
    print("\n" * 50)
    return player1_board, player2_board


def place_ship_manually(board, ship):
    board.display(show_ships=True)
    print(f"\nPlace your {ship.name} (size {ship.size})")

    while True:
        pos = input("Enter starting position (e.g., A5): ").upper()
        if len(pos) < 2 or not pos[0].isalpha() or not pos[1:].isdigit():
            print("Invalid input format! Please enter a valid position like 'A5'.")
            continue

        col = ord(pos[0]) - 65  # Convert 'A' to 0, 'B' to 1, etc.
        row = int(pos[1:]) - 1  # Convert '5' to 4, etc.

        if row < 0 or row >= board.size or col < 0 or col >= board.size:
            print("Position out of bounds! Please try again.")
            continue

        # Skip direction prompt for 1x1 ships
        if ship.size == 1:
            if board.place_ship(ship, row, col, horizontal=True):
                print(f"{ship.name} placed successfully!")
                break
        else:
            direction = input("Enter direction (North, South, East, West - N/S/E/W): ").upper()
            if direction not in ('N', 'S', 'E', 'W'):
                print("Invalid direction! Please enter 'N', 'S', 'E', or 'W'.")
                continue

            overlap = False  # Variable to track if there’s an overlap

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

            if all(ship.is_sunk() for ship in player1_board.ships):
                print("Player 2 wins! Congratulations!")
                break

        # Add a line break after each turn to avoid overlap
        print("\n" * 2)
        
        turn += 1


# Player's turn to fire a shot.
def player_turn(opponent_board, player_name):
    while True:
        print(f"\n{player_name}, it's your turn to fire.")
        shot = input("Enter coordinates to fire (e.g., A5): ").upper()

        # Validate input
        if len(shot) < 2 or not shot[0].isalpha() or not shot[1:].isdigit():
            print("Invalid input! Please enter a valid position like 'A5'.")
            continue

        col = ord(shot[0]) - 65  # Convert 'A' to 0, 'B' to 1, etc.
        row = int(shot[1:]) - 1  # Convert '5' to 4, etc.

        if row < 0 or row >= opponent_board.size or col < 0 or col >= opponent_board.size:
            print("Position out of bounds! Please try again.")
            continue

        # Fire at the opponent's board
        result = opponent_board.fire(row, col)
        if result:
            return f"{player_name} chose {shot} and hit!"
        else:
            return f"{player_name} chose {shot} and missed."


# Main function to start the game.
if __name__ == "__main__":
    player_board, opponent_board = initialize_game()
    game_loop(player_board, opponent_board)
