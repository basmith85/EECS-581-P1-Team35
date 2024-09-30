"""
Battleship Game
This program implements a two-player Battleship game with manual ship placement. Players take turns firing
shots at each other's board, and the first player to sink all the opponent's ships wins.
Inputs: Player inputs for placing ships and firing shots
Output: Hits, misses, ship status (sunk or not)
Sources: Group 6, ChatGPT
Author: Zach Alwin, Kristin Böckmann, Lisa Phan, Nicholas Hausler, Vinayak Jha
Created on: 09/16/2024
"""
# Module Importing
from time import sleep
from random import randint, choice
directions = ['N', 'S', 'E', 'W']
import sys

DBG = False

# Ship class represents a ship's properties: name, size, coordinates, and hits it has taken
class Ship:
    # creates the init function for the ship class defining name, size, coordinates, and hits
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []  # List of tuples for the ship's coordinates
        self.hits = 0  # Track the number of hits on the ship

    # function to determine if a ship has been sunk or not
    def is_sunk(self):
        """Returns True if the ship is fully sunk (i.e., hits equal its size)."""
        return self.hits == self.size


# Board class represents the game board for both the player and opponent
class Board:
    # creates the init function for the board class defining size, grid, ships, and shots
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

    # places ships on the board at the given row and column, boolean value to determine if the ship is placed horizontally or not
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
                ship.coordinates.append((start_row, start_col + i))  # Adds the ships coordinates to the board's list
        else:  # vertical ship
            if start_row + ship.size > self.size:
                return False  # Ship would go out of bounds vertically
            for i in range(ship.size):
                if self.grid[start_row + i][start_col] != '~':
                    return False  # Space is already taken
            for i in range(ship.size):
                self.grid[start_row + i][start_col] = 'S'
                ship.coordinates.append((start_row + i, start_col))  # Adds the ships coordinates to the board's list

        self.ships.append(ship)  # Adds the ship to the list of ships on the board
        return True

    def fire(self, row, col, bomb=False):
        """Fire a shot at the opponent's board and determine hit or miss."""
        # Determines if a spot on the board has been fired on already by a player
        if (row, col) in self.shots:
            if not bomb:
                print("Already fired at this location!")
            return 2
        # "Fires" the shot on the board, determining if it is a hit or not and adding the shot to the boards list of shots
        self.shots.add((row, col))
        if self.grid[row][col] == 'S': # Ship is marked with an "S"
            if not bomb:
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
            if not bomb: 
                print("Miss!")
            self.grid[row][col] = 'O'  # Mark miss on the board
            return False
# The AI class defines the behavior of the computer opponent, including placing ships and firing at the player's board
class AI:
    # Initializes the AI with the game board and difficulty level
    def __init__(self, board, difficulty):
        self.board = board  # Stores the AI's board
        self.difficulty = difficulty  # Sets the AI's difficulty mode
        self.last_hit = None  # Tracks the last hit made by the AI to improve targeting in medium/hard modes
        self.possible_targets = []  # Stores potential target coordinates for intelligent shots

    # Places AI ships randomly on the board. Ships will be placed without overlapping or going out of bounds
    def place_ships(self, ships):
        print("\nAI is placing ships...")  # Notify that AI is placing ships
        for ship in ships:  # Loop over each ship that needs to be placed
            placed = False
            while not placed:  # Keep trying until a valid placement is found
                row = randint(0, self.board.size - 1)  # Choose a random row
                col = randint(0, self.board.size - 1)  # Choose a random column
                direction = choice(directions)  # Randomly choose the direction to place the ship
                placed = self.board.place_ship(ship, row, col, horizontal=(direction in ['E', 'W']))  # Attempt to place the ship

    # AI fires at the opponent's board. The behavior varies based on the difficulty level
    def fire(self, opponent_board):
        from random import randint  # Import random number generator

        # Function to get a random valid shot
        def get_random_shot():
            while True:
                row = randint(0, opponent_board.size - 1)  # Random row
                col = randint(0, opponent_board.size - 1)  # Random column
                if (row, col) not in opponent_board.shots:  # Check if this position was not shot before
                    return row, col  # Return the random shot

        # Returns a list of valid adjacent coordinates around a given row and column
        def get_adjacent_shots(row, col):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Possible directions (N, S, E, W)
            return [(row + dr, col + dc) for dr, dc in directions if 0 <= row + dr < opponent_board.size and 0 <= col + dc < opponent_board.size]

        # Match case to decide the AI's firing strategy based on the difficulty level
        match self.difficulty.lower():
            case 'easy':  # Easy mode: Random shots with no strategy
                row, col = get_random_shot()  # Get a random shot
                return opponent_board.fire(row, col)  # Fire at the chosen coordinates

            case 'medium':  # Medium mode: Targets around previous hits
                if self.last_hit and not self.possible_targets:  # If there's a last hit and no targets, get adjacent ones
                    self.possible_targets = get_adjacent_shots(*self.last_hit)
                if self.possible_targets:  # If there are possible targets, shoot at the next one
                    row, col = self.possible_targets.pop(0)
                    while (row, col) in opponent_board.shots:  # Ensure not to fire at previously hit positions
                        if not self.possible_targets:  # If no valid targets remain, choose a random shot
                            row, col = get_random_shot()
                            break
                        row, col = self.possible_targets.pop(0)
                else:  # If no last hit or possible targets, pick a random shot
                    row, col = get_random_shot()

                result = opponent_board.fire(row, col)  # Fire at the determined coordinates
                if result == 1:  # Hit but not sunk
                    self.last_hit = (row, col)  # Store this hit as the last hit
                elif result == 3:  # Ship sunk
                    self.last_hit = None  # Reset the last hit if the ship is sunk
                    self.possible_targets = []  # Clear the target list
                return result

            case 'hard':  # Hard mode: Fires directly at specific ship coordinates not yet hit
                for ship in opponent_board.ships:
                    for row, col in ship.coordinates:
                        if (row, col) not in opponent_board.shots:  # Shoot at any unhit ship coordinate
                            return opponent_board.fire(row, col)


# Sets up the game by initializing the player and AI boards, and places ships for both sides.
def initialize_game():
    player_board = Board()  # Create a new board for the player
    ai_board = Board()  # Create a new board for the AI

    # Loop to get the difficulty level input from the user
    while True:
        try:
            difficulty = input("Enter AI difficulty ('Easy', 'Medium', 'Hard'): ").lower()  # Prompt for difficulty
            if difficulty not in ('easy', 'medium', 'hard'):  # Validate input
                print("Invalid difficulty! Please enter 'Easy', 'Medium', or 'Hard'.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter 'Easy', 'Medium', or 'Hard'.")

    # Loop to get the number of ships the player wants.
    while True:
        try:
            num_ships = int(input("Enter the number of ships (1 to 5): "))  # Prompt for number of ships
            if num_ships < 1 or num_ships > 5:  # Validate input
                print("Please enter a number between 1 and 5.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 5.")

    player_ships = [Ship(f"Ship {i}", i) for i in range(1, num_ships + 1)]  # Create player ships based on input

    print("\nPlayer, place your ships:")  # Notify the player to place ships
    for ship in player_ships:  # Loop for placing each player's ship
        place_ship_manually(player_board, ship)

    #clear_screen()  # Optional screen clear

    ai_ships = [Ship(f"Ship {i}", i) for i in range(1, num_ships + 1)]  # Create AI ships based on the same input

    ai = AI(ai_board, difficulty)  # Initialize the AI with the board and difficulty level
    ai.place_ships(ai_ships)  # Place AI ships on the board
    if DBG:  # If debugging is enabled, display AI's board with ships visible
        ai.board.display(show_ships=True)
    return player_board, ai_board, ai  # Return initialized boards and AI instance


# Allows the player to manually place a ship on the board
def place_ship_manually(board, ship):
    board.display(show_ships=True)  # Display the current state of the board
    print(f"\nPlace your {ship.name} (size {ship.size})")  # Prompt the player to place their ship

    # Continue prompting until the ship is placed correctly
    while True:
        pos = input("Enter starting position (e.g., A5): ").upper()  # Get the starting position
        if len(pos) < 2 or not pos[0].isalpha() or not pos[1:].isdigit():  # Validate input format
            print("Invalid input format! Please enter a valid position like 'A5'.")
            continue

        col = ord(pos[0]) - 65  # Convert column from letter to number (e.g., 'A' -> 0)
        row = int(pos[1:]) - 1  # Convert row from 1-based to 0-based index

        # Check if the position is within board boundaries.
        if row < 0 or row >= board.size or col < 0 or col >= board.size:
            print("Position out of bounds! Please try again.")
            continue

        # If the ship is of size 1, no direction choice is needed.
        if ship.size == 1:
            if board.place_ship(ship, row, col, horizontal=True):  # Attempt to place the ship.
                print(f"{ship.name} placed successfully!")
                break
        else:
            # Prompt the user to choose the direction of the ship.
            direction = input("Enter direction (North, South, East, West - N/S/E/W): ").upper()
            if direction not in ('N', 'S', 'E', 'W'):  # Validate the direction input.
                print("Invalid direction! Please enter 'N', 'S', 'E', or 'W'.")
                continue

            overlap = False  # Track if the ship overlaps with another.

            # Handle ship placement based on the chosen direction.
            if direction == 'E':
                if col + ship.size > board.size:  # Check if the ship goes out of bounds to the East.
                    print("Ship goes out of bounds to the East! Please try again.")
                    continue
                for i in range(ship.size):  # Check for overlap.
                    if board.grid[row][col + i] != '~':
                        overlap = True
                        break
                if overlap:
                    print("Ship overlaps with another ship! Please try again.")
                    continue
                horizontal = True
                if board.place_ship(ship, row, col, horizontal=horizontal):  # Place the ship horizontally.
                    print(f"{ship.name} placed successfully!")
                    break
                    
# Main game loop that alternates turns between Player 1 and Player 2.
def game_loop(player_board, ai_board, ai):
    turn = 1
    recent_move_message = ""
    bomb_used = False  # Track if the bomb has been used

    while True:
        print(f"\n--- Turn {turn} ---")

        # Print the most recent move if the game still continues
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

            # Print message for a user win
            if all(ship.is_sunk() for ship in ai_board.ships):
                print("Player wins! Congratulations!")
                break
        else:  # Continue the game if no user win
            print("\nAI's turn:")
            sleep(2)
            result = ai.fire(player_board)
            recent_move_message = "AI fired and " + ("hit!" if result == 1 or result == 3 else "missed.")
            print(recent_move_message)

            # Print message for an AI win
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
        result = opponent_board.fire(row, c, True)
        if result in (1, 3):  # Hit
            hits.append((row, c))

    # Fire bomb in the entire column
    for r in range(opponent_board.size):  # Iterate over the entire column
        result = opponent_board.fire(r, col, True)
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

            col = ord(shot[0]) - 65  # Set column
            row = int(shot[1:]) - 1  # Set row 

            # Validate the row and column when placing ships and handle errors accordingly
            if row < 0 or row >= opponent_board.size or col < 0 or col >= opponent_board.size:
                print("Position out of bounds! Please try again.") 
                continue

            # Fire the bomb
            hit_positions = fire_bomb(opponent_board, row, col)
            bomb_used = True  # Mark the bomb as used

            if hit_positions:
                hit_details = ", ".join([f"{chr(col + 65)}{row + 1}" for row, col in hit_positions])  # Print hit details with special ability
                print(f"{player_name} used a bomb and hit: {hit_details}!")
            else:
                print(f"{player_name} used a bomb but missed all targets.") 
            return {"bomb_used": bomb_used}  # End turn after bomb use

        elif choice == "shot": 
            # Prompt the player to enter coordinates to fire at, converting input to uppercase for consistency
            shot = input("Enter coordinates to fire (e.g., A5): ").upper()

            # Validate the input format. It should have at least two characters: one letter and one number
            if len(shot) < 2 or not shot[0].isalpha() or not shot[1:].isdigit():
                print("Invalid input! Please enter a valid position like 'A5'.")
                continue

            # Convert the column and row to appropriate format
            col = ord(shot[0]) - 65
            row = int(shot[1:]) - 1

            # Check if the entered coordinates are within the boundaries of the opponent's board
            if row < 0 or row >= opponent_board.size or col < 0 or col >= opponent_board.size:
                print("Position out of bounds! Please try again.")
                continue

            # Fire at the specified coordinates on the opponent's board and store the result
            result = opponent_board.fire(row, col)

            # Conditions for output and storing result
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


# Main function to start the game, creates the boards and begins the game loop.
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        DBG = int(sys.argv[1]) == 1
    player_board, ai_board, ai = initialize_game()
    game_loop(player_board, ai_board, ai)
