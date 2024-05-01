import chess.engine
from collections import defaultdict

# Define the path to the Stockfish executable
stockfish_path = r'C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish'

# Define the path to the Stockfish executable for the automarker
#stockfish_path = '/opt/stockfish/stockfish'
# Define TroutBot class
class TroutBot:
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)

    def compute_move(self, fen: str) -> str:
        board = chess.Board(fen)
        try:
            result = self.engine.play(board, chess.engine.Limit(time=0.1))
            return result.move.uci()
        except Exception as e:
            print("An error occurred while computing move for board {}: {}".format(fen, e))
            return ""

def main():
    # Read the number of boards
    num_boards = int(input())

    # Create a dictionary to store move frequencies
    move_counts = defaultdict(int)

    # Initialize TroutBot
    bot = TroutBot()

    # Process each board
    for _ in range(num_boards):
        fen = input().strip()
        move = bot.compute_move(fen)
        move_counts[move] += 1

    # Find the most common move
    max_count = max(move_counts.values())
    most_common_moves = [move for move, count in move_counts.items() if count == max_count]
    chosen_move = sorted(most_common_moves)[0]  # Choose the first alphabetically if there are ties

    # Output the chosen move
    print(chosen_move)

    # Close the engine
    bot.engine.quit()

if __name__ == "__main__":
    main()
