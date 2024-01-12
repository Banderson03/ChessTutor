from stockfish import Stockfish

# Creating an object with a local download of the engine passed in
stockfish = Stockfish(path="ChessTutor\stockfish\stockfish-windows-x86-64-avx2.exe")

# Setting parameters of the model
stockfish.set_depth(20)
stockfish.set_skill_level(20)
print(stockfish.get_parameters())

# Setting board positions and retreiving top moves and evaluation
stockfish.set_fen_position("rnbqkb1r/pp1p1ppp/2p1pn2/8/3P4/2N2N2/PPP1PPPP/R1BQKB1R w KQkq - 0 4")
print(stockfish.get_evaluation())
print(stockfish.get_top_moves())
