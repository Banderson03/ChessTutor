from stockfish import Stockfish

# Creating an object with a local download of the engine passed in
stockfish = Stockfish(path="ChessTutor\stockfish\stockfish-windows-x86-64-avx2.exe")

# Setting parameters of the model
stockfish.set_depth(20)
stockfish.set_skill_level(20)
print(stockfish.get_parameters())

# Setting board positions and retreiving top moves and evaluation
stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
print(stockfish.get_evaluation())
print(stockfish.get_best_move())
