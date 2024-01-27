import board_handler
import time
from openai import OpenAI
from stockfish import Stockfish
import pygame
from pygame.locals import *
import chess
import chess.engine
import sys


class AI_Player:
    def __init__(self, board):
        self.board = board


        if sys.platform.startswith('win32'):
            self.engine = chess.engine.SimpleEngine.popen_uci("ChessTutor/komodo-14.1-64bit.exe")
            self.stockfish = Stockfish(path="ChessTutor/stockfish/stockfish-windows-x86-64-avx2.exe")
        else:
            self.engine = chess.engine.SimpleEngine.popen_uci("ChessTutor/komodo-14.1-64-osx")
            self.stockfish = Stockfish(path="ChessTutor/stockfish")


        self.engine.configure({"Skill": 1})
        # print(self.engine.analyse(self.board, chess.engine.Limit(time = 0.1)))
        self.getAnalysis()


    # Use try catches to find the right komodo (if they are using the mac or linux one)

    # def setFen(self, fen):
    #     self.fen = fen
    #     self.stockfish.set_fen_position(self.fen)


    def getMove(self):
        # print(self.stockfish.get_parameters())
        result = self.engine.play(self.board, chess.engine.Limit(time = 0.1)).move
        result = str(result)
        print(result)

        return result
    
    def quitEngine(self):
        self.engine.quit()

    
    def getAnalysis(self):
        fen = self.board.fen()
        self.stockfish.set_fen_position(fen)
        evaluation = self.stockfish.get_evaluation()
        return evaluation
        if evaluation['type'] == 'cp':
            centipawn_advantage = evaluation['value']
            if centipawn_advantage[0] == "-":
                print("Advantage")
            print(f"The centipawn advantage is {centipawn_advantage}")
        else:
            print("The position is a checkmate.")