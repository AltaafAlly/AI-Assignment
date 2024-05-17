from reconchess import utilities, Player, List, Optional, Color, Square, WinReason, GameHistory, Tuple
import chess
import random
import chess.engine
import os
import time

# Define the path to the Stockfish executable
# stockfish_path = r"C:\Users\altaa\Documents\GitHub\AI-Assignment\Part 3\stockfish\stockfish"
stockfish_path = r'D:\\Wits\\Honours\\AI\\AI-Assignment\\Part 3\\stockfish\\stockfish.exe'

# Define the path to the Stockfish executable for the automarker
# stockfish_path = '/opt/stockfish/stockfish'

class RandomSensing(Player):
    def __init__(self):
        self.board = None
        self.color = None
        self.my_piece_captured_square = None
        self.possible_states = set()
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)

    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
        self.board = board.copy()
        self.color = color
        self.possible_states.add(board.fen())
        self.start_time = time.time()

    def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
        # if the opponent captured our piece, remove it from our board.
        self.my_piece_captured_square = capture_square
        if captured_my_piece:
            self.board.remove_piece_at(capture_square)
            
        # If the number of possible states exceeds 10000, randomly remove states
        if len(self.possible_states) > 10000:
            self.possible_states = random.sample(list(self.possible_states), 10000)

        #print("handle_opponent_move_result(start): ", len(self.possible_states))
        # Update the possible states based on the opponent's move
        updated_states = set()
        for state in self.possible_states:
            board = chess.Board(state)

            # Check if the opponent's move is legal in the current state
            for move in board.legal_moves:
                board.push(move)
                updated_states.add(board.fen())
                board.pop()

        self.possible_states = updated_states
        #print("handle_opponent_move_result(end): ", len(self.possible_states))
            
    def choose_sense(
    self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float,) -> Optional[Square]:
        while True:
            # Choose a random sense action
            sense_square = random.choice(sense_actions)

            # Check if the 3x3 region around the sense square is fully on the board
            rank, file = chess.square_rank(sense_square), chess.square_file(sense_square)
            if 1 <= rank <= 6 and 1 <= file <= 6:
                return sense_square

    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
        # If the number of possible states exceeds 10000, randomly remove states
        if len(self.possible_states) > 10000:
            self.possible_states = random.sample(list(self.possible_states), 10000)
        
        # Update the possible states based on the sense result   
        updated_states = set()
        #print("handle_sense_result(start): ", len(self.possible_states))
        for state in self.possible_states:
            board = chess.Board(state)

            # Check if the sense result matches the current state
            match = True
            for square, piece in sense_result:
                if board.piece_at(square) != piece:
                    match = False
                    break
                
            if match:
                updated_states.add(state)

        self.possible_states = updated_states
        #print("handle_sense_result(end): ", len(self.possible_states))

        # Update our board with the sensed pieces
        for square, piece in sense_result:
            self.board.set_piece_at(square, piece)

    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        # If we might be able to take the king, try to
        enemy_king_square = self.board.king(not self.color)
        if enemy_king_square:
            # If there are any ally pieces that can take the king, execute one of those moves
            enemy_king_attackers = self.board.attackers(self.color, enemy_king_square)
            if enemy_king_attackers:
                attacker_square = enemy_king_attackers.pop()
                return chess.Move(attacker_square, enemy_king_square)

        # print('choose_move(start):', len(self.possible_states))
        # If there are no possible states, use the current board state
        if not self.possible_states:
            self.possible_states = [self.board.fen()]

        # If the number of possible states exceeds 10000, randomly remove states
        if len(self.possible_states) > 10000:
            self.possible_states = random.sample(list(self.possible_states), 10000)

        # Determine the time limit for each board based on the number of possible states
        time_limit = 10 / len(self.possible_states)

        # Initialize a dictionary to store the best moves for each state
        best_moves = {}

        # print("number of states: ", len(self.possible_states))
        # Iterate over each possible state
        for state in self.possible_states:
            try:
                board = chess.Board(state)
                board.turn = self.color

                # Use Stockfish to determine the best move for the current state
                result = self.engine.play(board, chess.engine.Limit(time=time_limit))

                # Check if result move is legal
                if result.move in board.legal_moves:
                    best_moves[state] = result.move
                else:
                    # Handle illegal move
                    print(f"Illegal move suggested by engine: {result.move} in state {state}")
                    # Optional: re-initialize the engine if it's consistently giving illegal moves
                    self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)

            except chess.engine.EngineTerminatedError:
                # print('Stockfish Engine died')
                self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)
                continue
            except chess.engine.EngineError:
                print('Stockfish Engine bad state at "{}"'.format(self.board.fen()))

        # Perform majority voting to select the move
        move_counts = {}
        for move in best_moves.values():
            if move is not None:
                move_counts[move] = move_counts.get(move, 0) + 1

        # Filter out moves that are not in the valid move list
        valid_moves = [move for move in move_counts if move in move_actions]

        if valid_moves:
            # Choose the move with the highest count
            best_move = max(valid_moves, key=move_counts.get)
            return best_move
        else:
            # If no valid moves or no majority, choose a random move
            return random.choice(move_actions) if move_actions else None


    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
                       captured_opponent_piece: bool, capture_square: Optional[Square]):
        # If a move was executed, apply it to our board
        if taken_move is not None:
            self.board.push(taken_move)

            # If an opponent's piece was captured, update the possible states
            if captured_opponent_piece:
                updated_states = set()
                for state in self.possible_states:
                    board = chess.Board(state)
                    if board.piece_at(capture_square) is not None:
                        board.remove_piece_at(capture_square)
                        updated_states.add(board.fen())
                self.possible_states = updated_states

        # If the number of possible states exceeds 10000, randomly remove states
        if len(self.possible_states) > 10000:
            self.possible_states = random.sample(list(self.possible_states), 10000)

        # Update the possible states based on the move result
        updated_states = set()
        #print("handle_move_result(start): ", len(self.possible_states))
        for state in self.possible_states:
            board = chess.Board(state)

            # Check if the taken move is legal in the current state
            if taken_move in board.legal_moves:
                board.push(taken_move)
                updated_states.add(board.fen())
            else:
                # If the taken move is not legal, check if the requested move is legal
                if requested_move and requested_move in board.legal_moves:
                    #print("Requested move was taken")
                    board.push(requested_move)
                    updated_states.add(board.fen())

        self.possible_states = updated_states
        #print("handle_move_result(end): ", len(self.possible_states))

    def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason], game_history: GameHistory):
        try:
            self.engine.quit()
        except chess.engine.EngineTerminatedError:
            pass
        
        # Calculate and print the total game time
        end_time = time.time()
        total_time = end_time - self.start_time
        print(f"Total game time: {total_time:.2f} seconds")