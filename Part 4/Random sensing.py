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
        valid_actions = []
        for square in sense_actions:
            rank, file = chess.square_rank(square), chess.square_file(square)
            if 0 < rank < 7 and 0 < file < 7:  # avoid edges
                valid_actions.append(square)
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
        if len(self.states) > 10000:
            self.states = random.sample(self.states, 10000)
        moves_count = {}
        for state in self.states:
            board = chess.Board(state)
            if board.is_checkmate():
                return None
            if board.is_check():
                for move in move_actions:
                    if move.to_square == board.king(not self.color):
                        return move
            result = self.engine.play(board, chess.engine.Limit(time=10/len(self.states)))
            move = result.move
            if move not in moves_count:
                moves_count[move] = 0
            moves_count[move] += 1
        return max(moves_count, key=moves_count.get)

    def handle_move_result(self, requested_move, taken_move, captured_opponent_piece, capture_square):
        if taken_move:
            new_states = set()
            for state in self.states:
                board = chess.Board(state)
                if taken_move in board.legal_moves:
                    board.push(taken_move)
                    new_states.add(board.fen())
            self.states = new_states

    def handle_game_end(self, winner_color, win_reason, game_history):
        self.engine.quit()
