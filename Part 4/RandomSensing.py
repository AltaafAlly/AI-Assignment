import random
import chess.engine
from reconchess import Player

# Define the path to the Stockfish executable
stockfish_path = r'C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish'
# Define the path to the Stockfish executable for the automarker
#stockfish_path = '/opt/stockfish/stockfish'

class BaselineBot(Player):
    def __init__(self):
        self.board = None
        self.color = None
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
        self.states = set()

    def handle_game_start(self, color, board, opponent_name):
        self.color = color
        self.board = board
        self.states.add(board.fen())

    def handle_opponent_move_result(self, captured_my_piece, capture_square):
        if captured_my_piece:
            new_states = set()
            for state in self.states:
                board = chess.Board(state)
                for move in board.legal_moves:
                    if move.to_square != capture_square:
                        board.push(move)
                        new_states.add(board.fen())
            self.states = new_states

    def choose_sense(self, sense_actions, move_actions, seconds_left):
        # Filter out squares on the edges of the board
        valid_actions = [square for square in sense_actions
                        if 1 < chess.square_rank(square) < 7
                        and 1 < chess.square_file(square) < 7]
        
        # Select a square uniformly at random from the valid actions
        return random.choice(valid_actions) if valid_actions else None


    def handle_sense_result(self, sense_result):
        new_states = set()
        for state in self.states:
            board = chess.Board(state)
            for square, piece in sense_result:
                board.set_piece_at(square, piece)
            new_states.add(board.fen())
        self.states = new_states

    def choose_move(self, move_actions, seconds_left):
        # Ensure there are valid move actions
        if not move_actions:
            return None

        # Calculate the time limit for Stockfish based on the number of boards
        num_boards = len(self.states)
        time_limit = 10 / max(1, num_boards)

        # Cap the number of boards at 10,000 if it exceeds
        if num_boards > 10000:
            self.states = random.sample(self.states, 10000)
            num_boards = 10000

        # Perform majority voting to select the move
        moves_count = {}
        for state in self.states:
            board = chess.Board(state)
            if board.is_checkmate():
                return None
            if board.is_check():
                for move in move_actions:
                    if move.to_square == board.king(not self.color):
                        return move
            result = self.engine.play(board, chess.engine.Limit(time=time_limit))
            move = result.move
            if move in move_actions:  # Ensure the move is valid
                if move not in moves_count:
                    moves_count[move] = 0
                moves_count[move] += 1

        # Choose the move with the highest count
        if moves_count:
            return max(moves_count, key=moves_count.get)
        else:
            return None


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
