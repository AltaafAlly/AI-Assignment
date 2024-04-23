import chess
import chess.engine
from reconchess import utilities

def next_moves(fen):
    board = chess.Board(fen)
    moves = list(board.pseudo_legal_moves)
    moves.append(chess.Move.null())

    for move in utilities.without_opponent_pieces(board).generate_castling_moves():
        if not utilities.is_illegal_castle(board, move):
            moves.append(move)

    return sorted(set(str(move) for move in moves))


fen = input()
print("\n".join(next_moves(fen)))