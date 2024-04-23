import chess

def PrintBoard(Board):
    print(Board)

x = input()
board = chess.Board(x)

y = input()
board.push(chess.Move.from_uci(y))

print(board.fen())