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

rankToRow = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}
fileToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
rowToRank = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
colToFile = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


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
        self.selection = ()
        self.clickSequence = []
        self.alteredTiles = []

    
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


    def movePiece(self, t1, t2):
        piece = t1.getPiece()
        t1.setPiece("__")
        t2.setPiece(piece)
        move = (t1.getNotation() + t2.getNotation())
        print(move)
        self.log.append(move)
        self.whiteMove = not self.whiteMove


    def handleMove(self, p1, p2):
        t1 = self.board[p1[0]][p1[1]]
        t2 = self.board[p2[0]][p2[1]]
        self.movePiece(t1, t2)
        

    def resetBoardHighlighting(self):
        for tile in self.alteredTiles:
            self.board[tile[0]][tile[1]].resetTile()


    def resetBoardSelections(self):
        self.selection = ()
        self.clickSequence = []
        self.resetBoardHighlighting()


    def updateSelections(self, click):
        if self.selection == click:
            self.resetBoardSelections
        else:
            self.selection = click
            self.clickSequence.append(self.selection)
            if len(self.clickSequence) == 2:
                self.handleMove(self.clickSequence[0], self.clickSequence[1])
                self.resetBoardSelections()
                self.drawBoard()
            else:
                self.board[click[0]][click[1]].setColor((212, 211, 211))
                self.alteredTiles.append((click[0], click[1]))
                self.drawBoard()    



class Tile:
    def __init__(self, x, y, piece, color, parent_surface):
        self.col = x
        self.row = y
        self.file = colToFile[self.col]
        self.rank = rowToRank[self.row]
        self.x = 32 + (100 * self.col)
        self.y = 12 + (100 * self.row)
        self.piece = piece
        self.surface = parent_surface
        self.defaultColor = color
        self.color = color
        self.mark = False

    def draw(self):
        tile_rect = pygame.rect.Rect(self.x, self.y, 100, 100)

        pygame.draw.rect(self.surface, self.color, tile_rect)
        if self.piece != "__":
            self.surface.blit(PImage[self.piece], (self.x + 2, self.y + 6))
        if self.mark:
            pass
        pygame.display.flip()
    

    def setPiece(self, piece):
        self.piece = piece


    def getPiece(self):
        return self.piece
    

    def getNotation(self):
        return (self.rank + self.file)
    

    def setColor(self, highlight):
        self.color = highlight


    def resetTile(self):
        self.color = self.defaultColor
        self.mark = False

# class Move:

#     def __init__(self, s1, s2, board):
#         self.s1Row = s1[0]
#         self.s1Col = s1[1]
#         self.s2Row = s2[0]
#         self.s2Col = s2[1]
#         self.movedPiece = board[self.s1Row][self.s1Col]
#         self.capturedPiece = board[self.s2Row][self.s2Col]
    
#     def convertCoordinates(self, row, col):
#         return (self.rowToRank[row] + self.colToRank[col])
    
#     def notateMove(self):
#         return (self.convertCoordinates(self.s1Row, self.s1Col) + self.convertCoordinates(self.s2Row, self.s2Col))
    

    