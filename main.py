import board_handler
import time
from openai import OpenAI
from stockfish import Stockfish
import pygame
from pygame.locals import *
import chess
import chess.engine
import sys


global game_over
game_over = False

BACKGROUND_COLOR = (49, 46, 43)

gameLog = []


class Game:
    def __init__(self):
        pygame.display.set_caption("ChessTutor (Powered by GPT)")
        if sys.platform.startswith('win32'):
            self.surface = pygame.display.set_mode((1600,900))
        else:
            self.surface = pygame.display.set_mode((1600,900), pygame.FULLSCREEN)
        self.surface.fill(BACKGROUND_COLOR)
        self.clock = pygame.time.Clock()
        self.board = board_handler.Board(self.surface)
        self.board.drawBoard()
        self.selection = ()
        self.clickSequence = []
        self.drawSelector()
        # pygame.init()

        # pygame.font.init()

        # 3 buttons at bottom, 880 start giving 720 room , 720 / 3 = 240 per button
        # Selected button gets set to background color and given white text, the menu above will be background color with border
        # Non selected buttons will be light tile color with black text

        pygame.draw.rect(self.surface, board_handler.DARKSQUARECOLOR, pygame.rect.Rect(868, 12, 720, 888), 10, border_radius=16)


        
        pygame.display.flip()


    def drawSelector(self):
        # 3 option buttons
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, pygame.rect.Rect(870, 810, 240, 82))
        pygame.draw.rect(self.surface, (241, 217, 181), pygame.rect.Rect(1108, 810, 240, 82))
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, pygame.rect.Rect(1348, 810, 238, 82))

        # Vertical Dividers
        pygame.draw.rect(self.surface, board_handler.DARKSQUARECOLOR, pygame.rect.Rect(1343, 810, 10, 82))
        pygame.draw.rect(self.surface, board_handler.DARKSQUARECOLOR, pygame.rect.Rect(1103, 810, 10, 82))

        # Horizontal Divider
        pygame.draw.rect(self.surface, board_handler.DARKSQUARECOLOR, pygame.rect.Rect(868, 800, 720, 10))


    def mouseHandler(self):
        x, y = pygame.mouse.get_pos()

        if x < 832 and x > 32:
            if y < 813 and y > 12:
                col = (x - 32) // 100
                row = (y - 12) // 100
                self.board.updateSelections((row, col))
                


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
                        self.board.quitAiEngine()
                        running = False
                    if event.key == K_RETURN:
                        print("return")
                        menu = False
                    if event.key == K_u:
                        self.board.undoMove()
                        print("u")
                    if event.key == K_i:
                        self.board.invertBoard()
                        print("i")

                
                elif event.type == QUIT:
                    print("quit")
                    self.board.quitAiEngine()
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
    board = chess.Board()


    # engine = chess.engine.SimpleEngine.popen_uci("ChessTutor/komodo-14.1-64bit.exe")
    # engine.configure({"Skill": 1})

    # result = engine.play(board, chess.engine.Limit(time= 0.1))

    # print(result.move)
    # print(board.legal_moves)
    # move = chess.Move.from_uci("e2e4")
    # if move in board.legal_moves:
    #     print("Yippee")
    #     board.push(move)
    #     print(board.legal_moves)
    #     move = chess.Move.from_uci("d7d6")
    #     board.push(move)
    #     print(board.legal_moves)
    # print(board.attacks("B2"))

    # square = chess.parse_square("e1")

    # legal_moves = list(board.legal_moves)

    # moves_from_square = [move for move in legal_moves if move.from_square == square]

    # moveList = [move.uci() for move in moves_from_square]

    # print(moveList)

    # board.
    game.run()
    

    # engine.quit()
    # Oh boy