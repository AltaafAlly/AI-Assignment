import random
import chess.engine
from reconchess import Player

# Define the path to the Stockfish executable for the automarker
#stockfish_path = '/opt/stockfish/stockfish'

# Define the path to the Stockfish executable
stockfish_path = r'C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish'

class MyAgent(Player):
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
            if self.my_piece_captured_square:
                board.remove_piece_at(self.my_piece_captured_square)
            for square, piece in sense_result:
                board.set_piece_at(square, piece)
            new_states.add(board.fen())
        self.states = new_states

    # def choose_move(self, move_actions, seconds_left):
    #     if len(self.states) > 10000:
    #         self.states = random.sample(self.states, 10000)
    #     moves = {}
    #     for state in self.states:
    #         board = chess.Board(state)
    #         if board.is_check():
    #             for move in move_actions:
    #                 if move.to_square == board.king(not self.color):
    #                     return move
    #         self.engine.position(board)
    #         move = self.engine.play(chess.engine.Limit(time=10/len(self.states)), game=object()).move
    #         if move in move_actions:
    #             if move not in moves:
    #                 moves[move] = 0
    #             moves[move] += 1
    #     if moves:
    #         return max(moves, key=lambda x: (moves[x], x.uci()))
    #     else:
    #         return random.choice(move_actions)
    # def choose_move(self, move_actions, seconds_left):
    #     # Ensure there are moves available
    #     if not move_actions:
    #         return None

    #     # Convert the list of valid moves to algebraic notation
    #     valid_moves_uci = [move.uci() for move in move_actions]

    #     # Create a new board position
    #     board = chess.Board()

    #     # Set the current board position
    #     for state in self.states:
    #         board.set_fen(state)

    #     # Use the Stockfish engine to select a move
    #     result = self.engine.play(board, chess.engine.Limit(time=1))
    #     best_move_uci = result.move.uci()

    #     # Check if the move suggested by Stockfish is valid
    #     if best_move_uci in valid_moves_uci:
    #         return chess.Move.from_uci(best_move_uci)
    #     else:
    #         # If the suggested move is not valid, choose a random valid move
    #         return random.choice(move_actions)
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