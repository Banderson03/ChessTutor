import board_handler
import time
from openai import OpenAI
from stockfish import Stockfish
import pygame
from pygame.locals import *
import chess


class AI_Player:
    def __init__(self):
        self.stockfish = Stockfish(path="ChessTutor\stockfish\stockfish-windows-x86-64-avx2.exe", parameters={"UCI_LimitStrength": "true", "UCI_Elo": 10})
        self.stockfish.set_depth(2)
        print(self.stockfish.get_parameters())
        self.fen = ""


    def setFen(self, fen):
        self.fen = fen
        self.stockfish.set_fen_position(self.fen)


    def getMove(self):
        print(self.stockfish.get_parameters())

        return self.stockfish.get_best_move()