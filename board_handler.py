import time
from openai import OpenAI
from stockfish import Stockfish
import pygame
from pygame.locals import *
import chess

PImage = {}
boardReference = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["__", "__", "__", "__", "__", "__", "__", "__"],
    ["__", "__", "__", "__", "__", "__", "__", "__"],
    ["__", "__", "__", "__", "__", "__", "__", "__"],
    ["__", "__", "__", "__", "__", "__", "__", "__"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

lightSquareColor = (241, 217, 181)
darkSquareColor = (181, 136, 99)

class Board:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface
        self.moves = pygame.transform.scale(pygame.image.load("ChessTutor/images/Moves of the king.png"), (300, 300))
        self.boardEngine = chess.Board()
        self.board = [] 
        self.loadBoard()
        self.loadPieces()
        self.log = []
        self.whiteMove = True      
    
    def loadBoard(self):
        tileType = True
        color = (241, 217, 181)
        for row in range(8):
            rank = []
            tileType = not tileType
            for col in range(8):
                ref = boardReference[row][col]
                tileType = not tileType
                if tileType:
                    color = lightSquareColor
                else:
                    color = darkSquareColor
                rank.append(Tile(col, row, ref, color, self.parent_surface))
            self.board.append(rank)
            
    
    def loadPieces(self):
        pieceKeys = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
        for key in pieceKeys:
            PImage[key] = pygame.transform.scale(pygame.image.load("ChessTutor/images/" + key + ".png"), (96, 96))


    def drawBoard(self):
        for row in range(8):
            for col in range(8):               
                self.board[row][col].draw()
        pygame.display.flip()


    def movePiece(self, move):
        piece = self.board[move.s1Row][move.s1Col].getPiece()
        self.board[move.s1Row][move.s1Col].setPiece("__")
        self.board[move.s2Row][move.s2Col].setPiece(piece)
        
        self.log.append(move.notateMove())
        self.whiteMove = not self.whiteMove


    def handleMove(self, p1, p2):
        move = Move(p1, p2, self.board)
        print(move.notateMove())
        self.movePiece(move)

    

class Tile:
    def __init__(self, x, y, piece, color, parent_surface):
        self.file = x
        self.rank = y
        self.x = 32 + (100 * self.file)
        self.y = 12 + (100 * self.rank)
        self.piece = piece
        self.surface = parent_surface
        self.color = color

    def draw(self):
        tile_rect = pygame.rect.Rect(self.x, self.y, 100, 100)

        pygame.draw.rect(self.surface, self.color, tile_rect)
        if self.piece != "__":
            self.surface.blit(PImage[self.piece], (self.x + 2, self.y + 6))
        pygame.display.flip()
    
    def setPiece(self, piece):
        self.piece = piece

    def getPiece(self):
        return self.piece



class Move:
    rankToRow = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}
    fileToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    rowToRank = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
    colToRank = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    def __init__(self, s1, s2, board):
        self.s1Row = s1[0]
        self.s1Col = s1[1]
        self.s2Row = s2[0]
        self.s2Col = s2[1]
        self.movedPiece = board[self.s1Row][self.s1Col]
        self.capturedPiece = board[self.s2Row][self.s2Col]
    
    def convertCoordinates(self, row, col):
        return (self.rowToRank[row] + self.colToRank[col])
    
    def notateMove(self):
        return (self.convertCoordinates(self.s1Row, self.s1Col) + self.convertCoordinates(self.s2Row, self.s2Col))
    

    