import time
from openai import OpenAI
from stockfish import Stockfish
import pygame
from pygame.locals import *

BACKGROUND_COLOR = (49, 46, 43)
PImage = {}
gameLog = []

class Board:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface
        self.image = pygame.transform.scale(pygame.image.load("ChessTutor/images/board.png"), (900, 860))
        self.moves = pygame.transform.scale(pygame.image.load("ChessTutor/images/Moves of the king.png"), (300, 300))
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.log = []
        self.whiteMove = True
        self.pieceDictionary= {"bR": "rook", }

        self.potentialThreats = []
        

    
    def loadPieces(self):
        pieceKeys = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
        for key in pieceKeys:
            PImage[key] = pygame.transform.scale(pygame.image.load("ChessTutor/images/" + key + ".png"), (114, 114))

    def drawPieces(self): 
        for rank in range(8):
            for file in range(8):
                curPiece = self.board[rank][file]
                if curPiece != "__": 
                    self.parent_surface.blit(PImage[curPiece], (28 + (107.5 * file), 5 + (101.6 * rank)))


    def drawBoard(self):
        self.parent_surface.blit(self.image, (0,0))
        self.parent_surface.blit(self.moves, (1000,0))
        self.drawPieces()
        pygame.display.flip()

    def movePiece(self, move):
        self.board[move.s1Row][move.s1Col] = "__"
        self.board[move.s2Row][move.s2Col] = move.movedPiece
        self.log.append(move.notateMove())
        self.whiteMove = not self.whiteMove

    def handleMove(self, p1, p2):
        move = Move(p1, p2, self.board)
        print(move.notateMove())
        self.movePiece(move)

    def pieceCheckLoop(self):
        temp = "__"

        for row in range(8):
            for col in range(8):
                temp = self.board[row][col]
                if temp == "bp"or temp == "wp":
                    self.pawn()
                elif temp == "bN" or temp == "wN":
                    self.knight()
                elif temp == "bB" or temp == "wB":
                    self.bishop()
                elif temp == "bR" or temp == "wR":
                    self.rook()
                elif temp == "bQ" or temp == "wQ":
                    self.queen()
                elif temp == "bK" or temp == "wK":
                    self.king()
        
    
    def rook(self):
        # Generate all valid moves, once past 
        print("yay")

    def knight(self):
        print("yay")

    def bishop(self):
        print("yay")
    
    def queen(self):
        print("yay")

    def king(self):
        print("yay")

    def pawn(self):
        print("yay")

class Move():

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


class Game:
    def __init__(self):
        pygame.display.set_caption("ChessTutor (Powered by GPT)")
        self.surface = pygame.display.set_mode((1600,900))
        self.surface.fill(BACKGROUND_COLOR)
        self.clock = pygame.time.Clock()
        self.board = Board(self.surface)
        self.board.loadPieces()
        self.board.drawBoard()
        self.selection = ()
        self.clickSequence = []
        

        # 8-3 = 5 | 3 + 8 = 11| 11- 5 = 6 || 3 = n 8 = N
        # top lef corner (32, 13)
        # y change = 101px per
        # x change = 107px per
        # pygame.draw.rect(self.surface, (255,0,0), pygame.Rect(890, 13, 2, 2))
        # pygame.display.flip()

    def mouseHandler(self):
        x, y = pygame.mouse.get_pos()

        if x < 890 and x > 32:
            if y < 824 and y > 13:
                col = (x - 32) // 107
                row = (y - 13) // 101
                if self.selection == (row, col):
                    self.selection = ()
                    self.clickSequence = []
                else:
                    
                    self.selection = (row, col)
                    self.clickSequence.append(self.selection)
                if len(self.clickSequence) == 2:
                    self.board.handleMove(self.clickSequence[0], self.clickSequence[1])
                    self.selection = ()
                    self.clickSequence = []
                    self.board.drawBoard()
                    self.board.pieceCheckLoop()

                


    def run(self):

        # placeholder standard pygame controls
        running = True
        menu = False
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():

                # if not menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # print("uh")
                    self.mouseHandler()

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        print("return")
                        menu = False

                
                elif event.type == QUIT:
                    print("quit")
                    running = False
            try:
                if not menu:
                    time.sleep(0)
                    # self.play()
            except Exception as e:
                # self.show_game_over()
                print("menu")
                menu = True
                self.reset()

            clock.tick(15)




if __name__ == "__main__":
    game = Game()
    game.run()
    # Oh boy