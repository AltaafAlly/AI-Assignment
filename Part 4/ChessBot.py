import chess.engine
import random
from reconchess import Player, Color, Square, GameHistory, WinReason
from typing import List, Optional, Tuple


# Define the path to the Stockfish executable
stockfish_path = r'C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish'

# Define the path to the Stockfish executable for the automarker
#stockfish_path = '/opt/stockfish/stockfish'
class BaselineAgent(Player):
    def __init__(self):
        super().__init__()
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
        self.current_state = None
        self.states = set()

    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
        self.current_state = board.fen()

    def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Square):
        if captured_my_piece:
            # Narrow down the list of possible states based on opponent's capture
            possible_states = set()
            for state in self.states:
                # Check if the capture square matches any captured pieces in the state
                board = chess.Board(state)
                if board.piece_at(capture_square):
                    possible_states.add(state)
            self.states = possible_states

    def choose_sense(self, sense_actions: List[int], move_actions: List[chess.Move], seconds_left: float) -> int:
        # Choose where to sense on the board
        sense_square = random.choice([sq for sq in sense_actions if 1 < sq < 64])
        return sense_square



    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
        # Narrow down the list of possible states based on the sensing result
        possible_states = set()
        for state in self.states:
            board = chess.Board(state)
            for square, piece in sense_result:
                if piece is not None:
                    board.set_piece_at(square, piece)
            possible_states.add(board.fen())
        self.states = possible_states

    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        # Select a move to play
        return random.choice(move_actions)

    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move], captured_opponent_piece: bool, capture_square: Optional[Square]):
        # Update the states based on the outcome of the move
        if taken_move:
            new_state = chess.Board(self.current_state)
            new_state.push(taken_move)
            self.states.add(new_state.fen())

    def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason], game_history: GameHistory):
        # Close the connection to Stockfish
        self.engine.quit()

