import board_handler
import time
from openai import OpenAI
from stockfish import Stockfish
import pygame
from pygame.locals import *
import chess
import chess.engine


global game_over
game_over = False

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
        # pygame.init()

        # pygame.font.init()


        pygame.display.flip()

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
                        running = False
                    if event.key == K_RETURN:
                        print("return")
                        menu = False
                    if event.key == K_u:
                        self.board.undoMove()
                        print("u")

                
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