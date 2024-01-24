import time
from openai import OpenAI
from stockfish import Stockfish
import pygame
from pygame.locals import *
import chess
import ai_handler
import main

PImage = {}
marker = pygame.transform.scale(pygame.image.load("ChessTutor/images/marker.png"), (34, 34))
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


LIGHTSQUARECOLOR = (241, 217, 181)
DARKSQUARECOLOR = (181, 136, 99)
LIGHTGRAYCOLOR = (148, 146, 145)
pygame.font.init()
font = pygame.font.SysFont("subway", 42)



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
        self.moveList = []
        self.ai_Mode = False
        self.capturedWhitePieces = []
        self.capturedBlackPieces = []
        self.boardHistory = []
        self.aiTurn = False
        # self.capturedBlackPieces.append("bR")
        # self.capturedWhitePieces.append("wR")
        # self.capturedBlackPieces.append("bQ")
        # self.capturedWhitePieces.append("wQ")
        self.AI_Player = ai_handler.AI_Player(self.boardEngine)


    def quitAiEngine(self):
        self.AI_Player.quitEngine()
    
    def loadBoard(self):
        tileType = True
        color = (241, 217, 181)
        for row in range(8):
            rank = []
            tileType = not tileType
            for col in range(8):
                piece = boardReference[row][col]
                tileType = not tileType
                if tileType:
                    color = LIGHTSQUARECOLOR

                else:
                    color = DARKSQUARECOLOR
                rank.append(Tile(col, row, piece, color, self.parent_surface))
            self.board.append(rank)
            
    
    def loadPieces(self):
        pieceKeys = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
        for key in pieceKeys:
            PImage[key] = pygame.transform.scale(pygame.image.load("ChessTutor/images/" + key + ".png"), (96, 96))

    def drawBoardUI(self):
        for num in range(8):
            self.parent_surface.blit(font.render(chr(ord('a') + num), True,  LIGHTGRAYCOLOR), (75 + (100 * num), 820))
            self.parent_surface.blit(font.render(chr(ord('8') - num), True, LIGHTGRAYCOLOR), (6, 50 + (100 * num)))

        moveRect = pygame.rect.Rect(30, 855, 165, 50)
        pygame.draw.rect(self.parent_surface, (49, 46, 43), moveRect)

        # moveRectBorder = pygame.rect.Rect(30, 855, 165, 50)
        # pygame.draw.rect(self.parent_surface, (149, 46, 43), moveRectBorder, 3)

        if self.whiteMove:
            self.parent_surface.blit(font.render("White Turn", True, (255, 255, 255)), (40, 865))
        else:
            self.parent_surface.blit(font.render("Black Turn", True, (0, 0, 0)), (40, 865))

        evaluation = self.AI_Player.getAnalysis()

        if evaluation['type'] == "cp":
            centipawn_advantage = evaluation['value']
            print(centipawn_advantage)
            self.parent_surface.blit(font.render("Advantage:  " + str(centipawn_advantage), True, (255, 255, 255)), (600, 865))
        
        # fileText = font.render("a                      b", True, (148, 146, 145))
        # fileLabel = fileText.get_rect()
        # fileLabel.center = ((100,830))
        # self.parent_surface.blit(fileText, fileLabel)

    def drawBoard(self):
        for row in range(8):
            for col in range(8):               
                self.board[row][col].draw()
        self.drawBoardUI()
        self.drawCapturedPieces()
        # print(self.captured_Pieces)
        pygame.display.flip()



    def drawCapturedPieces(self):
        piecesRect = pygame.rect.Rect(836, 12, 37, 800)
        pygame.draw.rect(self.parent_surface, (49, 46, 43), piecesRect)

        for piece in range(len(self.capturedWhitePieces)):
            self.parent_surface.blit(pygame.transform.scale(PImage[self.capturedWhitePieces[piece][0]], (30, 30)), (834, 12 + (26 * piece)))

        for piece in range(len(self.capturedBlackPieces)):
            self.parent_surface.blit(pygame.transform.scale(PImage[self.capturedBlackPieces[piece][0]], (30, 30)), (834, 780 - (26 * piece)))


    def saveBoard(self):
        snapshot = []
        for row in range(8):
            tRow = []
            for col in range(8):
                tRow.append(self.board[row][col].getPiece())
            snapshot.append(tRow)
        self.boardHistory.append(snapshot)

    def undoMove(self):
        turn = len(self.boardHistory)
        if turn != 0:
            self.boardEngine.pop()
            boardSnapshot = self.boardHistory.pop()
            self.resetBoardSelections()
            # print(boardSnapshot)
            for row in range(8):
                for col in range(8):
                    self.board[row][col].setPiece(boardSnapshot[row][col])
            
            try:
                bP = self.capturedBlackPieces[len(self.capturedBlackPieces) - 1][1]
                print(bP)
                print(turn)
                if bP == turn:
                    print(self.capturedBlackPieces)
                    self.capturedBlackPieces.pop()   
                    print(self.capturedBlackPieces)
            except:
                pass

            try:
                wP = self.capturedWhitePieces[len(self.capturedWhitePieces) - 1][1]
                print(wP)
                print(turn)
                if wP == turn:
                    print(self.capturedWhitePieces)
                    self.capturedWhitePieces.pop()   
                    print(self.capturedWhitePieces)
            except:
                pass

            self.whiteMove = not self.whiteMove
            self.aiTurn = not self.aiTurn
            if self.aiTurn and self.ai_Mode:
                self.undoMove()
            self.AI_Player.getAnalysis()
            self.drawBoard()


    def invertBoard(self):
        # self.whiteMove = not self.whiteMove
        self.aiTurn = not self.aiTurn
        if self.aiTurn and self.ai_Mode:
            self.aiMovePiece()
            self.drawBoard()

    def movePiece(self, t1, t2):
        uci_move = (t1.getNotation() + t2.getNotation())
        uci_movePromote = uci_move + "q"
      
        if (uci_move in self.moveList) or (self.aiTurn and self.ai_Mode) or (uci_movePromote in self.moveList):

            self.saveBoard()

            if t1.getPiece()[1] == "p" and self.handlePromotion(t1):
                print("we in")
                move = chess.Move.from_uci(uci_movePromote)
            else:
                move = chess.Move.from_uci(uci_move)

                if self.boardEngine.is_castling(move):
                    self.handleCastling(t1, move)
                if self.boardEngine.is_en_passant(move):
                    self.handleEnPassant()


            piece = t1.getPiece()
            
            # print(move)
            if (self.boardEngine.is_capture(move)):
                if not self.boardEngine.is_en_passant(move):
                    if t2.getPiece()[0] == "w":
                        self.capturedWhitePieces.append((t2.getPiece(), len(self.boardHistory)))
                    else:
                        self.capturedBlackPieces.append((t2.getPiece(), len(self.boardHistory)))
                else:
                    if self.whiteMove:
                        self.capturedBlackPieces.append(("bp", len(self.boardHistory)))
                    else:
                        self.capturedWhitePieces.append(("wp", len(self.boardHistory)))

            self.boardEngine.push(move)
            self.log.append(move)
            t1.setPiece("__")
            t2.setPiece(piece)
            self.whiteMove = not self.whiteMove
            self.aiTurn = not self.aiTurn
            self.AI_Player.getAnalysis()

            # print(self.alteredTiles)

        
    def aiMovePiece(self):
        # self.AI_Player.setFen(self.boardEngine.fen())
        move = self.AI_Player.getMove()
        print("AI" + move)
        self.log.append(move)
        t1 = self.board[rankToRow[move[1]]][fileToCol[move[0]]]
        t2 = self.board[rankToRow[move[3]]][fileToCol[move[2]]]
        
        self.movePiece(t1, t2)
        # self.drawBoard()


    def handlePromotion(self, t1):
        if self.whiteMove and t1.getNotation()[1] == "7":
            t1.setPiece("wQ")
        elif (not self.whiteMove) and t1.getNotation()[1] == "2":
            t1.setPiece("bQ")
        else:
            return False
        return True
        

    
    def handleCastling(self, t1, move):
        print("cas")
        if self.boardEngine.is_kingside_castling(move):
            if self.whiteMove:
                self.board[7][7].setPiece("__")
                self.board[7][5].setPiece("wR")
            else:
                self.board[0][7].setPiece("__")
                self.board[0][5].setPiece("bR")
        else:
            if self.whiteMove:
                self.board[7][0].setPiece("__")
                self.board[7][3].setPiece("wR")
            else:
                self.board[0][0].setPiece("__")
                self.board[0][3].setPiece("bR")


    def handleEnPassant(self):
        captured_Piece = self.boardEngine.ep_square

        if self.whiteMove:
            captured_Piece -= 8
        else:
            captured_Piece += 8

        row = 7 - (captured_Piece // 8)
        col = captured_Piece % 8

        self.board[row][col].setPiece("__")


    # def handleMove(self, p1, p2):
    #     t1 = self.board[p1[0]][p1[1]]
    #     t2 = self.board[p2[0]][p2[1]]
    #     self.movePiece(t1, t2)
        

    def resetBoardHighlighting(self):
        for tile in self.alteredTiles:
            self.board[tile[0]][tile[1]].resetTile()


    def resetBoardSelections(self):
        self.selection = ()
        self.clickSequence = []
        self.moveList = []
        self.resetBoardHighlighting()
        self.alteredTiles = []


    def updateSelections(self, click):
        if self.selection == click:
            self.resetBoardSelections
        else:
            self.selection = click
            self.clickSequence.append(self.selection)
            if len(self.clickSequence) == 2:
                t1 = self.board[self.clickSequence[0][0]][self.clickSequence[0][1]]
                t2 = self.board[self.clickSequence[1][0]][self.clickSequence[1][1]]
                if t1.getPiece() != "__":
                    self.movePiece(t1, t2)
                self.resetBoardSelections()
                self.drawBoard()
                if (self.aiTurn and self.ai_Mode):
                    self.aiMovePiece()
                    self.drawBoard()
            else:
                self.handleSelection()
                self.drawBoard()
    
    def findLegalMoves(self, tile):
        square = chess.parse_square(tile.getNotation())
        legal_moves = list(self.boardEngine.legal_moves)
        moves_from_square = [move for move in legal_moves if move.from_square == square]
        self.moveList = [move.uci() for move in moves_from_square]
        print(self.moveList)

    def handleSelection(self):
        tile = self.board[self.selection[0]][self.selection[1]]
        self.alteredTiles.append((self.selection[0], self.selection[1]))
        tile.setColor((212, 211, 211))
        if tile.getPiece() != "__": # and tile.getPiece()[0] != "b":
            self.findLegalMoves(tile)
            self.markMoves()
            print("yay")

    def markMoves(self):
        for move in self.moveList:
            col = fileToCol[move[2]]
            row = rankToRow[move[3]]
            self.board[row][col].markTile()
            self.alteredTiles.append((row, col))
        



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
            self.surface.blit(marker, (self.x + 33, self.y + 33))

        pygame.display.flip()
    

    def setPiece(self, piece):
        self.piece = piece


    def getPiece(self):
        return self.piece
    

    def getNotation(self):
        return (self.file + self.rank)
    

    def setColor(self, highlight):
        self.color = highlight


    def resetTile(self):
        self.color = self.defaultColor
        self.mark = False

    def markTile(self):
        self.mark = True

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
    

    