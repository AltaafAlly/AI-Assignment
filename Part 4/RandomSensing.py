# # import random
# # import chess.engine
# # from reconchess import Player

# # Define the path to the Stockfish executable
# from reconchess import *
# import random
# import chess.engine
# stockfish_path = r'C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish'
# # Define the path to the Stockfish executable for the automarker
# # stockfish_path = '/opt/stockfish/stockfish'


# # #THIS IS MY WRONG BASELINE BOT
# # # class BaselineBot(Player):
# # #     def __init__(self):
# # #         self.board = None
# # #         self.color = None
# # #         self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
# # #         self.states = set()

# # #     def handle_game_start(self, color, board, opponent_name):
# # #         self.color = color
# # #         self.board = board
# # #         self.states.add(board.fen())

# # #     def handle_opponent_move_result(self, captured_my_piece, capture_square):
# # #         if captured_my_piece:
# # #             new_states = set()
# # #             for state in self.states:
# # #                 board = chess.Board(state)
# # #                 for move in board.legal_moves:
# # #                     if move.to_square != capture_square:
# # #                         board.push(move)
# # #                         new_states.add(board.fen())
# # #             self.states = new_states

# # #     def choose_sense(self, sense_actions, move_actions, seconds_left):
# # #         # Filter out squares on the edges of the board
# # #         valid_actions = [square for square in sense_actions
# # #                         if 1 < chess.square_rank(square) < 7
# # #                         and 1 < chess.square_file(square) < 7]

# # #         # Select a square uniformly at random from the valid actions
# # #         return random.choice(valid_actions) if valid_actions else None


# # #     def handle_sense_result(self, sense_result):
# # #         new_states = set()
# # #         for state in self.states:
# # #             board = chess.Board(state)
# # #             for square, piece in sense_result:
# # #                 board.set_piece_at(square, piece)
# # #             new_states.add(board.fen())
# # #         self.states = new_states

# # #     def choose_move(self, move_actions, seconds_left):
# # #         return random.choice(move_actions + [None])


# # #     def handle_move_result(self, requested_move, taken_move, captured_opponent_piece, capture_square):
# # #         new_states = set()
# # #         for state in self.states:
# # #             board = chess.Board(state)
# # #             if taken_move in board.legal_moves:
# # #                 board.push(taken_move)
# # #                 new_states.add(board.fen())
# # #         self.states = new_states


# # #     def handle_game_end(self, winner_color, win_reason, game_history):
# # #         self.engine.quit()

# # import random
# # import chess
# # import chess.engine

# # class MyAgent(Player):
# #     def __init__(self):
# #         self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
# #         self.possible_states = set()

# #     def handle_game_start(self, color, board, opponent_name):
# #         self.color = color
# #         self.possible_states = {board.fen()}

# #     def handle_opponent_move_result(self, captured_my_piece, capture_square):
# #         updated_states = set()
# #         for state in self.possible_states:
# #             board = chess.Board(state)
# #             for move in board.legal_moves:
# #                 if captured_my_piece == (board.piece_at(move.to_square) is not None):
# #                     board.push(move)
# #                     updated_states.add(board.fen())
# #                     board.pop()
# #         self.possible_states = updated_states

# #     def choose_sense(self, sense_actions, move_actions, seconds_left):
# #         valid_squares = [square for square in chess.SQUARES if square not in chess.SquareSet(chess.BB_RANK_1 | chess.BB_RANK_8 | chess.BB_FILE_A | chess.BB_FILE_H)]
# #         return random.choice(valid_squares)

# #     def handle_sense_result(self, sense_result):
# #         updated_states = set()
# #         for state in self.possible_states:
# #             board = chess.Board(state)
# #             if all(board.piece_at(square) == piece for square, piece in enumerate(sense_result)):
# #                 updated_states.add(state)
# #         self.possible_states = updated_states

# #     def choose_move(self, move_actions, seconds_left):
# #         if len(self.possible_states) > 10000:
# #             self.possible_states = set(random.sample(self.possible_states, 10000))

# #         if len(self.possible_states) == 0:
# #             # If there are no possible states, return a random move
# #             return random.choice(move_actions)

# #         time_limit = 10 / len(self.possible_states)
# #         move_counts = {}
# #         for state in self.possible_states:
# #             board = chess.Board(state)
# #             result = self.engine.play(board, chess.engine.Limit(time=time_limit))
# #             move = result.move
# #             move_counts[move] = move_counts.get(move, 0) + 1

# #         best_move = max(move_counts, key=move_counts.get)
# #         return best_move

# #     def handle_move_result(self, requested_move, taken_move, captured_opponent_piece, capture_square):
# #         updated_states = set()
# #         for state in self.possible_states:
# #             board = chess.Board(state)
# #             if board.is_legal(taken_move):
# #                 board.push(taken_move)
# #                 updated_states.add(board.fen())
# #         self.possible_states = updated_states

# #     def handle_game_end(self, winner_color, win_reason, game_history):
# #         self.engine.quit()


# class MyAgent(Player):
#     def __init__(self):
#         self.board = None
#         self.color = None
#         self.my_piece_captured_square = None
#         self.set_board_states = set()

#     def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
#         self.board = board
#         self.color = color
#         self.set_board_states = {board.fen()}

#     def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
#         self.my_piece_captured_square = capture_square
#         if captured_my_piece:
#             self.set_board_states = {fen for fen in self.set_board_states if self.my_piece_captured_square in chess.Board(fen).attacks(self.my_piece_captured_square)}
#         else:
#             self.set_board_states = {fen for fen in self.set_board_states if not chess.Board(fen).move_stack or not chess.Board(fen).is_capture(chess.Board(fen).peek())}

#     def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> Square:
#         return random.choice([square for square in sense_actions if square not in [1, 2, 3, 4, 5, 6, 7, 8, 57, 58, 59, 60, 61, 62, 63, 64]])

#     def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
#         self.set_board_states = {fen for fen in self.set_board_states if all(
#             chess.Board(fen).piece_at(square) == piece for square, piece in sense_result)}

#     # def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:

#     #     engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
        
#     #     if len(self.set_board_states) > 10000:
#     #         self.set_board_states = random.sample(self.set_board_states, 10000)
#     #     if self.set_board_states:
#     #         time_limit = 10/len(self.set_board_states)
#     #     else:
#     #         time_limit = 0.1 

#     #     possible_moves = []

#     #     for fen in self.set_board_states:
#     #         board = chess.Board(fen)
#     #         if board.is_check():
#     #             possible_moves.append(board.king(not self.color))
#     #         else:
#     #             move = engine.play(board, chess.engine.Limit(time=time_limit)).move
#     #             if move in move_actions:
#     #                 possible_moves.append(move)

#     #     engine.quit()

#     #     if possible_moves:
#     #         move = max(set(possible_moves), key=possible_moves.count)
#     #         if move in move_actions:
#     #             return move
#     #     #If no move fall back to random move
#     #     return random.choice(move_actions)
#     def choose_move(
#         self, move_actions: List[chess.Move], seconds_left: float
#     ) -> Optional[chess.Move]:
#         engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
#         # Check if the king is under attack
#         king_square = self.board.king(self.color)
#         if king_square is not None:
#             attackers = self.board.attackers(not self.color, king_square)
#             if attackers:
#                 # Check if the king can capture the attacker
#                 for attacker_square in attackers:
#                     capturing_move = chess.Move(king_square, attacker_square)
#                     if capturing_move in move_actions:
#                         return capturing_move

#         # Check if the opponent's king can be captured
#         enemy_king_square = self.board.king(not self.color)
#         if enemy_king_square:
#             enemy_king_attackers = self.board.attackers(
#                 self.color, enemy_king_square)
#             if enemy_king_attackers:
#                 attacker_square = enemy_king_attackers.pop()
#                 capturing_move = chess.Move(attacker_square, enemy_king_square)
#                 if capturing_move in move_actions:
#                     return capturing_move

#         # Use majority voting to select a move
#         move_counts = {}
#         num_boards = len(self.set_board_states)
#         if num_boards > 0:
#             time_limit = min(10 / num_boards, 0.5)
#             possible_states_list = list(self.set_board_states)  # Convert set to list
#             for fen in random.sample(possible_states_list, min(num_boards, 10000)):
#                 board = chess.Board(fen)
#                 if board.is_check():
#                     possible_moves = [board.king(not self.color)]
#                 else:
#                     move = engine.play(board, chess.engine.Limit(time=time_limit)).move
#                     if move in move_actions:
#                         possible_moves = [move]
#                 for move in possible_moves:
#                     move_counts[move] = move_counts.get(move, 0) + 1


#         if move_counts:
#             best_move = max(move_counts, key=move_counts.get)
#             return best_move

#         # If no valid move is found, return a random move from the available move_actions
#         if move_actions:
#             return random.choice(move_actions)
#         else:
#             return None


#     def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
#                            captured_opponent_piece: bool, capture_square: Optional[Square]):
#         if taken_move is not None:
#             self.set_board_states = {fen for fen in self.set_board_states if chess.Board(
#                 fen).piece_at(taken_move.to_square) == self.board.piece_at(taken_move.to_square)}
#         else:
#             self.set_board_states = {fen for fen in self.set_board_states if chess.Board(
#                 fen).piece_at(requested_move.to_square) == self.board.piece_at(requested_move.to_square)}

#     def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason], game_history: GameHistory):
#         pass

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
        self,
        sense_actions: List[Square],
        move_actions: List[chess.Move],
        seconds_left: float,
    ) -> Optional[Square]:
        # If no specific sensing strategy applies, choose a random sense action
        return random.choice(sense_actions)

    def choose_move(
        self, move_actions: List[chess.Move], seconds_left: float
    ) -> Optional[chess.Move]:
        # Check if there are any possible moves
        if not move_actions:
            return None

        move_counts = {}
        num_boards = len(self.possible_states)
        time_limit = 10 / num_boards

        # Set the maximum time for move selection
        # max_time = 0.5  # Maximum time allowed in seconds

        # start_time = time.time()

        # Iterate through possible states and select moves
        possible_states_list = list(self.possible_states)
        for state in random.sample(possible_states_list, min(num_boards, 10000)):
            board = chess.Board(state)
            board.turn = self.color
            board.clear_stack()
            valid_moves = [move for move in move_actions if board.is_legal(move)]

            # Check if time limit exceeded
            # if time.time() - start_time > max_time:
            #     # Return a random move
            #     print("Time limit exceeded random moved played")
            #     return random.choice(move_actions)

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
        else:
            # If no valid move is found, return a random move
            return random.choice(move_actions)


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
