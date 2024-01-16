import board_handler
import time
from openai import OpenAI
from stockfish import Stockfish
import pygame
from pygame.locals import *
import chess

BACKGROUND_COLOR = (49, 46, 43)
gameLog = []


class Game:
    def __init__(self):
        pygame.display.set_caption("ChessTutor (Powered by GPT)")
        self.surface = pygame.display.set_mode((1600,900))
        self.surface.fill(BACKGROUND_COLOR)
        self.clock = pygame.time.Clock()
        self.board = board_handler.Board(self.surface)
        self.board.drawBoard()
        self.selection = ()
        self.clickSequence = []
        

        # 8-3 = 5 | 3 + 8 = 11| 11- 5 = 6 || 3 = n 8 = N
        # top lef corner (32, 13)
        # y change = 101px per
        # x change = 107px per
        pygame.draw.rect(self.surface, (255,0,0), pygame.Rect(890, 13, 2, 2))
        pygame.display.flip()

    def mouseHandler(self):
        x, y = pygame.mouse.get_pos()

        if x < 832 and x > 32:
            if y < 813 and y > 12:
                col = (x - 32) // 100
                row = (y - 12) // 100
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
    board = chess.Board()

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

    square = chess.parse_square("e1")

    legal_moves = list(board.legal_moves)

    moves_from_square = [move for move in legal_moves if move.from_square == square]

    moveList = [move.uci() for move in moves_from_square]

    print(moveList)

    game.run()
    # Oh boy