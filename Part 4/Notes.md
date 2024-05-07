#Stuff we did to our bot so far

- Used the trout bot a basline to help put bot to make moves 
- Added Prioritize Move which does the following:
- this part of the code prioritizes capturing opponent pieces, giving preference to capturing higher-value pieces and also considering captures where a piece exists at the destination square. If no such moves are available, it falls back to using the stockfish chess engine to choose a move.
- Piece Value Calculation: The value_of_piece method assigns numerical values to different chess pieces based on their type (pawn, knight, bishop, rook, queen, and king) and color. These values are used for evaluating moves during gameplay