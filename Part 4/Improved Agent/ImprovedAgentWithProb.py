
import random
import chess
import chess.engine
import random
import chess.engine
from reconchess import Player, List, Optional, chess
import chess.engine
import random
from reconchess import *
import os

# Define the path to the Stockfish executable
stockfish_path = r'C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish'
# Define the path to the Stockfish executable for the automarker
# stockfish_path = '/opt/stockfish/stockfish'

class MyAgent(Player):
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
        self.possible_states = set()
        self.last_opponent_move = None
        self.my_piece_captured_square = None
        self.board = None

    def handle_game_start(self, color, board, opponent_name):
        self.color = color
        self.board = board
        self.possible_states = {board.fen()}

    def handle_opponent_move_result(self, captured_my_piece, capture_square):
        self.my_piece_captured_square = capture_square if captured_my_piece else None
        updated_states = set()
        for state in self.possible_states:
            board = chess.Board(state)
            for move in board.legal_moves:
                if captured_my_piece == (board.piece_at(move.to_square) is not None):
                    board.push(move)
                    updated_states.add(board.fen())
                    board.pop()
        self.possible_states = updated_states

    def prioritize_sensing_actions(self) -> List[Square]:
        prioritized_sensing_actions = []

        # Prioritize sensing around the opponent's last move
        if self.last_opponent_move:
            last_opponent_move_obj = chess.Move.from_uci(self.last_opponent_move)
            last_opponent_move_to_square = last_opponent_move_obj.to_square
            for square in chess.SQUARES:
                if chess.square_distance(square, last_opponent_move_to_square) <= 2:
                    prioritized_sensing_actions.append(square)

        # Prioritize sensing around our recently captured piece
        if self.my_piece_captured_square:
            prioritized_sensing_actions.append(self.my_piece_captured_square)

        # Prioritize sensing around opponent's last known piece locations
        for square, piece in self.board.piece_map().items():
            if piece.color != self.color:
                for neighbor_square in chess.SQUARES:
                    if chess.square_distance(square, neighbor_square) <= 2:
                        prioritized_sensing_actions.append(neighbor_square)

        # Prioritize sensing around the opponent's king
        opponent_king_square = self.board.king(not self.color)
        if opponent_king_square:
            for neighbor_square in chess.SQUARES:
                if chess.square_distance(neighbor_square, opponent_king_square) <= 2:
                    prioritized_sensing_actions.append(neighbor_square)

        # Prioritize sensing in key strategic areas (e.g., central squares, pawn promotion squares)
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        for square in center_squares:
            if square not in self.board.piece_map():
                prioritized_sensing_actions.append(square)

        return prioritized_sensing_actions

    def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> Optional[Square]:
        # If our piece was just captured, sense where it was captured
        if self.my_piece_captured_square:
            return self.my_piece_captured_square

        # If we might capture a piece when we move, sense where the capture will occur
        future_move = self.choose_move(move_actions, seconds_left)
        if future_move is not None and self.board.piece_at(future_move.to_square) is not None:
            return future_move.to_square

        # Prioritize sensing actions based on strategic considerations
        prioritized_sensing_actions = self.prioritize_sensing_actions()

        # Remove squares with your own pieces from the prioritized sensing actions
        prioritized_sensing_actions = [square for square in prioritized_sensing_actions if self.board.piece_at(square) is None or self.board.piece_at(square).color != self.color]

        # If there are prioritized sensing actions, assign probabilities and choose one based on the probabilities
        if prioritized_sensing_actions:
            # Assign probabilities to each square based on their priority
            probabilities = self.assign_probabilities(prioritized_sensing_actions)

            # Choose a square based on the probabilities
            chosen_square = random.choices(prioritized_sensing_actions, weights=probabilities, k=1)[0]
            return chosen_square

        # Otherwise, randomly choose a sense action, but don't sense on a square where our pieces are located
        for square, piece in self.board.piece_map().items():
            if piece.color == self.color:
                sense_actions.remove(square)
        return random.choice(sense_actions)

    def assign_probabilities(self, squares: List[Square]) -> List[float]:
        # Assign probabilities to each square based on their priority
        probabilities = []
        total_priority = sum(self.calculate_priority(square) for square in squares)

        for square in squares:
            priority = self.calculate_priority(square)
            probability = priority / total_priority
            probabilities.append(probability)

        return probabilities

    def calculate_priority(self, square: Square) -> float:
        # Calculate the priority of a square based on strategic considerations
        priority = 0

        # Assign higher priority to squares near the opponent's last move
        if self.last_opponent_move:
            last_opponent_move_obj = chess.Move.from_uci(self.last_opponent_move)
            last_opponent_move_to_square = last_opponent_move_obj.to_square
            distance = chess.square_distance(square, last_opponent_move_to_square)
            priority += 10 / (distance + 1)

        # Assign higher priority to squares near recently captured pieces
        if self.my_piece_captured_square:
            distance = chess.square_distance(square, self.my_piece_captured_square)
            priority += 8 / (distance + 1)

        # Assign higher priority to squares near the opponent's king
        opponent_king_square = self.board.king(not self.color)
        if opponent_king_square:
            distance = chess.square_distance(square, opponent_king_square)
            priority += 6 / (distance + 1)

        # Assign higher priority to central squares
        if square in [chess.D4, chess.D5, chess.E4, chess.E5]:
            priority += 4

        return priority

    def handle_sense_result(self, sense_result):
        updated_states = set()
        for state in self.possible_states:
            board = chess.Board(state)
            if all(board.piece_at(square) == piece for square, piece in enumerate(sense_result)):
                updated_states.add(state)
        self.possible_states = updated_states

    def choose_move(self, move_actions, seconds_left):
        if len(self.possible_states) > 10000:
            self.possible_states = set(random.sample(self.possible_states, 10000))

        if len(self.possible_states) == 0:
            # If there are no possible states, return a random move
            return random.choice(move_actions)

        time_limit = 10 / len(self.possible_states)
        move_counts = {}
        for state in self.possible_states:
            board = chess.Board(state)
            result = self.engine.play(board, chess.engine.Limit(time=time_limit))
            move = result.move
            move_counts[move] = move_counts.get(move, 0) + 1

        if move_counts:
            best_move = max(move_counts, key=move_counts.get)
        else:
            # If no best move is found, return a random move from the available move actions
            best_move = random.choice(move_actions)
            
        return best_move
    
    def handle_move_result(self, requested_move, taken_move, captured_opponent_piece, capture_square):
        self.last_opponent_move = str(taken_move)
        updated_states = set()
        for state in self.possible_states:
            board = chess.Board(state)
            if board.is_legal(taken_move):
                board.push(taken_move)
                updated_states.add(board.fen())
        self.possible_states = updated_states
        self.board.push(taken_move)

    def handle_game_end(self, winner_color, win_reason, game_history):
        self.engine.quit()