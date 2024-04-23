import chess

def CreateBoard(board):
    return chess.Board(board)

def PrintBoard(Board):
    print(Board)

Board = input()

PrintBoard(CreateBoard(Board))