import random
from random import randrange, choice
import copy


class Board:
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win = win
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.history = []

    def copy(self):
        new_board = Board(self.height, self.width, self.win)
        new_board.board = [[self.board[i][j] for j in range(self.width)] for i in range(self.height)]
        new_board.history = self.history.copy()
        return new_board

    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            def change(i):  # true if there'll be change in i-th tile
                if row[i] == 0 and row[i + 1] != 0:  # Move
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:  # Merge
                    return True
                return False

            return any(change(i) for i in range(len(row) - 1))

        check = dict()
        check['Left'] = lambda field: any(row_is_left_movable(row) for row in field)
        check['Right'] = lambda field: check['Left'](self.invert(field))
        check['Up'] = lambda field: check['Left'](self.transpose(field))
        check['Down'] = lambda field: check['Right'](self.transpose(field))

        if direction in check:
            return check[direction](self.board)
        else:
            return False

    def transpose(self, field):
        return [list(row) for row in zip(*field)]

    def invert(self, field):
        return [row[::-1] for row in field]

    def reset(self):
        self.board = [[0 for i in range(self.width)] for j in range(self.height)]
        self.history = []

    def spawn(self):
        empty_cells = [(i, j) for i in range(self.height) for j in range(self.width) if self.board[i][j] == 0]
        if empty_cells:
            new_element = 4 if randrange(100) > 89 else 2
            i, j = choice(empty_cells)
            self.board[i][j] = new_element

    def is_win(self):
        return any(any(i >= self.win for i in row) for row in self.board)

    def is_gameover(self):
        if any(0 in row for row in self.board):
            return False

        # Check if any moves are possible
        for direction in ['Left', 'Right', 'Up', 'Down']:
            if self.move_is_possible(direction):
                return False
        return True

    def move_left_row(self, row):
        # Move all non-zero elements to the left
        non_zero = [i for i in row if i != 0]

        # Merge adjacent equal elements
        merged = []
        i = 0
        while i < len(non_zero):
            if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:
                merged.append(non_zero[i] * 2)
                i += 2
            else:
                merged.append(non_zero[i])
                i += 1

        # Pad with zeros
        merged.extend([0] * (len(row) - len(merged)))
        return merged

    def move(self, direction):
        self.history.append(copy.deepcopy(self.board))

        if direction == 'Left':
            self.board = [self.move_left_row(row) for row in self.board]
        elif direction == 'Right':
            self.board = [self.move_left_row(row[::-1])[::-1] for row in self.board]
        elif direction == 'Up':
            transposed = self.transpose(self.board)
            moved = [self.move_left_row(row) for row in transposed]
            self.board = self.transpose(moved)
        elif direction == 'Down':
            transposed = self.transpose(self.board)
            moved = [self.move_left_row(row[::-1])[::-1] for row in transposed]
            self.board = self.transpose(moved)

    def undo(self):
        if self.history:
            self.board = self.history.pop()
            return True
        return False

    def display(self):
        print("\n" + "=" * 50)
        for row in self.board:
            print("|", end="")
            for cell in row:
                if cell == 0:
                    print(f"{'':^10}", end="|")
                else:
                    print(f"{cell:^10}", end="|")
            print()
        print("=" * 50)


class AI:
    def __init__(self, board):
        self.board = board

    def simulate_game(self, board_copy):
        """Simulate a random game from the current board state"""
        while not board_copy.is_win() and not board_copy.is_gameover():
            possible_moves = []
            for direction in ['Left', 'Right', 'Up', 'Down']:
                if board_copy.move_is_possible(direction):
                    possible_moves.append(direction)

            if not possible_moves:
                break

            # Make a random move
            move = choice(possible_moves)
            board_copy.move(move)
            board_copy.spawn()

        if board_copy.is_win():
            return board_copy.win

        total = 0
        num = 0
        for i in range(board_copy.height):
            for j in range(board_copy.width):
                if board_copy.board[i][j] > 0:
                    total += board_copy.board[i][j]
                    num += 1
        return total / num

    def get_best_move(self, simulations=50):
        """Get the best move based on win rate from simulations"""
        possible_moves = []
        for direction in ['Left', 'Right', 'Up', 'Down']:
            if self.board.move_is_possible(direction):
                possible_moves.append(direction)

        if not possible_moves:
            return None

        best_moves = []
        best_score = -1

        print(f"\nRunning {simulations} simulations for each possible move...")

        for move in possible_moves:
            score = 0
            for _ in range(simulations):
                # Create a copy and make the move
                board_copy = self.board.copy()
                board_copy.move(move)
                board_copy.spawn()

                # Simulate the rest of the game
                score += self.simulate_game(board_copy)

            print(f"Move {move}: {score} points")
            if score == best_score:
                best_moves.append(move)
            elif score > best_score:
                best_score = score
                best_moves = [move]

        best_move = random.choice(best_moves)
        print(f"\nBest move: {best_move} ({best_score} points)")
        return best_move


class Game:
    def __init__(self):
        self.board = None
        self.ai = None

    def get_game_settings(self):
        """Get game settings from user"""
        while True:
            try:
                height = int(input("Enter board height (default 4): ") or "4")
                width = int(input("Enter board width (default 4): ") or "4")
                win = int(input("Enter win tile value (default 2048): ") or "2048")

                if height < 2 or width < 2:
                    print("Height and width must be at least 2!")
                    continue
                if win < 4 or (win & (win - 1)) != 0:
                    print("Win tile must be a power of 2 and at least 4!")
                    continue

                return height, width, win
            except ValueError:
                print("Please enter valid numbers!")

    def start_new_game(self):
        """Start a new game with user-specified settings"""
        height, width, win = self.get_game_settings()
        self.board = Board(height, width, win)
        self.ai = AI(self.board)

        # Add initial tiles
        self.board.spawn()
        self.board.spawn()

        print(f"\nStarting new {height}x{width} game! Target: {win}")
        self.board.display()

    def restart_game(self):
        """Restart game with same settings"""
        if self.board:
            height, width, win = self.board.height, self.board.width, self.board.win
            self.board = Board(height, width, win)
            self.ai = AI(self.board)

            # Add initial tiles
            self.board.spawn()
            self.board.spawn()

            print(f"\nRestarting {height}x{width} game! Target: {win}")
            self.board.display()

    def show_menu(self):
        """Show game menu"""
        print("\nOptions:")
        print("1. Make your own move (w/a/s/d for up/left/down/right)")
        print("2. Let computer make a move")
        print("3. Undo last move")
        print("4. Restart game (same settings)")
        print("5. Start new game (new settings)")
        print("6. Quit")

    def show_end_game_menu(self):
        """Show end game menu"""
        print("\nGame Over Options:")
        print("1. Undo last move")
        print("2. Restart game (same settings)")
        print("3. Start new game (new settings)")
        print("4. Quit")

    def make_user_move(self):
        """Handle user move input"""
        move_map = {'w': 'Up', 'a': 'Left', 's': 'Down', 'd': 'Right'}

        while True:
            user_input = input("Enter move (w/a/s/d): ").lower()
            if user_input in move_map:
                direction = move_map[user_input]
                if self.board.move_is_possible(direction):
                    self.board.move(direction)
                    self.board.spawn()
                    return True
                else:
                    print("That move is not possible!")
            else:
                print("Invalid input! Use w/a/s/d for up/left/down/right")

    def make_ai_move(self):
        """Let AI make a move"""
        best_move = self.ai.get_best_move()
        if best_move:
            self.board.move(best_move)
            self.board.spawn()
            return True
        return False

    def play(self):
        """Main game loop"""
        print("Welcome to 2048 with AI Assistant!")
        self.start_new_game()

        while True:
            # Check game state
            if self.board.is_win():
                print("\n🎉 Congratulations! You reached the target tile! 🎉")
                self.handle_end_game()
                continue
            elif self.board.is_gameover():
                print("\n💀 Game Over! No more moves possible! 💀")
                self.handle_end_game()
                continue

            # Show menu and get user choice
            self.show_menu()

            try:
                choice = input("\nEnter your choice (1-6): ")

                if choice == '1':
                    if self.make_user_move():
                        self.board.display()
                elif choice == '2':
                    if self.make_ai_move():
                        self.board.display()
                    else:
                        print("No moves available!")
                elif choice == '3':
                    if self.board.undo():
                        print("Move undone!")
                        self.board.display()
                    else:
                        print("No moves to undo!")
                elif choice == '4':
                    self.restart_game()
                elif choice == '5':
                    self.start_new_game()
                elif choice == '6':
                    print("Thanks for playing!")
                    break
                else:
                    print("Invalid choice! Please enter 1-6.")

            except KeyboardInterrupt:
                print("\n\nThanks for playing!")
                break

    def handle_end_game(self):
        """Handle end game options"""
        while True:
            self.show_end_game_menu()

            try:
                choice = input("\nEnter your choice (1-4): ")

                if choice == '1':
                    if self.board.undo():
                        print("Move undone!")
                        self.board.display()
                        break
                    else:
                        print("No moves to undo!")
                elif choice == '2':
                    self.restart_game()
                    break
                elif choice == '3':
                    self.start_new_game()
                    break
                elif choice == '4':
                    print("Thanks for playing!")
                    exit()
                else:
                    print("Invalid choice! Please enter 1-4.")

            except KeyboardInterrupt:
                print("\n\nThanks for playing!")
                exit()


if __name__ == "__main__":
    game = Game()
    game.play()
