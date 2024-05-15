from reconchess import utilities
from reconchess import Player
import chess
import random
import chess.engine
from reconchess import Player, List, Optional, chess
import chess.engine
import random
from reconchess import *
import os
import time

stockfish_path = (
    r"C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish"
)
# Define the path to the Stockfish executable for the automarker
# stockfish_path = '/opt/stockfish/stockfish'


# WORKING BASELINE CODE DONT BREAK

class ImprovedAgent(Player):
    def __init__(self):
        self.board = None
        self.color = None
        self.my_piece_captured_square = None
        self.possible_states = set()
        self.engine = chess.engine.SimpleEngine.popen_uci(
            stockfish_path, setpgrp=True)

    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
        self.board = board.copy()
        self.color = color
        self.possible_states = {board.fen()}

    def handle_opponent_move_result(
        self, captured_my_piece: bool, capture_square: Optional[Square]
    ):
        if captured_my_piece and capture_square is not None:
            for state in self.possible_states:
                # Create a copy of the current board
                board = chess.Board(state)
                # Check if there is a piece at the capture square
                if board.piece_at(capture_square) is not None:
                    # Remove the captured piece from the board
                    board.remove_piece_at(capture_square)
                    # Add the FEN representation of the modified board to possible states
                    self.possible_states.add(board.fen())

    def handle_sense_result(
        self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]
    ):
        new_possible_states = set()
        for square, piece in sense_result:
            # Create a copy of the current board
            new_board = self.board.copy()
            # Set the piece at the sensed square
            new_board.set_piece_at(square, piece)
            # Add the FEN representation of the new board to possible states
            self.possible_states.add(new_board.fen())

    def choose_sense(
    self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float,
    ) -> Optional[Square]:
        while True:
            # Choose a random sense action
            sense_square = random.choice(sense_actions)

            # Check if the 3x3 region around the sense square is fully on the board
            rank, file = chess.square_rank(sense_square), chess.square_file(sense_square)
            if 1 <= rank <= 6 and 1 <= file <= 6:
                return sense_square


    #BEST VERSION OF CHOOSE_MOVE
    def choose_move(
        self, move_actions: List[chess.Move], seconds_left: float
    ) -> Optional[chess.Move]:
        best_moves = {}
        num_boards = len(self.possible_states)
        time_limit = 10 / num_boards
        print("number of boards:", num_boards, "time for move:", time_limit)
        
        for state in random.sample(list(self.possible_states), min(num_boards, 10000)):
            board = chess.Board(state)
            board.turn = self.color
            board.clear_stack()

            valid_moves = [move for move in move_actions if board.is_legal(move)]

            if valid_moves:
                try:
                    result = self.engine.play(board, chess.engine.Limit(time=time_limit), root_moves=valid_moves)
                    best_move = result.move
                    best_moves[state] = best_move
                except (chess.engine.EngineTerminatedError, ValueError):
                    self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
            else:
                best_moves[state] = None

        if best_moves:
            # Count the frequency of each move across all possible states
            move_counts = {}
            for move in best_moves.values():
                if move is not None:
                    move_counts[move] = move_counts.get(move, 0) + 1

            # Select the move with the highest count that is also a valid action
            valid_moves = [move for move in move_counts if move in move_actions]
            if valid_moves:
                best_move = max(valid_moves, key=move_counts.get)
                return best_move

        # If no valid move is found, return a random move from the available move actions
        if move_actions:
            return random.choice(move_actions)
        else:
            return None

    def handle_opponent_move_result(
        self, captured_my_piece: bool, capture_square: Optional[Square]
    ):
        if captured_my_piece and capture_square is not None:
            new_possible_states = set()
            for state in self.possible_states:
                board = chess.Board(state)
                if board.piece_at(capture_square) is not None:
                    board.remove_piece_at(capture_square)
                    new_possible_states.add(board.fen())
            self.possible_states.update(new_possible_states)

    def handle_game_end(
        self,
        winner_color: Optional[Color],
        win_reason: Optional[WinReason],
        game_history: GameHistory,
    ):
        try:
            self.engine.quit()
        except chess.engine.EngineTerminatedError:
            pass
