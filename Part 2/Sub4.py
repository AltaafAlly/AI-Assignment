import chess

def parse_window(window_str):
    window = {}
    for square_piece in window_str.split(';'):
        square, piece = square_piece.split(':')
        window[chess.parse_square(square)] = piece
    return window

def is_consistent(board, window):
    for square, piece in window.items():
        if piece != '?' and piece != board.piece_at(square).symbol():
            return False
    return True

def filter_states(states, window_str):
    window = parse_window(window_str)
    return [state for state in states if is_consistent(chess.Board(state), window)]


n = int(input())
states = [input() for _ in range(n)]
window_str = input()
print("\n".join(sorted(filter_states(states, window_str))))