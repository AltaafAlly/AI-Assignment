import chess

def next_capture_states(fen, capture_square):
    board = chess.Board(fen)
    square = chess.parse_square(capture_square)
    states = []
    for move in board.legal_moves:
        if board.is_capture(move) and move.to_square == square:
            board.push(move)
            states.append(board.fen()) 
            board.pop()
    return sorted(states)

if __name__ == "__main__":
    fen = input()
    capture_square = input()
    print("\n".join(next_capture_states(fen, capture_square)))