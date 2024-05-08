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

# Define the path to the Stockfish executable
stockfish_path = (
    r"C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish"
)
# Define the path to the Stockfish executable for the automarker
# stockfish_path = '/opt/stockfish/stockfish'


#WORKING CODE DONT BREAK 

class ImprovedAgent(Player):
    def __init__(self):
        self.board = None
        self.color = None
        self.my_piece_captured_square = None
        self.possible_states = set()
        self.engine = chess.engine.SimpleEngine.popen_uci(
            stockfish_path, setpgrp=True)

    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
        self.board = board.copy() if board else None
        self.color = color
        self.possible_states = {board.fen()} if board else set()

    def handle_opponent_move_result(
        self, captured_my_piece: bool, capture_square: Optional[Square]
    ):
        self.my_piece_captured_square = capture_square
        if captured_my_piece and capture_square is not None:
            self.possible_states = {
                state
                for state in self.possible_states
                if chess.Board(state).piece_at(capture_square) is not None
            }
            for state in self.possible_states:
                board = chess.Board(state)
                board.remove_piece_at(capture_square)
                self.possible_states.remove(state)
                self.possible_states.add(board.fen())
        else:
            self.possible_states = {state for state in self.possible_states}

    def choose_sense(
        self,
        sense_actions: List[Square],
        move_actions: List[chess.Move],
        seconds_left: float,
    ) -> Optional[Square]:
        # If our piece was just captured, sense where it was captured
        if self.my_piece_captured_square:
            return self.my_piece_captured_square

        # If we might capture a piece when we move, sense where the capture will occur
        future_move = self.choose_move(move_actions, seconds_left)
        if (
            future_move is not None
            and self.board.piece_at(future_move.to_square) is not None
        ):
            return future_move.to_square

        # Sense squares near the opponent's king
        opponent_king_square = self.board.king(not self.color)
        if opponent_king_square:
            surrounding_squares = [
                square
                for square in chess.SQUARES
                if chess.square_distance(square, opponent_king_square) <= 2
            ]
            valid_sense_squares = [
                square for square in surrounding_squares if square in sense_actions
            ]
            if valid_sense_squares:
                return random.choice(valid_sense_squares)

        # If no specific sensing strategy applies, choose a random sense action
        return random.choice(sense_actions)

    def handle_sense_result(
        self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]
    ):
        # Update the current board with the sensed information
        for square, piece in sense_result:
            self.board.set_piece_at(square, piece)

        self.possible_states = {
            state
            for state in self.possible_states
            if all(
                chess.Board(state).piece_at(square) == piece
                for square, piece in sense_result
            )
        }

    def choose_move(
        self, move_actions: List[chess.Move], seconds_left: float
    ) -> Optional[chess.Move]:
        # Check if the king is under attack
        king_square = self.board.king(self.color)
        if king_square is not None:
            attackers = self.board.attackers(not self.color, king_square)
            if attackers:
                # Check if the king can capture the attacker
                for attacker_square in attackers:
                    capturing_move = chess.Move(king_square, attacker_square)
                    if capturing_move in move_actions:
                        return capturing_move

        # Check if the opponent's king can be captured
        enemy_king_square = self.board.king(not self.color)
        if enemy_king_square:
            enemy_king_attackers = self.board.attackers(
                self.color, enemy_king_square)
            if enemy_king_attackers:
                attacker_square = enemy_king_attackers.pop()
                capturing_move = chess.Move(attacker_square, enemy_king_square)
                if capturing_move in move_actions:
                    return capturing_move

        # Use majority voting to select a move
        move_counts = {}
        num_boards = len(self.possible_states)
        if num_boards > 0:
            time_limit = min(10 / num_boards, 0.5)
            possible_states_list = list(
                self.possible_states)  # Convert set to list
            for state in random.sample(possible_states_list, min(num_boards, 10000)):
                board = chess.Board(state)
                board.turn = self.color
                board.clear_stack()
                valid_moves = [
                    move for move in move_actions if board.is_legal(move)]
                if valid_moves:
                    result = self.engine.play(
                        board,
                        chess.engine.Limit(time=time_limit),
                        root_moves=valid_moves,
                    )
                    move = result.move
                    if move is not None:
                        move_counts[move] = move_counts.get(move, 0) + 1

        if move_counts:
            best_move = max(move_counts, key=move_counts.get)
            return best_move

        # If no valid move is found, return a random move from the available move_actions
        if move_actions:
            return random.choice(move_actions)
        else:
            return None

    def handle_move_result(
        self,
        requested_move: Optional[chess.Move],
        taken_move: Optional[chess.Move],
        captured_opponent_piece: bool,
        capture_square: Optional[Square],
    ):
        if taken_move is not None:
            self.possible_states = {
                state
                for state in self.possible_states
                if chess.Board(state).is_legal(taken_move)
            }
            self.possible_states = {
                chess.Board(state).push(taken_move).fen()
                for state in self.possible_states
                if chess.Board(state).push(taken_move) is not None
            }

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
