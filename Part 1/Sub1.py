import chess

# Create a board from the input string (Push test)
def CreateBoard(board):
    return chess.Board(board)

def PrintBoard(Board):
    print(Board)

Board = input()

PrintBoard(CreateBoard(Board))