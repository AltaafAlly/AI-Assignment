from reconchess import utilities, Player, List, Optional, Color, Square, WinReason, GameHistory, Tuple
import chess
import random
import chess.engine
import os
import time

# Define the path to the Stockfish executable
stockfish_path = r"C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish"
# Define the path to the Stockfish executable for the automarker
# stockfish_path = '/opt/stockfish/stockfish'

class ImprovedAgent(Player):
    def __init__(self):
        self.board = None
        self.color = None
        self.my_piece_captured_square = None
        self.possible_states = set()
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)

    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
        self.board = board.copy()
        self.color = color
        self.possible_states = {board.fen()}

    def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
        if captured_my_piece and capture_square is not None:
            new_possible_states = set()
            for state in self.possible_states:
                board = chess.Board(state)
                if board.piece_at(capture_square) is not None:
                    board.remove_piece_at(capture_square)
                    new_possible_states.add(board.fen())
            self.possible_states.update(new_possible_states)

    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
        new_possible_states = set()
        
        for state in self.possible_states:
            board = chess.Board(state)
            valid_state = True
            
            for square, piece in sense_result:
                if piece is None:
                    if board.piece_at(square) is not None:
                        board.remove_piece_at(square)
                else:
                    if board.piece_at(square) != piece:
                        board.set_piece_at(square, piece)
            
            new_possible_states.add(board.fen())
        
        self.possible_states.update(new_possible_states)

    def choose_sense(
    self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float,) -> Optional[Square]:
        while True:
            # Choose a random sense action
            sense_square = random.choice(sense_actions)

            # Check if the 3x3 region around the sense square is fully on the board
            rank, file = chess.square_rank(sense_square), chess.square_file(sense_square)
            if 1 <= rank <= 6 and 1 <= file <= 6:
                return sense_square

    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        best_moves = {}
        num_boards = len(self.possible_states)

        # Limit number of boards to 10,000 if it exceeds
        boards_to_sample = min(num_boards, 10000)
        # Set time limit for Stockfish
        time_limit = 10 / num_boards if num_boards > 0 else 10
        print("Number of boards:", num_boards, "Time for move:", time_limit)

        # Sample boards randomly
        for state in random.sample(list(self.possible_states), boards_to_sample):
            board = chess.Board(state)
            board.turn = self.color
            board.clear_stack()

            enemy_king_square = board.king(not self.color)
            if enemy_king_square:
                enemy_king_attackers = board.attackers(self.color, enemy_king_square)
                if enemy_king_attackers:
                    attacker_square = enemy_king_attackers.pop()
                    return chess.Move(attacker_square, enemy_king_square)

            valid_moves = [move for move in move_actions if board.is_legal(move)]

            if valid_moves:
                for move in valid_moves:
                    try:
                        # Verify if the move is legal before sending to engine
                        board.push(move)
                        self.engine.play(board, chess.engine.Limit(time=time_limit))
                        best_moves[state] = move
                        board.pop()
                        break
                    except (chess.engine.EngineTerminatedError, ValueError, chess.engine.EngineError):
                        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
            else:
                best_moves[state] = None

        if best_moves:
            move_counts = {}
            for move in best_moves.values():
                if move is not None:
                    move_counts[move] = move_counts.get(move, 0) + 1

            valid_moves = [move for move in move_counts if move in move_actions]
            if valid_moves:
                # Choose the move with the highest count
                best_move = max(valid_moves, key=move_counts.get)
                return best_move

        # If no moves are available or no consensus, choose a random move
        if move_actions:
            return random.choice(move_actions)
        else:
            return None

    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move], captured_opponent_piece: bool, capture_square: Optional[Square]):
        if taken_move is None:
            return

        new_possible_states = set()

        for state in self.possible_states:
            board = chess.Board(state)

            # Check if the requested move was legal in this state
            if requested_move is not None and requested_move in board.legal_moves:
                # Apply the move
                board.push(chess.Move.from_uci(taken_move))

                # Handle the capture if one occurred
                if captured_opponent_piece and capture_square is not None:
                    board.remove_piece_at(capture_square)

                # Add the updated board state to the new possible states
                new_possible_states.add(board.fen())

        self.possible_states.update(new_possible_states)

        # Update the internal board state if the move was valid
        # if taken_move is not None and taken_move in self.board.legal_moves:
        #     self.board.push(taken_move)
        # else:
        #     print("Invalid move:", taken_move)

    def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason], game_history: GameHistory):
        try:
            self.engine.quit()
        except chess.engine.EngineTerminatedError:
            pass