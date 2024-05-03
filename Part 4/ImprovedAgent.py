import random
import chess.engine
from reconchess import Player
import os

# Define the path to the Stockfish executable for the automarker
#stockfish_path = '/opt/stockfish/stockfish'

# Define the path to the Stockfish executable
stockfish_path = r'C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish'

class ImprovedBot(Player):
    def __init__(self):
        self.board = None
        self.color = None
        self.my_piece_captured_square = None
        self.states = set()
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)

    def handle_game_start(self, color, board, opponent_name):
        self.board = board
        self.color = color
        self.states.add(board.fen())

    def handle_opponent_move_result(self, captured_my_piece, capture_square):
        self.my_piece_captured_square = capture_square
        new_states = set()
        for state in self.states:
            board = chess.Board(state)
            for move in board.pseudo_legal_moves:
                if captured_my_piece:
                    if chess.square_name(move.to_square) == chess.square_name(capture_square):
                        board.push(move)
                        new_states.add(board.fen())
                        board.pop()
                else:
                    if move.to_square != capture_square:
                        board.push(move)
                        new_states.add(board.fen())
                        board.pop()
        self.states = new_states
    #THIS IS RANDOM SENSING
    # def choose_sense(self, sense_actions, move_actions, seconds_left):
    #     valid_actions = []
    #     for square in sense_actions:
    #         rank, file = chess.square_rank(square), chess.square_file(square)
    #         if 0 < rank < 7 and 0 < file < 7:  # avoid edges
    #             valid_actions.append(square)
    #     return random.choice(valid_actions) if valid_actions else None

    #THIS IS USING:
    # Threat level, 
    # proximity to center squares, 
    # piece mobility, 
    # pawn structure
    def choose_sense(self, sense_actions, move_actions, seconds_left):
        # Calculate the score for each sense action based on various factors
        action_scores = {}
        for square in sense_actions:
            # Calculate neighboring squares
            neighbors = []
            file, rank = chess.square_file(square), chess.square_rank(square)
            for file_offset in (-1, 0, 1):
                for rank_offset in (-1, 0, 1):
                    if file_offset == 0 and rank_offset == 0:
                        continue
                    neighbor_file, neighbor_rank = file + file_offset, rank + rank_offset
                    if 0 <= neighbor_file < 8 and 0 <= neighbor_rank < 8:
                        neighbors.append(chess.square(neighbor_file, neighbor_rank))

            # Score based on threat level
            threat_score = sum(1 for neighbor in neighbors if self.board.is_attacked_by(not self.color, neighbor))

            # Score based on proximity to center squares
            center_distance = min(abs(file - 3.5), abs(rank - 3.5))
            center_score = 1 / (1 + center_distance)  # Higher score for squares closer to the center

            # Score based on piece mobility
            mobility_score = len(self.board.attackers(not self.color, square))  # Higher score for squares with more attackers

            # Score based on pawn structure
            pawn_score = 0
            if self.board.piece_at(square) is not None and self.board.piece_at(square).piece_type == chess.PAWN:
                pawn_score = sum(1 for neighbor in neighbors if self.board.piece_at(neighbor) is not None and
                                self.board.piece_at(neighbor).piece_type == chess.PAWN)

            # Total score for the action
            total_score = threat_score + center_score + mobility_score + pawn_score
            action_scores[square] = total_score

        # Sort sense actions by score in descending order
        sorted_actions = sorted(sense_actions, key=lambda x: action_scores.get(x, 0), reverse=True)

        # Choose the square with the highest score
        return sorted_actions[0] if sorted_actions else None


    def handle_sense_result(self, sense_result):
        new_states = set()
        for state in self.states:
            board = chess.Board(state)
            if self.my_piece_captured_square:
                board.remove_piece_at(self.my_piece_captured_square)
            for square, piece in sense_result:
                board.set_piece_at(square, piece)
            new_states.add(board.fen())
        self.states = new_states

    def choose_move(self, move_actions, seconds_left):
        if not move_actions:
            return None

        # Convert the list of valid moves to algebraic notation
        valid_moves_uci = [move.uci() for move in move_actions]

        # Create a new board position
        board = chess.Board()

        # Set the current board position
        for state in self.states:
            board.set_fen(state)

        # Use the Stockfish engine to select a move
        # Perform iterative deepening search
        best_move_uci = None
        for depth in range(1, 20):  # Adjust the depth as needed
            result = self.engine.play(board, chess.engine.Limit(depth=depth))
            best_move_uci = result.move.uci()
            if best_move_uci in valid_moves_uci:
                break  # Found a valid move within the time limit

        # Check if the move suggested by Stockfish is valid
        if best_move_uci in valid_moves_uci:
            return chess.Move.from_uci(best_move_uci)
        else:
            # If the suggested move is not valid, choose a random valid move
            return random.choice(move_actions)


    def handle_move_result(self, requested_move, taken_move, captured_opponent_piece, capture_square):
        new_states = set()
        for state in self.states:
            board = chess.Board(state)
            if taken_move in board.legal_moves:
                board.push(taken_move)
                new_states.add(board.fen())
        self.states = new_states

    def handle_game_end(self, winner_color, win_reason, game_history):
        self.engine.quit()