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


# class ImprovedBot(Player):
#     def __init__(self):
#         self.board = None
#         self.color = None
#         self.my_piece_captured_square = None
#         self.board_stack = []  # Initialize an empty list to store board states

#         # initialize the stockfish engine
#         self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)

#     def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
#         self.board = board
#         self.color = color

#     def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
#         # if the opponent captured our piece, remove it from our board.
#         self.my_piece_captured_square = capture_square
#         if captured_my_piece:
#             self.board.remove_piece_at(capture_square)
#         # Store the opponent's last move
#         self.last_opponent_move = self.board.peek().uci() if self.board.move_stack else None

#         # Call the superclass method to handle the move result
#         super().handle_opponent_move_result(captured_my_piece, capture_square)

#     def prioritize_sensing_actions(self) -> List[Square]:
#         # Prioritize sensing actions based on the current game state and strategic considerations
#         prioritized_sensing_actions = []

#         # Prioritize sensing around the opponent's last move if available
#         if self.last_opponent_move:
#             # Convert the last opponent's move to a move object
#             last_opponent_move_obj = chess.Move.from_uci(self.last_opponent_move)
#             # Get the square the opponent's last piece moved to
#             last_opponent_move_to_square = last_opponent_move_obj.to_square
#             # Add nearby squares to the prioritized sensing actions
#             for square in chess.SQUARES:
#                 if chess.square_distance(square, last_opponent_move_to_square) <= 2:
#                     prioritized_sensing_actions.append(square)

#         # If our piece was recently captured, prioritize sensing around the captured square
#         if self.my_piece_captured_square:
#             prioritized_sensing_actions.append(self.my_piece_captured_square)

#         # Sense around opponent's last known locations
#         for square, piece in self.board.piece_map().items():
#             if piece.color != self.color:
#                 for neighbor_square in chess.SQUARES:
#                     if chess.square_distance(square, neighbor_square) <= 2:
#                         prioritized_sensing_actions.append(neighbor_square)

#         # Sense around opponent's king
#         opponent_king_square = self.board.king(not self.color)
#         if opponent_king_square:
#             for neighbor_square in self.board.attackers(not self.color, opponent_king_square):
#                 prioritized_sensing_actions.append(neighbor_square)

#         # Sense in key areas (e.g., central squares, pawn promotion squares)
#         center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
#         for square in center_squares:
#             if square not in self.board.piece_map():  # If unseen
#                 prioritized_sensing_actions.append(square)

#         # Add additional prioritized sensing actions based on strategic considerations
#         # For example, sense around potential pawn promotion squares, etc.

#         return prioritized_sensing_actions

#     # HOW MY BOT HANDLES SENSING
#     def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> Optional[Square]:
#         # If our piece was just captured, sense where it was captured
#         if self.my_piece_captured_square:
#             return self.my_piece_captured_square

#         # If we might capture a piece when we move, sense where the capture will occur
#         future_move = self.choose_move(move_actions, seconds_left)
#         if future_move is not None and self.board.piece_at(future_move.to_square) is not None:
#             return future_move.to_square

#         # Prioritize sensing actions based on strategic considerations
#         prioritized_sensing_actions = self.prioritize_sensing_actions()

#         # If there are prioritized sensing actions, choose one of them
#         if prioritized_sensing_actions:
#             # Remove prioritized sensing actions that are not in the sense actions list
#             prioritized_sensing_actions = [square for square in prioritized_sensing_actions if square in sense_actions]
#             if prioritized_sensing_actions:
#                 return random.choice(prioritized_sensing_actions)

#         # otherwise, just randomly choose a sense action, but don't sense on a square where our pieces are located
#         for square, piece in self.board.piece_map().items():
#             if piece.color == self.color:
#                 sense_actions.remove(square)
#         return random.choice(sense_actions)

#     def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
#         # add the pieces in the sense result to our board
#         for square, piece in sense_result:
#             self.board.set_piece_at(square, piece)

#     def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:

#         # if we might be able to take the king, try to
#         enemy_king_square = self.board.king(not self.color)
#         if enemy_king_square:
#             # if there are any ally pieces that can take king, execute one of those moves
#             enemy_king_attackers = self.board.attackers(self.color, enemy_king_square)
#             if enemy_king_attackers:
#                 attacker_square = enemy_king_attackers.pop()
#                 return chess.Move(attacker_square, enemy_king_square)

#         # otherwise, try to move with the stockfish chess engine
#         try:
#             self.board.turn = self.color
#             self.board.clear_stack()
#             result = self.engine.play(self.board, chess.engine.Limit(time=1))
#             return result.move
#         except chess.engine.EngineTerminatedError:
#             print('Stockfish Engine died')
#         except chess.engine.EngineError:
#             print('Stockfish Engine bad state at "{}"'.format(self.board.fen()))

#         # if all else fails, pass
#         return None

#     def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
#                            captured_opponent_piece: bool, capture_square: Optional[Square]):
#         # if a move was executed, apply it to our board
#         if taken_move is not None:
#             self.board.push(taken_move)

#     def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason],
#                         game_history: GameHistory):
#         try:
#             # if the engine is already terminated then this call will throw an exception
#             self.engine.quit()
#         except chess.engine.EngineTerminatedError:
#             pass


# import random
# import chess.engine
# from reconchess import Player, List, Optional, chess
# from reconchess import *

# # Define the path to the Stockfish executable
# stockfish_path = r'C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish'
# # Define the path to the Stockfish executable for the automarker
# # stockfish_path = '/opt/stockfish/stockfish'

# class MyAgent(Player):
#     def __init__(self):
#         self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
#         self.possible_states = set()
#         self.last_opponent_move = None
#         self.my_piece_captured_square = None
#         self.board = None

#     def handle_game_start(self, color, board, opponent_name):
#         self.color = color
#         self.board = board
#         self.possible_states = {board.fen()}

#     def handle_opponent_move_result(self, captured_my_piece, capture_square):
#         self.my_piece_captured_square = capture_square if captured_my_piece else None
#         updated_states = set()
#         for state in self.possible_states:
#             board = chess.Board(state)
#             for move in board.legal_moves:
#                 if captured_my_piece == (board.piece_at(move.to_square) is not None):
#                     board.push(move)
#                     updated_states.add(board.fen())
#                     board.pop()
#         self.possible_states = updated_states

#     def prioritize_sensing_actions(self) -> List[Square]:
#         # Prioritize sensing actions based on the current game state and strategic considerations
#         prioritized_sensing_actions = []

#         # Prioritize sensing around the opponent's last move if available
#         if self.last_opponent_move:
#             # Convert the last opponent's move to a move object
#             last_opponent_move_obj = chess.Move.from_uci(self.last_opponent_move)
#             # Get the square the opponent's last piece moved to
#             last_opponent_move_to_square = last_opponent_move_obj.to_square
#             # Add nearby squares to the prioritized sensing actions
#             for square in chess.SQUARES:
#                 if chess.square_distance(square, last_opponent_move_to_square) <= 2:
#                     prioritized_sensing_actions.append(square)

#         # If our piece was recently captured, prioritize sensing around the captured square
#         if self.my_piece_captured_square:
#             prioritized_sensing_actions.append(self.my_piece_captured_square)

#         # Sense around opponent's last known locations
#         for square, piece in self.board.piece_map().items():
#             if piece.color != self.color:
#                 for neighbor_square in chess.SQUARES:
#                     if chess.square_distance(square, neighbor_square) <= 2:
#                         prioritized_sensing_actions.append(neighbor_square)

#         # Sense around opponent's king
#         opponent_king_square = self.board.king(not self.color)
#         if opponent_king_square:
#             for neighbor_square in self.board.attackers(not self.color, opponent_king_square):
#                 prioritized_sensing_actions.append(neighbor_square)

#         # Sense in key areas (e.g., central squares, pawn promotion squares)
#         center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
#         for square in center_squares:
#             if square not in self.board.piece_map():  # If unseen
#                 prioritized_sensing_actions.append(square)

#         # Add additional prioritized sensing actions based on strategic considerations
#         # For example, sense around potential pawn promotion squares, etc.

#         return prioritized_sensing_actions

#     def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> Optional[Square]:
#         # If our piece was just captured, sense where it was captured
#         if self.my_piece_captured_square:
#             return self.my_piece_captured_square

#         # If we might capture a piece when we move, sense where the capture will occur
#         future_move = self.choose_move(move_actions, seconds_left)
#         if future_move is not None and self.board.piece_at(future_move.to_square) is not None:
#             return future_move.to_square

#         # Prioritize sensing actions based on strategic considerations
#         prioritized_sensing_actions = self.prioritize_sensing_actions()

#         # If there are prioritized sensing actions, choose one of them
#         if prioritized_sensing_actions:
#             # Remove prioritized sensing actions that are not in the sense actions list
#             prioritized_sensing_actions = [square for square in prioritized_sensing_actions if square in sense_actions]
#             if prioritized_sensing_actions:
#                 return random.choice(prioritized_sensing_actions)

#         # otherwise, just randomly choose a sense action, but don't sense on a square where our pieces are located
#         for square, piece in self.board.piece_map().items():
#             if piece.color == self.color:
#                 sense_actions.remove(square)
#         return random.choice(sense_actions)

#     def handle_sense_result(self, sense_result):
#         updated_states = set()
#         for state in self.possible_states:
#             board = chess.Board(state)
#             if all(board.piece_at(square) == piece for square, piece in enumerate(sense_result)):
#                 updated_states.add(state)
#         self.possible_states = updated_states

#     def choose_move(self, move_actions, seconds_left):
#         if len(self.possible_states) > 10000:
#             self.possible_states = set(random.sample(self.possible_states, 10000))

#         if len(self.possible_states) == 0:
#             # If there are no possible states, return a random move
#             return random.choice(move_actions)

#         time_limit = 10 / len(self.possible_states)
#         move_counts = {}
#         for state in self.possible_states:
#             board = chess.Board(state)
#             result = self.engine.play(board, chess.engine.Limit(time=time_limit))
#             move = result.move
#             if move is not None:
#                 move_counts[move] = move_counts.get(move, 0) + 1

#         if move_counts:
#             best_move = max(move_counts, key=move_counts.get)
#         else:
#             # If no best move is found, return a random move from the available move actions
#             best_move = random.choice(move_actions)

#         return best_move

#     def handle_move_result(self, requested_move, taken_move, captured_opponent_piece, capture_square):
#         updated_states = set()
#         for state in self.possible_states:
#             board = chess.Board(state)
#             if board.is_legal(taken_move):
#                 board.push(taken_move)
#                 updated_states.add(board.fen())
#         self.possible_states = updated_states

#     def handle_game_end(self, winner_color, win_reason, game_history):
#         self.engine.quit()


# class MyAgent(Player):
#     def __init__(self):
#         self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
#         self.possible_states = set()
#         self.my_piece_captured_square = None
#         self.last_move_opponent = None
#         self.board = chess.Board()

#     def handle_game_start(self, color, board, opponent_name):
#         self.color = color
#         self.possible_states = {board.fen()}
#         self.board = board

#     def handle_opponent_move_result(self, captured_my_piece, capture_square):
#         self.my_piece_captured_square = capture_square if captured_my_piece else None
#         updated_states = set()
#         for state in self.possible_states:
#             board = chess.Board(state)
#             for move in board.legal_moves:
#                 if captured_my_piece == (board.piece_at(move.to_square) is not None):
#                     board.push(move)
#                     updated_states.add(board.fen())
#                     board.pop()
#         self.possible_states = updated_states

#     def choose_sense(self, sense_actions, move_actions, seconds_left):
#         # If our piece was just captured, sense where it was captured
#         if self.my_piece_captured_square:
#             return self.my_piece_captured_square

#         # If we might capture a piece when we move, sense where the capture will occur
#         future_move = self.choose_move(move_actions, seconds_left)
#         if future_move is not None and self.board.piece_at(future_move.to_square) is not None:
#             return future_move.to_square

#         # Prioritize sensing actions based on strategic considerations
#         prioritized_sensing_actions = self.prioritize_sensing_actions()

#         # Remove squares with your own pieces from the prioritized sensing actions
#         prioritized_sensing_actions = [square for square in prioritized_sensing_actions if self.board.piece_at(square) is None or self.board.piece_at(square).color != self.color]

#         # If there are prioritized sensing actions, choose one of them
#         if prioritized_sensing_actions:
#             return random.choice(prioritized_sensing_actions)

#         # Otherwise, randomly choose a sense action that doesn't sense our own pieces
#         valid_squares = [square for square in sense_actions if self.board.piece_at(square) is None or self.board.piece_at(square).color != self.color]
#         return random.choice(valid_squares) if valid_squares else None

#     def prioritize_sensing_actions(self):
#         prioritized_squares = []

#         # Prioritize squares near the opponent's last move
#         if self.last_move_opponent is not None:
#             last_move_squares = [self.last_move_opponent.from_square, self.last_move_opponent.to_square]
#             prioritized_squares.extend(last_move_squares)

#         # Prioritize squares near our recently captured piece
#         if self.my_piece_captured_square is not None:
#             prioritized_squares.append(self.my_piece_captured_square)

#         # Prioritize squares with unknown pieces
#         unknown_squares = [square for square in chess.SQUARES if self.board.piece_at(square) is None]
#         prioritized_squares.extend(unknown_squares)

#         # Prioritize squares near the opponent's king
#         opponent_king_square = self.board.king(not self.color)
#         if opponent_king_square is not None:
#             prioritized_squares.append(opponent_king_square)
#             prioritized_squares.extend(self.board.attacks(opponent_king_square))

#         return prioritized_squares

#     def handle_sense_result(self, sense_result):
#         updated_states = set()
#         for state in self.possible_states:
#             board = chess.Board(state)
#             if all(board.piece_at(square) == piece for square, piece in enumerate(sense_result)):
#                 updated_states.add(state)
#         self.possible_states = updated_states


#     def choose_move(self, move_actions, seconds_left):
#         if len(self.possible_states) > 10000:
#             self.possible_states = set(random.sample(self.possible_states, 10000))

#         if len(self.possible_states) == 0:
#             # If there are no possible states, return a random move from move_actions
#             return random.choice(move_actions)

#         time_limit = 10 / len(self.possible_states)
#         move_scores = {}

#         for state in self.possible_states:
#             board = chess.Board(state)

#             # Generate pseudo-legal moves
#             pseudo_legal_moves = list(board.generate_pseudo_legal_moves())

#             # Generate castling moves manually
#             castling_moves = []
#             if board.has_kingside_castling_rights(self.color):
#                 if self.color == chess.WHITE:
#                     if board.piece_at(chess.F1) is None and board.piece_at(chess.G1) is None:
#                         castling_moves.append(chess.Move.from_uci("e1g1"))
#                 else:
#                     if board.piece_at(chess.F8) is None and board.piece_at(chess.G8) is None:
#                         castling_moves.append(chess.Move.from_uci("e8g8"))
#             if board.has_queenside_castling_rights(self.color):
#                 if self.color == chess.WHITE:
#                     if board.piece_at(chess.D1) is None and board.piece_at(chess.C1) is None and board.piece_at(chess.B1) is None:
#                         castling_moves.append(chess.Move.from_uci("e1c1"))
#                 else:
#                     if board.piece_at(chess.D8) is None and board.piece_at(chess.C8) is None and board.piece_at(chess.B8) is None:
#                         castling_moves.append(chess.Move.from_uci("e8c8"))

#             # Combine pseudo-legal moves and castling moves
#             all_moves = pseudo_legal_moves + castling_moves

#             # Filter out moves that are not in move_actions
#             valid_moves = [move for move in all_moves if move in move_actions]

#             for move in valid_moves:
#                 result = self.engine.analyse(board, chess.engine.Limit(time=time_limit), root_moves=[move])
#                 score = result["score"].relative.score()
#                 move_scores[move] = move_scores.get(move, 0) + score

#         if move_scores:
#             best_move = max(move_scores, key=move_scores.get)
#         else:
#             self.board.turn = self.color
#             self.board.clear_stack()
#             best_move = self.engine.play(self.board, chess.engine.Limit(time=0.5))

#         return best_move
#     # def choose_move(self, move_actions, seconds_left):
#     #     if len(self.possible_states) > 10000:
#     #         self.possible_states = set(random.sample(self.possible_states, 10000))

#     #     if len(self.possible_states) == 0:
#     #         # If there are no possible states, return a random move
#     #         return random.choice(move_actions)

#     #     time_limit = 10 / len(self.possible_states)
#     #     move_counts = {}
#     #     for state in self.possible_states:
#     #         board = chess.Board(state)
#     #         result = self.engine.play(board, chess.engine.Limit(time=time_limit))
#     #         move = result.move
#     #         move_counts[move] = move_counts.get(move, 0) + 1

#     #     best_move = max(move_counts, key=move_counts.get)
#     #     return best_move

#     def handle_move_result(self, requested_move, taken_move, captured_opponent_piece, capture_square):
#         # Update the board with the taken move
#         if taken_move is not None:
#             self.board.push(taken_move)
#             self.last_move_opponent = taken_move

#         updated_states = set()
#         for state in self.possible_states:
#             board = chess.Board(state)
#             if taken_move is not None and board.is_legal(taken_move):
#                 board.push(taken_move)
#                 updated_states.add(board.fen())
#         self.possible_states = updated_states

#     def handle_game_end(self, winner_color, win_reason, game_history):
#         self.engine.quit()


# import chess.engine
# import random
# from reconchess import *

# class ImprovedAgent(Player):
#     def __init__(self):
#         self.board = None
#         self.color = None
#         self.my_piece_captured_square = None
#         self.set_board_states = set()
#         self.move_history = []

#     def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
#         self.board = board
#         self.color = color
#         self.set_board_states = {board.fen()}
#         self.move_history = []

#     def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
#         self.my_piece_captured_square = capture_square
#         if captured_my_piece:
#             self.set_board_states = {fen for fen in self.set_board_states if self.my_piece_captured_square in chess.Board(fen).attacks(self.my_piece_captured_square)}
#         else:
#             self.set_board_states = {fen for fen in self.set_board_states if not chess.Board(fen).move_stack or not chess.Board(fen).is_capture(chess.Board(fen).peek())}

#     def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> Square:
#         # If our piece was just captured, sense where it was captured
#         if self.my_piece_captured_square:
#             return self.my_piece_captured_square

#         # If we might capture a piece when we move, sense where the capture will occur
#         future_move = self.choose_move(move_actions, seconds_left)
#         if future_move is not None and self.board.piece_at(future_move.to_square) is not None:
#             return future_move.to_square

#         # Prioritize sensing actions based on strategic considerations
#         prioritized_sensing_actions = self.prioritize_sensing_actions()

#         # If there are prioritized sensing actions, choose one of them
#         # if prioritized_sensing_actions:
#         #     # Remove prioritized sensing actions that are not in the sense actions list
#         #     prioritized_sensing_actions = [square for square in prioritized_sensing_actions if square in sense_actions]
#         #     if prioritized_sensing_actions:
#         #         return prioritized_sensing_actions[0]  # Choose the first prioritized sensing action

#         # If no specific strategy applies, choose a sensing action that is not on a square where our pieces are located
#         valid_sensing_actions = [square for square in sense_actions if self.board.piece_at(square) is None or self.board.piece_at(square).color != self.color]
#         if valid_sensing_actions:
#             return random.choice(valid_sensing_actions)
#         else:
#             return sense_actions[0]  # If no valid sensing actions available, choose the first one

#     def prioritize_sensing_actions(self) -> List[Square]:
#         prioritized_actions = []
#         # Prioritize sensing the opponent's king position (highest priority)
#         opponent_king_square = self.get_opponent_king_square()
#         if opponent_king_square:
#             prioritized_actions.append(opponent_king_square)

#         # Prioritize sensing squares from which an attack on the opponent's king is possible
#         if opponent_king_square:
#             for square in chess.SQUARES:
#                 if self.board.piece_at(square) and self.board.piece_at(square).color != self.color:
#                     if opponent_king_square in self.board.attacks(square):
#                         prioritized_actions.append(square)

#         # Prioritize sensing squares near the opponent's king
#         if opponent_king_square:
#             for square in chess.SQUARES:
#                 if chess.square_distance(square, opponent_king_square) <= 2:
#                     prioritized_actions.append(square)

#         # Prioritize sensing squares where the opponent's pieces are located
#         for square, piece in self.board.piece_map().items():
#             if piece.color != self.color:
#                 prioritized_actions.append(square)

#         # Prioritize sensing squares near the center of the board
#         center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
#         for square in center_squares:
#             prioritized_actions.append(square)

#         return prioritized_actions

#     def get_opponent_king_square(self) -> Optional[Square]:
#         for fen in self.set_board_states:
#             board = chess.Board(fen)
#             king_square = board.king(not self.color)
#             if king_square:
#                 return king_square
#         return None

#     def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
#         self.set_board_states = {fen for fen in self.set_board_states if all(chess.Board(fen).piece_at(square) == piece for square, piece in sense_result)}

#     def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
#         engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
#         if len(self.set_board_states) > 10000:
#             self.set_board_states = random.sample(self.set_board_states, 10000)
#         if self.set_board_states:
#             time_limit = 10/len(self.set_board_states)
#         else:
#             time_limit = 0.1
#         possible_moves = []
#         for fen in self.set_board_states:
#             board = chess.Board(fen)
#             if board.is_checkmate():
#                 possible_moves.append(board.king(not self.color))
#             else:
#                 # Refine move selection by considering additional factors
#                 move = self.select_move(board, move_actions, time_limit)
#                 if move in move_actions:
#                     possible_moves.append(move)
#         engine.quit()
#         if possible_moves:
#             move = max(set(possible_moves), key=possible_moves.count)
#             if move in move_actions:
#                 return move
#         return random.choice(move_actions)

#     def select_move(self, board: chess.Board, move_actions: List[chess.Move], time_limit: float) -> Optional[chess.Move]:
#         engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
#         move = engine.play(board, chess.engine.Limit(time=time_limit)).move
#         engine.quit()
#         # Prioritize moves that capture the opponent's king
#         for move in move_actions:
#             if board.piece_at(move.to_square) and board.piece_at(move.to_square).piece_type == chess.KING:
#                 return move
#         # Utilize additional chess heuristics and domain knowledge
#         if move in move_actions:
#             # Prioritize moves that improve piece mobility and control the center
#             if board.is_capture(move) or board.gives_check(move) or move.to_square in chess.SquareSet(chess.BB_CENTER):
#                 return move

#         return move

#     def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
#                            captured_opponent_piece: bool, capture_square: Optional[Square]):
#         if taken_move is not None:
#             self.set_board_states = {fen for fen in self.set_board_states if chess.Board(fen).piece_at(taken_move.to_square) == self.board.piece_at(taken_move.to_square)}
#             self.move_history.append(taken_move)
#         else:
#             self.set_board_states = {fen for fen in self.set_board_states if chess.Board(fen).piece_at(requested_move.to_square) == self.board.piece_at(requested_move.to_square)}
#             self.move_history.append(requested_move)

#     def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason], game_history: GameHistory):
#         pass


stockfish_path = (
    r"C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish"
)


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
