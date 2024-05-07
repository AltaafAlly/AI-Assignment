import random
import chess.engine
from reconchess import Player, List, Optional, chess
import chess.engine
import random
from reconchess import *
import os

class ImprovedBot(Player):
    def __init__(self):
            self.board = None
            self.color = None
            self.my_piece_captured_square = None

            # initialize the stockfish engine
            self.engine = chess.engine.SimpleEngine.popen_uci(
                stockfish_path, setpgrp=True)

    def value_of_piece(self, piece):
        if piece is None:
            return 0
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }
        abs_value = piece_values.get(piece.piece_type, 0)
        return abs_value if piece.color == self.color else -abs_value

    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
        self.board = board
        self.color = color

    def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
        # if the opponent captured our piece, remove it from our board.
        self.my_piece_captured_square = capture_square
        if captured_my_piece:
            self.board.remove_piece_at(capture_square)

    def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> \
            Optional[Square]:
        # if our piece was just captured, sense where it was captured
        if self.my_piece_captured_square:
            return self.my_piece_captured_square

        # if we might capture a piece when we move, sense where the capture will occur
        future_move = self.choose_move(move_actions, seconds_left)
        if future_move is not None and self.board.piece_at(future_move.to_square) is not None:
            return future_move.to_square

        # otherwise, just randomly choose a sense action, but don't sense on a square where our pieces are located
        for square, piece in self.board.piece_map().items():
            if piece.color == self.color:
                sense_actions.remove(square)
        return random.choice(sense_actions)

    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
        # add the pieces in the sense result to our board
        for square, piece in sense_result:
            self.board.set_piece_at(square, piece)

    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        # if we might be able to take the king, try to
        enemy_king_square = self.board.king(not self.color)
        if enemy_king_square:
            # if there are any ally pieces that can take king, execute one of those moves
            enemy_king_attackers = self.board.attackers(self.color, enemy_king_square)
            if enemy_king_attackers:
                attacker_square = enemy_king_attackers.pop()
                return chess.Move(attacker_square, enemy_king_square)
        
        # Piece Captures (Prioritized)
        capture_moves = []
        for move in move_actions:
            if self.board.is_capture(move):
                capture_moves.append((move, self.value_of_piece(self.board.piece_at(move.to_square)))) 
        
        capture_moves.sort(key=lambda x: x[1], reverse=True) # Highest value captures first

        for move, _ in capture_moves:
            return move
        
        capture_moves = []
        for move in move_actions:
            if self.board.is_capture(move) and self.board.piece_at(move.to_square) is not None:  # Check for piece
                capture_moves.append((move, self.value_of_piece(self.board.piece_at(move.to_square)))) 
        
        capture_moves.sort(key=lambda x: x[1], reverse=True)
        
        # otherwise, try to move with the stockfish chess engine
        try:
            self.board.turn = self.color
            self.board.clear_stack()
            result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
            return result.move
        except chess.engine.EngineTerminatedError:
            print('Stockfish Engine died')
        except chess.engine.EngineError:
            print('Stockfish Engine bad state at "{}"'.format(self.board.fen()))

        # if all else fails, pass
        return None

    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
                        captured_opponent_piece: bool, capture_square: Optional[Square]):
        # if a move was executed, apply it to our board
        if taken_move is not None:
            self.board.push(taken_move)

    def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason],
                        game_history: GameHistory):
        try:
            # if the engine is already terminated then this call will throw an exception
            self.engine.quit()
        except chess.engine.EngineTerminatedError:
            pass