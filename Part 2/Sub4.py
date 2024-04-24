import chess

def consistent_states(N, states, window):
    consistent_states = []

    # Parse the window description
    window_squares = window.strip().split(';')
    window_dict = {square_piece.split(':')[0]: square_piece.split(':')[1] for square_piece in window_squares}

    # Iterate over each potential state
    for fen_str in states:
        board = chess.Board(fen_str)

        # Check if the pieces in the window squares match the window description
        consistent = True
        for square, piece in window_dict.items():
            fen_square = board.piece_at(chess.parse_square(square))
            if fen_square is None:
                # If the square is empty, it should match the window piece or be '?'
                if piece != '?':
                    consistent = False
                    break
            elif fen_square.symbol().lower() != piece.lower():
                # If the piece in the square doesn't match the window piece, it's inconsistent
                consistent = False
                break

        # If the state is consistent with the window observation, include it in the output
        if consistent:
            consistent_states.append(fen_str)

    return sorted(consistent_states)


# Read input
N = int(input())
states = [input() for _ in range(N)]
window = input()

# Output consistent states
result = consistent_states(N, states, window)

for state in result:
    print(state)


