import chess.engine
import os
from reconchess import Player, Color, chess, Square
from typing import List, Optional

# Define the path to the Stockfish executable for local machine
#stockfish_path = r'C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish'

# Define the path to the Stockfish executable for the automarker
stockfish_path = '/opt/stockfish/stockfish'
# Define TroutBot class
class TroutBot(Player):

    def __init__(self):
        super().__init__()
        self.engine = None
        self.board = None
        self.color = None

        # Initialize the Stockfish engine
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)

    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
        self.board = board
        self.color = color

    def choose_move(self, legal_moves: chess.LegalMoveGenerator, seconds_left: float) -> Optional[chess.Move]:
    # Check if any move captures the opponent's king
        for move in legal_moves:
            if self.board.is_capture(move) and self.board.piece_at(move.to_square) is not None and \
                    self.board.piece_at(move.to_square).piece_type == chess.KING and \
                    self.board.piece_at(move.to_square).color != self.color:
                return move

        try:
            # Ask Stockfish for a move with a time limit of 0.5 seconds
            result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
            return result.move
        except chess.engine.EngineTerminatedError:
            print('Stockfish Engine died')
        except chess.engine.EngineError:
            print('Stockfish Engine bad state at "{}"'.format(self.board.fen()))

        return None


    # Implement other necessary methods for TroutBot

def main():
    # Initialize TroutBot
    bot = TroutBot()

    try:
        # Read input FEN string
        fen = input().strip()

        # Initialize the board and game
        board = chess.Board(fen)
        color = chess.COLOR_NAMES[board.turn]

        # Call TroutBot to generate move
        bot.handle_game_start(Color(color), board, 'Opponent')
        move = bot.choose_move(board.legal_moves, seconds_left=60)  # Adjust time limit as needed

        # Output move in the required format
        if move:
            print(move.uci())
        else:
            print("No valid move found.")

    except Exception as e:
        print("An error occurred:", e)
        return

    finally:
        # Close Stockfish engine
        bot.engine.quit()


if __name__ == "__main__":
    main()
