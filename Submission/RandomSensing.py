import random
from reconchess import *
import os
import chess.engine
import datetime
import asyncio

class RandomSensing(Player):
	def __init__(self):
		self.color = None
		self.move_no = 0
		self.possible_boards = {}
		self.sense_results = []
		self.checkpoints = []
		self.move_recovery = 0
		self.stockfish_path = '/opt/stockfish/stockfish'
		#self.stockfish_path = r'D:\\Wits\\Honours\\AI\\AI-Assignment\\Part 3\\stockfish\\stockfish.exe'
		if not os.path.exists(self.stockfish_path):
			raise ValueError('No stockfish executable found at "{}"'.format(self.stockfish_path))

		# initialize the stockfish engine
		self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path, timeout=None)

	def boards_not_taken(self, brds):
		newBoards = {}
		for fen, board in brds.items():
			if board.turn == self.color:
				board.turn = not self.color

			self.handle_castling_moves(board, newBoards)
			self.handle_non_capture_moves(board, newBoards)

			newBoards[fen] = board

		return newBoards

	def handle_castling_moves(self, board, newBoards):
		for castling_side in [chess.WHITE, chess.BLACK]:
			if board.has_kingside_castling_rights(castling_side):
				self.add_castling_move(board, castling_side, "K", newBoards)
			if board.has_queenside_castling_rights(castling_side):
				self.add_castling_move(board, castling_side, "Q", newBoards)

	def add_castling_move(self, board, castling_side, castling_type, newBoards):
		king = board.king(castling_side)
		castling_file = 6 if castling_type == "K" else 2
		target_square = chess.square(castling_file, chess.square_rank(king))
		move = chess.Move(king, target_square)
		new_board = board.copy()
		new_board.push(move)
		newBoards[new_board.fen()] = new_board.copy()
	
	def handle_non_capture_moves(self, board, newBoards):
		for move in board.pseudo_legal_moves:
			if board.piece_at(move.to_square) is None:
				new_board = board.copy()
				new_board.push(move)
				newBoards[new_board.fen()] = new_board.copy()

	def boards_taken(self, tile, brds):
		newBoards = {}
		for fen, board in brds.items():
			if board.turn == self.color:
				board.turn = not self.color

			for move in board.pseudo_legal_moves:
				if board.is_capture(move) or board.is_en_passant(move):
					new_board = board.copy()
					new_board.push(move)
					if (new_board.piece_at(tile) is None or
							new_board.piece_at(tile).color != self.color):
						newBoards[new_board.fen()] = new_board.copy()

		return newBoards

	def sense_update_logic(self, sense_result, brds):
		# print("sense_update_logic")
		newBoards = {}
		for fen, board in brds.items():
			if self.is_consistent_with_sense_result(board, sense_result):
				newBoards[fen] = board.copy()

		return newBoards

	def is_consistent_with_sense_result(self, board, sense_result):
		# print("is_consistent_with_sense_result")
		for square, piece in sense_result:
			board_piece = board.piece_at(square)
			if (board_piece is None and piece is not None or
					board_piece is not None and piece is None or
					board_piece is not None and piece is not None and (
						board_piece.piece_type != piece.piece_type or
						board_piece.color != piece.color)):
				return False

		return True

	def move_update_logic(self, requested_move, taken_move, captured_opponent_piece, capture_square, brds):
		# print("move_update_logic")
		newBoards = {}
		for fen, board in brds.items():
			if board.turn != self.color:
				board.turn = self.color

			if taken_move is not None:
				if self.is_valid_taken_move(board, taken_move, captured_opponent_piece, capture_square):
					new_board = board.copy()
					new_board.push(taken_move)
					newBoards[new_board.fen()] = new_board.copy()
			elif requested_move is not None:
				if self.is_valid_pawn_move(board, requested_move):
					newBoards[fen] = board.copy()
			else:
				newBoards[fen] = board.copy()

		return newBoards

	def is_valid_taken_move(self, board, taken_move, captured_opponent_piece, capture_square):
		if taken_move in board.pseudo_legal_moves:
			if (captured_opponent_piece and board.piece_at(capture_square) is not None and
					board.piece_at(capture_square).piece_type != chess.KING):
				return True
			elif not captured_opponent_piece and board.piece_at(taken_move.to_square) is None:
				return True

		return False

	def is_valid_pawn_move(self, board, requested_move):
		piece = board.piece_at(requested_move.from_square)
		if piece is not None and piece.piece_type == chess.PAWN:
			if (board.piece_at(requested_move.to_square) is None and
					chess.square_file(requested_move.from_square) != chess.square_file(requested_move.to_square)):
				return True
			elif chess.square_file(requested_move.from_square) == chess.square_file(requested_move.to_square):
				rank_diff = abs(chess.square_rank(requested_move.from_square) - chess.square_rank(requested_move.to_square))
				if rank_diff == 2:
					intermediate_square = chess.square(
						chess.square_file(requested_move.to_square),
						chess.square_rank(requested_move.from_square) + (1 if chess.square_rank(requested_move.to_square) > chess.square_rank(requested_move.from_square) else -1)
					)
					if board.piece_at(intermediate_square) is not None:
						return True
				else:
					if board.piece_at(requested_move.to_square) is not None:
						return True
	
		return False
	
	def advance_boards(self, captured_my_piece, capture_square, boards):
		if captured_my_piece:
			return self.boards_taken(capture_square, boards)
		else:
			return self.boards_not_taken(boards)
	
	def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
		self.color = color
		self.possible_boards[board.fen()] = board.copy()
		self.checkpoints.append((-1, {board.fen(): board}))
		self.checkpoints.sort(key=lambda x: x[0])
		self.start_time = datetime.datetime.now()
	
	def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
		# print("handle_opponent_move_result")
		self.move_recovery = 0
		if self.move_no != 0 or self.color == chess.BLACK:
			self.possible_boards = self.advance_boards(captured_my_piece, capture_square, self.possible_boards)
 
	def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> Optional[Square]:
			# print("Choosing random 3x3 sense")
			sense_actions = self.filter_sense_actions(sense_actions)
			if sense_actions:
				return self.choose_random_3x3_sense(sense_actions)
			else:
				return None
	
	def choose_random_3x3_sense(self, sense_actions):
		while sense_actions:
			rank = random.randint(1, 6)
			file = random.randint(1, 6)
			sense_square = chess.square(file, rank)
	
			if sense_square in sense_actions:
				return sense_square
	
			sense_actions.remove(sense_square)
	
		return None
	
	def filter_sense_actions(self, sense_actions):
		filtered_actions = []
		for square in sense_actions:
			rank = chess.square_rank(square)
			file = chess.square_file(square)
			if 1 <= rank <= 6 and 1 <= file <= 6:
				filtered_actions.append(square)
		return filtered_actions
		
	def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
		# print("handle_sense_result")
		self.sense_results.append(sense_result)
		self.possible_boards = self.sense_update_logic(sense_result, self.possible_boards)

	def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
		# print("choose_move")
		if self.move_recovery > 3:
			return None

		if len(self.possible_boards) > 1000:
			self.possible_boards = self.limit_boards(self.possible_boards, 1000, 100)	

		timelimit = 1.0 / len(self.possible_boards) if self.possible_boards else 1.0

		moves, checks, mates = self.analyze_moves(move_actions, timelimit)

		if not moves and not checks and not mates:
			return self.handle_no_valid_moves(move_actions, seconds_left)

		return self.select_best_move(moves, checks, mates, move_actions)

	def limit_boards(self, boards, max_size, sample_size):
		if len(boards) > max_size:
			new_boards = {}
			for _ in range(sample_size):
				key = random.choice(list(boards))
				new_boards[key] = boards[key]
			self.checkpoints.append((self.move_no, boards))
			return new_boards
		return boards

	def analyze_moves(self, move_actions, timelimit):
		moves, checks, mates = [], [], []
		score, count = 0, 0
	
		for fen in self.possible_boards:
			board = chess.Board(fen)
	
			if self.move_no < 5 and not self.is_king_scanned(board):
				board.set_piece_at(chess.E1 if self.color == chess.WHITE else chess.E8, chess.Piece(chess.KING, self.color))
	
			mates.extend(self.find_mate_moves(board, move_actions))
	
			if board.turn != self.color:
				board.turn = not self.color
	
			if board.status() == chess.STATUS_VALID:
				score, count = self.evaluate_moves(board, move_actions, timelimit, score, count, moves, checks)
	
		return moves, checks, mates
	
	def is_king_scanned(self, board):
		for sense_result in self.sense_results:
			for square, piece in sense_result:
				if piece is not None and piece.piece_type == chess.KING and piece.color == self.color:
					return True
		return False

	def find_mate_moves(self, board, move_actions):
		enemy_king = board.king(not self.color)
		if enemy_king:
			king_attackers = board.attackers(self.color, enemy_king)
			return [chess.Move(attacker_square, enemy_king)
					for attacker_square in king_attackers
					if chess.Move(attacker_square, enemy_king) in move_actions]
		return []

	def evaluate_moves(self, board, move_actions, timelimit, score, count, moves, checks):
		try:
			result = self.engine.play(board, chess.engine.Limit(time=timelimit), root_moves=move_actions)
			if result and result.move:
				board.push(result.move)
				board.clear_stack()
				info = self.engine.analyse(board, chess.engine.Limit(time=timelimit/10.0))
				move_score = info["score"].pov(self.color).score(mate_score=100000)
				score += move_score
				count += 1
				if board.is_check():
					checks.append((result.move, move_score))
				else:
					moves.append((result.move, move_score))
		except (asyncio.exceptions.TimeoutError, chess.engine.EngineError, chess.engine.EngineTerminatedError, AssertionError):
			print(f'!!!!!!!!!!! -- Engine timeout at "{board.fen()}"')
			self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path, timeout=None)

		return score, count

	# PAY ATTENTION HERE!!!!!!!!!!!!!!!!!
	def handle_no_valid_moves(self, move_actions, seconds_left):
		return random.choice(move_actions) if move_actions else None

	def refresh_state_stack(self):
		to_add = {fen: board for fen, board in self.possible_boards.items()}
		self.possible_boards.clear()
		self.checkpoints.append((self.move_no, to_add))

	def select_best_move(self, moves, checks, mates, move_actions):
		# print("select_best_move")
		# print(f"Moves: {len(moves)} || Checks: {len(checks)} || Mates: {len(mates)}")
  
		for move in mates:
			if self.is_valid_move(move):
				# print(f"Mate!!! {move}")
				return move

		for move, _ in sorted(checks, key=lambda x: x[1], reverse=True):
			if move in move_actions and self.is_valid_move(move):
				# print(f"Checked?! {move}")
				return move

		for move, _ in sorted(moves, key=lambda x: x[1], reverse=True):
			if move in move_actions and self.is_valid_move(move):
				# print(move)
				return move

		for move in move_actions:
			if self.is_valid_move(move):
				# print(f"Safe Move? {move}")
				return move

		# print("No valid move chosen")
		return None

	def is_valid_move(self, move):
		for fen in self.possible_boards:
			board = chess.Board(fen)
			if move in board.pseudo_legal_moves and board.is_into_check(move):
				return False
			elif move not in board.pseudo_legal_moves and board.is_check():
				return False
		return True

	def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
						   captured_opponent_piece: bool, capture_square: Optional[Square]):
		# print("handle_move_result")
		self.update_potential_boards(requested_move, taken_move, captured_opponent_piece, capture_square)
		self.move_no += 1
		# self.print_move_result_info()
	
	def update_potential_boards(self, requested_move, taken_move, captured_opponent_piece, capture_square):
		self.possible_boards = self.move_update_logic(requested_move, taken_move, captured_opponent_piece, capture_square, self.possible_boards)
		# if captured_opponent_piece:
			# print("I killed something")
	
	def print_move_result_info(self):
		earliest_checkpoint = self.checkpoints[0][0] if self.checkpoints else "---"
		print(f"Considering {len(self.possible_boards)} potential board states || Earliest Checkpoint: {earliest_checkpoint}")
		print(f"StockyInf.:\t End move {self.move_no}")
	
	def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason],
						game_history: GameHistory):
		self.quit_engine()
		self.print_game_duration()
	
	def quit_engine(self):
		try:
			self.engine.quit()
		except:
			print("Engine quit failed")
	
	def print_game_duration(self):
		self.end_time = datetime.datetime.now()
		game_duration = self.end_time - self.start_time
		minutes, seconds = divmod(game_duration.total_seconds(), 60)
		print(f"Game Duration: {int(minutes)} minutes {int(seconds)} seconds")
