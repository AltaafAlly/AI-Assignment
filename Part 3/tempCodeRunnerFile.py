    for move in legal_moves:
            if self.board.is_capture(move) and self.board.is_king(self.board.piece_at(move.to_square)) and \
                    self.board.piece_at(move.from_square).color == self.color:
                return move

        # If no move captures the opponent's king, ask Stockfish for a move
        try:
            self.board.turn = self.color
            self.board.clear_stack()
            result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
            return result.move
        except chess.engine.EngineTerminatedError:
            print('Stockfish Engine died')
        except chess.engine.EngineError:
            print('Stockfish Engine bad state at "{}"'.format(self.board.fen()))

        # If all else fails, return None
        return None