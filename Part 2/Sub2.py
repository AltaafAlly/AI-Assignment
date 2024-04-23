import chess
import chess.engine
from reconchess import utilities

def next_positions(fen):
    board = chess.Board(fen)
    positions = []

    # Generate all legal moves, including castling moves
    moves = list(board.pseudo_legal_moves)
    moves.append(chess.Move.null())

    # Append castling moves
    for move in utilities.without_opponent_pieces(board).generate_castling_moves():
        if not utilities.is_illegal_castle(board, move):
            moves.append(move)

    # Apply each move and append resulting positions to the list
    for move in moves:
        new_board = board.copy()
        new_board.push(move)
        positions.append(new_board.fen())

    return sorted(set(positions))

fen = input()
print("\n".join(next_positions(fen)))
